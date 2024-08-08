from datetime import datetime

from pydantic import BaseModel


class AddDoctor(BaseModel):
    firstName: str
    lastName: str
    email: str
    speciality: str
    phoneNumber: str


class DoctorSchema(AddDoctor):
    doctorId: int
    createdAt: datetime


class ListDoctors(BaseModel):
    items: list[DoctorSchema]
    total: int
    count: int
