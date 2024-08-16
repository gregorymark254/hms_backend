from fastapi import Depends
from sqlalchemy.orm import Session

from . import router, schemas, models
from ..users.models import get_current_user
from ..utils.database import get_db
from ..utils.pagination import Pagination, Paginator


@router.get('/', response_model=schemas.ListPayment, dependencies=[Depends(get_current_user)])
def get_payments(db: Session = Depends(get_db), pagination: Paginator = Depends()):
    query = db.query(models.Payment)
    total = query.count()
    payments = query.offset(pagination.offset).limit(pagination.limit).all()
    count = len(payments)
    return Pagination(items=payments, total=total, count=count)


@router.post('/', response_model=schemas.PaymentSchema, dependencies=[Depends(get_current_user)])
async def add_payment(request: schemas.AddPayment, db: Session = Depends(get_db)):
    payment = models.Payment(**request.model_dump())
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment