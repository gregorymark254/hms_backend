from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from . import router, schemas, models
from ..users.models import get_current_user, get_admin_or_pharmacy
from ..utils.database import get_db
from ..utils.pagination import Pagination, Paginator


@router.get('/', response_model=schemas.ListPrescription, dependencies=[Depends(get_current_user)])
async def get_prescriptions(db: Session = Depends(get_db), pagination: Paginator = Depends()):
    query = db.query(models.Prescription)
    total = query.count()
    prescriptions = query.offset(pagination.offset).limit(pagination.limit).all()
    count = len(prescriptions)
    return Pagination(items=prescriptions, total=total, count=count)


@router.post('/', response_model=schemas.Prescription, dependencies=[Depends(get_admin_or_pharmacy)])
async def create_prescription(request: schemas.AddPrescription, db: Session = Depends(get_db)):
    new_prescription = models.Prescription(**request.model_dump())
    db.add(new_prescription)
    db.commit()
    db.refresh(new_prescription)
    return new_prescription


@router.get('/{prescriptionId}', response_model=schemas.Prescription, dependencies=[Depends(get_current_user)])
async def get_prescription_by_id(prescriptionId: int, db: Session = Depends(get_db)):
    query = db.query(models.Prescription).filter_by(prescriptionId=prescriptionId).first()
    if not query:
        raise HTTPException(status_code=404, detail='Prescription not found')

    return query


@router.put('/{prescriptionId}', dependencies=[Depends(get_admin_or_pharmacy)])
async def update_prescription(prescriptionId: str, request:schemas.AddPrescription, db: Session = Depends(get_db)):
    query = db.query(models.Prescription).filter_by(prescriptionId=prescriptionId).first()
    if not query:
        raise HTTPException(status_code=404, detail='Prescription not found')

    query.prescriptionName = request.prescriptionName
    query.dosage = request.dosage
    query.instructions = request.instructions
    query.duration = request.duration

    db.commit()
    db.refresh(query)

    return {'message': f'prescription {query.prescriptionName} updated'}