from fastapi import Depends
from sqlalchemy.orm import Session, joinedload

from . import router, schemas, models
from ..users.models import get_current_user
from ..utils.database import get_db
from ..utils.pagination import Paginator, Pagination


@router.get('/', response_model=schemas.ListAppointment, dependencies=[Depends(get_current_user)])
async def get_appointments(db: Session = Depends(get_db), pagination: Paginator = Depends(), patientId: int | None = None, doctorId: int | None = None):
    query = db.query(models.Appointment).options(joinedload(models.Appointment.patient), joinedload(models.Appointment.doctor))
    if patientId:
        query = query.filter_by(patientId=patientId)
    if doctorId:
        query = query.filter_by(doctorId=doctorId)

    total = query.count()
    appointments = query.offset(pagination.offset).limit(pagination.limit).all()
    count = len(appointments)

    formatted_results = [appointment.to_json() for appointment in appointments]
    return Pagination(items=formatted_results, total=total, count=count)


@router.post('/', response_model=schemas.AppointmentSchema, dependencies=[Depends(get_current_user)])
async def add_appointment(request: schemas.AddAppointment, db: Session = Depends(get_db)):
    new_appointment = models.Appointment(**request.model_dump())
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment
