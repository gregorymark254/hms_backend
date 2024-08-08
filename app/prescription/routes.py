from fastapi import Depends
from sqlalchemy.orm import Session

from . import router, schemas, models
from ..users.models import get_current_user
from ..utils.database import get_db
from ..utils.pagination import Pagination, Paginator


@router.get('/', response_model=schemas.ListPrescription, dependencies=[Depends(get_current_user)])
async def get_prescriptions(db: Session = Depends(get_db), pagination: Paginator = Depends()):
    query = db.query(models.Prescription)
    total = query.count()
    prescriptions = query.offset(pagination.offset).limit(pagination.limit).all()
    count = len(prescriptions)
    return Pagination(items=prescriptions, total=total, count=count)


@router.post('/', response_model=schemas.Prescription, dependencies=[Depends(get_current_user)])
async def create_prescription(request: schemas.AddPrescription, db: Session = Depends(get_db)):
    new_prescription = models.Prescription(**request.model_dump())
    db.add(new_prescription)
    db.commit()
    db.refresh(new_prescription)
    return new_prescription