from fastapi import Depends
from sqlalchemy.orm import Session

from . import router, schemas, models
from ..users.models import get_current_user
from ..utils.database import get_db
from ..utils.pagination import Pagination, Paginator


@router.get('/', response_model=schemas.ListDoctors, dependencies=[Depends(get_current_user)])
def get_doctors(db: Session = Depends(get_db), pagination: Paginator = Depends()):
    query = db.query(models.Doctor)
    total = query.count()
    doctors = query.offset(pagination.offset).limit(pagination.limit).all()
    count = len(doctors)
    return Pagination(items=doctors, total=total, count=count)


@router.post('/', response_model=schemas.DoctorSchema, dependencies=[Depends(get_current_user)])
async def add_doctor(request: schemas.AddDoctor, db: Session = Depends(get_db)):
    doctor = models.Doctor(**request.model_dump())
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor