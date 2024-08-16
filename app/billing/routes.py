from fastapi import Depends
from sqlalchemy.orm import Session

from . import router, schemas, models
from ..users.models import get_current_user
from ..utils.database import get_db
from ..utils.pagination import Pagination, Paginator


@router.get('/', response_model=schemas.ListBilling, dependencies=[Depends(get_current_user)])
def get_billing(db: Session = Depends(get_db), pagination: Paginator = Depends(), patientId: int | None = None):
    query = db.query(models.Billing)
    if patientId:
        query = query.filter_by(patientId=patientId)
    total = query.count()
    billing = query.offset(pagination.offset).limit(pagination.limit).all()
    count = len(billing)

    return Pagination(items=billing, total=total, count=count)


@router.post('/', response_model=schemas.BillingSchema, dependencies=[Depends(get_current_user)])
def create_billing(request: schemas.AddBilling, db: Session = Depends(get_db)):
    billing = models.Billing(**request.model_dump())
    db.add(billing)
    db.commit()
    db.refresh(billing)
    return billing