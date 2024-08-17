from fastapi import Depends
from sqlalchemy.orm import Session

from . import router, schemas, models
from ..users.models import get_current_user, get_admin_or_doctor
from ..utils.database import get_db
from ..utils.pagination import Pagination, Paginator


@router.get('/', response_model=schemas.ListMedications, dependencies=[Depends(get_current_user)])
async def get_medication(db: Session = Depends(get_db), pagination: Paginator = Depends(), patientId: int | None = None):
    query = db.query(models.Medication)
    if patientId:
        query = query.filter_by(patientId=patientId)
    total = query.count()
    medication = query.offset(pagination.offset).limit(pagination.limit).all()
    count = len(medication)
    return Pagination(items=medication, total=total, count=count)


@router.post('/', response_model=schemas.Medication, dependencies=[Depends(get_admin_or_doctor)])
async def add_medication(request: schemas.AddMedication, db: Session = Depends(get_db)):
    medication = models.Medication(**request.model_dump())
    db.add(medication)
    db.commit()
    db.refresh(medication)
    return medication

