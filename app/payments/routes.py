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


@router.post('/stk_push')
async def send_stk_push(request: schemas.StkPush):
    mpesa = Mpesa()
    payload = mpesa.stk_push(phone=request.phone, amount=request.amount)
    response = mpesa.send_stk_push(payload)

    return response.json()


@router.post('/stk_callback')
async def send_stk_callback(request: Request):
    callback = await request.json()
    print('------Received Callback--------')
    print(callback)
    print('-------End of callback-------')

    return {'status': 'ok'}