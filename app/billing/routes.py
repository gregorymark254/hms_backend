from dns.e164 import query
from fastapi import Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload

from . import router, schemas, models
from ..users.models import get_current_user
from ..utils.database import get_db
from ..utils.pagination import Pagination, Paginator


@router.get('/', response_model=schemas.ListBilling, dependencies=[Depends(get_current_user)])
async def get_billing(db: Session = Depends(get_db), pagination: Paginator = Depends(), patientId: int | None = None):
    query = db.query(models.Billing).options(joinedload(models.Billing.patient))
    if patientId:
        query = query.filter_by(patientId=patientId)
    total = query.count()
    billings = query.order_by(desc(models.Billing.billingId)).offset(pagination.offset).limit(pagination.limit).all()
    count = len(billings)

    formatted_results = [billing.to_json() for billing in billings]
    return Pagination(items=formatted_results, total=total, count=count)


@router.post('/', dependencies=[Depends(get_current_user)])
async def create_billing(request: schemas.AddBilling, db: Session = Depends(get_db)):
    billing = models.Billing(**request.model_dump())
    db.add(billing)
    db.commit()
    db.refresh(billing)
    return {'message': 'Billing has been added.'}


@router.get('/{billingId}', response_model=schemas.PayBill, dependencies=[Depends(get_current_user)])
async def get_billing_by_id(billingId: int, db: Session = Depends(get_db)):
    bill = db.query(models.Billing).filter_by(billingId=billingId).first()

    if not bill:
        raise HTTPException(status_code=404, detail='Billing not found')
    else:
        return bill.to_json()
