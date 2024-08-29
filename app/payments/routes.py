from datetime import datetime

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from . import router, schemas, models
from .models import PaymentEnum
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


@router.post('/stk_push')
async def send_stk_push(request: schemas.StkPush):
    mpesa = Mpesa()
    payload = mpesa.stk_push(phone=request.phone, amount=request.amount)
    response = mpesa.send_stk_push(payload)

    return response.json()



@router.post("/stk_callback")
async def process_response(request: Request, db: Session = Depends(get_db)):
    try:
        json_response = await request.json()
        stk_callback = json_response['Body']['stkCallback']

        merchant_response_id = stk_callback['CheckoutRequestID']
        result_code = stk_callback['ResultCode']
        mpesa_ref = stk_callback['CallbackMetadata']['Item'][1]['Value']

        # Find the corresponding transaction
        transaction = db.query(models.Transaction).filter(models.Transaction.merchant_req_id == merchant_response_id).first()

        if transaction:
            if result_code == 0:
                # Update the transaction status
                transaction.status = "Completed"
                transaction.mpesa_ref = mpesa_ref
                transaction.updated_at = datetime.now()

                # Create a corresponding payment record
                related_payment = models.Payment(
                    transactionId=merchant_response_id,
                    amount=transaction.amount,
                    paymentMethod=models.PaymentEnum.mpesa,
                    patientId=transaction.patientId,
                    billingId=transaction.billingId,
                    status="Completed",
                    mpesaRef=mpesa_ref
                )
                db.add(related_payment)
                db.commit()

                return {"message": "Payment processed"}
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
