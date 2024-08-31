from datetime import datetime

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from . import router, schemas, models
from .mpesa import Mpesa
from ..users.models import get_current_user
from ..utils.database import get_db
from ..utils.pagination import Pagination, Paginator
from ..billing import models as billing_models

@router.get('/', response_model=schemas.ListPayment, dependencies=[Depends(get_current_user)])
async def get_payments(db: Session = Depends(get_db), pagination: Paginator = Depends()):
    query = db.query(models.Payment)
    total = query.count()
    payments = query.offset(pagination.offset).limit(pagination.limit).all()
    count = len(payments)
    return Pagination(items=payments, total=total, count=count)


@router.post('/', response_model=schemas.PaymentSchema, dependencies=[Depends(get_current_user)])
async def add_payment(request: schemas.AddPayment, db: Session = Depends(get_db)):
    payment = models.Payment(**request.model_dump())
    db.add(payment)

    billing = db.query(billing_models.Billing).filter(billing_models.Billing.billingId == request.billingId).first()
    if billing is None:
        raise HTTPException(status_code=404, detail='Billing not found')

    billing.status = 'paid'

    db.commit()
    db.refresh(payment)
    return payment


@router.post('/mpesa', dependencies=[Depends(get_current_user)])
async def mpesa_pay(request: schemas.MpesaPayment, db: Session = Depends(get_db)):
    amount = request.amount
    phone_number = request.phoneNumber
    billing_id = request.billingId
    patient_id = request.patientId

    # Find the billing record
    billing = db.query(billing_models.Billing).filter(billing_models.Billing.billingId == billing_id).first()
    if not billing:
        raise HTTPException(status_code=404, detail='Billing record not found')

    # Verify the amount matches
    if billing.amount != amount:
        raise HTTPException(status_code=400, detail='Amount does not match billing amount')

    # send stk push and get merchant request id
    mpesa = Mpesa()
    payload = mpesa.stk_push(phone=request.phoneNumber, amount=request.amount)
    response = mpesa.send_stk_push(payload)

    # get response from stk push
    json_response = response.json()
    try:
        merchant_response_id = json_response['MerchantRequestID']
        checkout_req_id = json_response['CheckoutRequestID']
        response_code = json_response['ResponseCode']
        response_description = json_response['ResponseDescription']
        customer_message = json_response['CustomerMessage']
    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"Unexpected response format: {e}")

    # Check if a transaction with the same billingId already exists
    existing_transaction = db.query(models.Transaction).filter_by(billingId=billing_id).first()

    if existing_transaction:
        # Update the existing transaction
        existing_transaction.merchant_req_id = merchant_response_id
        existing_transaction.checkout_req_id = checkout_req_id
        existing_transaction.response_code = response_code
        existing_transaction.response_description = response_description
        existing_transaction.customer_message = customer_message
        existing_transaction.phoneNumber = phone_number
        existing_transaction.amount = amount
        existing_transaction.status = "Pending"
        existing_transaction.patientId = patient_id

    else:
        # Create a new transaction record
        transaction = models.Transaction(
            merchant_req_id=merchant_response_id,
            checkout_req_id=checkout_req_id,
            response_code=response_code,
            response_description=response_description,
            customer_message=customer_message,
            phoneNumber=phone_number,
            amount=amount,
            status="Pending",
            billingId=billing_id,
            patientId=patient_id
        )
        db.add(transaction)
    db.commit()

    print(response.json())
    print("------Payment initiated successfully------")
    return response.json()



@router.post("/stk_callback")
async def process_response(request: Request, db: Session = Depends(get_db)):
    try:
        print('------Callback received------')
        json_response = await request.json()
        print(json_response)
        print('-------End of callback-------')

        stk_callback = json_response['Body']['stkCallback']
        merchant_response_id = stk_callback['MerchantRequestID']
        result_code = stk_callback['ResultCode']

        mpesa_ref = stk_callback['CallbackMetadata']['Item'][1]['Value'] # mpesa transaction code
        mpesa_amount = stk_callback['CallbackMetadata']['Item'][0]['Value'] # mpesa transaction amount
        mpesa_number = stk_callback['CallbackMetadata']['Item'][4]['Value'] # mpesa transaction phone number
        mpesa_date = stk_callback['CallbackMetadata']['Item'][3]['Value'] # mpesa transaction date time

        # Convert transaction date to datetime
        transaction_date = None
        if mpesa_date:
            try:
                transaction_date = datetime.strptime(str(mpesa_date), '%Y%m%d%H%M%S')
            except ValueError:
                raise HTTPException(status_code=400, detail='Invalid transaction date format')

        # Find the corresponding transaction
        transaction = db.query(models.Transaction).filter(models.Transaction.merchant_req_id == merchant_response_id).first()

        if transaction:
            if result_code == 0:
                # Update the transaction status
                transaction.status = "Completed"

                # Save the corresponding payment record
                save_payment = models.Payment(
                    transactionId=mpesa_ref,
                    amount=mpesa_amount,
                    paymentMethod=models.PaymentEnum.mpesa,
                    phoneNumber=mpesa_number,
                    paymentDate=transaction_date,
                    patientId=transaction.patientId,
                    billingId=transaction.billingId,
                    status=models.PaymentStatusEnum.Completed,
                )
                db.add(save_payment)
                db.commit()

                # Update the related billing status
                billing = db.query(billing_models.Billing).filter(
                    billing_models.Billing.billingId == transaction.billingId).first()
                if billing:
                    billing.status = billing_models.BillingEnum.paid
                    db.commit()

                return {"message": "Payment processed successfully"}
            else:
                return {"message": "Transaction failed", "result_code": result_code}
        else:
            raise HTTPException(status_code=404, detail="Transaction not found")

    except Exception as e:
        db.rollback()
        print(f"Error processing response: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        db.close()


@router.get('/transaction_status', response_model=schemas.ListTransactions, dependencies=[Depends(get_current_user)])
async def get_transaction_status(db: Session = Depends(get_db), pagination: Paginator = Depends()):
    query = db.query(models.Transaction)
    total = query.count()
    transaction_status = query.offset(pagination.offset).limit(pagination.limit).all()
    count = len(transaction_status)
    return Pagination(items=transaction_status, total=total, count=count)


'''
* POLLING TRANSACTIONS
* THIS USED WHEN CHECKING IF A PAYMENT IS COMPLETE IF CALLBACK URL IS NOT REACHED AFTER STK PUSH
'''
@router.post('/transaction_status/{billingId}', dependencies=[Depends(get_current_user)])
async def check_transaction_status(billingId: int, db: Session = Depends(get_db)):
    # Query the database for the transaction using billingId
    transaction = db.query(models.Transaction).filter(models.Transaction.billingId == billingId).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # checkout_request_id from transaction table to send in request body of stk query
    checkout_request_id = transaction.checkout_req_id

    # Sending stk query to check if transaction was complete or failed
    mpesa_status = Mpesa()
    payload = mpesa_status.payment_status(checkout_request_id=checkout_request_id)
    response = mpesa_status.check_payment_status(payload)

    print('------Response Received------')
    print(response)
    result = response.get('ResultCode')
    print('-------End of response-------')


    if int(result) == 0:
        # Update the transaction status if result code is 0
        transaction.status = "Completed"
        db.commit()

        # Update the related billing status if it is pending
        billing = db.query(billing_models.Billing).filter(
            billing_models.Billing.billingId == transaction.billingId).first()
        if billing.status == 'pending':
            billing.status = billing_models.BillingEnum.paid
            db.commit()
        else:
            pass

        return {"message": "Payment processed successfully"}
    else:
        return {"message": "Payment failed", "ResultDesc": response.get('ResultDesc')}