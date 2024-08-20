from fastapi import Depends
from sqlalchemy.orm import Session, joinedload

from . import router, schemas, models
from ..users.models import get_current_user
from ..utils.database import get_db
from ..utils.pagination import Pagination, Paginator


@router.get('/', response_model=schemas.ListBilling, dependencies=[Depends(get_current_user)])
def get_billing(db: Session = Depends(get_db), pagination: Paginator = Depends(), patientId: int | None = None):
    query = db.query(models.Billing).options(joinedload(models.Billing.patient))
    if patientId:
        query = query.filter_by(patientId=patientId)
    total = query.count()
    billings = query.offset(pagination.offset).limit(pagination.limit).all()
    count = len(billings)

    formatted_results = [billing.to_json() for billing in billings]
    return Pagination(items=formatted_results, total=total, count=count)


@router.post('/', response_model=schemas.BillingSchema, dependencies=[Depends(get_current_user)])
def create_billing(request: schemas.AddBilling, db: Session = Depends(get_db)):
    billing = models.Billing(**request.model_dump())
    db.add(billing)
    db.commit()
    db.refresh(billing)
    return billing