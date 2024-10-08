from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from . import router, models, schemas
from ..users.models import get_current_user
from ..utils.database import get_db
from ..utils.pagination import Pagination, Paginator


@router.get('/', response_model=schemas.ListPatients, dependencies=[Depends(get_current_user)])
async def get_patients(email: str | None = None, db: Session = Depends(get_db), pagination: Paginator = Depends()):
    query = db.query(models.Patient)

    if email:
        query = query.filter(email=email)

    total = query.count()
    patients = query.offset(pagination.offset).limit(pagination.limit).all()
    count = len(patients)
    return Pagination(items=patients, total=total, count=count)


@router.post('/', response_model=schemas.PatientSchema, dependencies=[Depends(get_current_user)])
async def add_patient(request: schemas.AddPatientSchema, db: Session = Depends(get_db)):
    new_patient = models.Patient(**request.model_dump())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient


@router.get('/{patientId}', response_model=schemas.PatientSchema, dependencies=[Depends(get_current_user)])
async def get_patient_by_id(patientId: int, db: Session = Depends(get_db)):
    query = db.query(models.Patient).filter_by(patientId=patientId).first()
    if query is None:
        raise HTTPException(status_code=404, detail="User not found")
    return query


@router.put('/{patientId}', dependencies=[Depends(get_current_user)])
async def update_patient(patientId: int, request: schemas.UpdatePatient, db: Session = Depends(get_db)):
    query = db.query(models.Patient).filter_by(patientId=patientId).first()
    if not query:
        raise HTTPException(status_code=404, detail="User not found")

    query.firstName = request.firstName
    query.lastName = request.lastName
    query.dateOfBirth = request.dateOfBirth
    query.gender = request.gender
    query.address = request.address
    query.phoneNumber = request.phoneNumber
    query.emergencyNumber = request.emergencyNumber
    query.insuranceNumber = request.insuranceNumber
    query.insuranceName = request.insuranceName

    db.commit()
    db.refresh(query)

    return {'message': f'patient {query.email} updated'}
