from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class AddAppointment(BaseModel):
    appointmentDate: date
    reason: str
    patientId: int
    doctorId: int


class AppointmentSchema(AddAppointment):
    appointmentId: int
    patient_name: str
    doctor_name: str
    status: str
    createdAt: datetime

    model_config = ConfigDict(from_attributes=True)


class ListAppointment(BaseModel):
    items: list[AppointmentSchema]
    total: int
    count: int
