from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class AddAppointment(BaseModel):
    appointmentDate: date
    reason: str
    status: str
    patientId: int
    doctorId: int


class AppointmentSchema(AddAppointment):
    appointmentId: int
    createdAt: datetime

    model_config = ConfigDict(from_attributes=True)


class ListAppointment(BaseModel):
    items: list[AppointmentSchema]
    total: int
    count: int
