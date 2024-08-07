from datetime import datetime

from pydantic import BaseModel


class AddPatientSchema(BaseModel):
    firstName: str
    lastName: str
    email: str
    dateOfBirth: str
    gender: str
    address: str
    phoneNumber: str
    emergencyNUmber: str
    insuranceNumber: str
    insuranceName: str


class PatientSchema(AddPatientSchema):
    createdAt: datetime


class ListPatients(BaseModel):
    items: list[PatientSchema]
    total: int
    count: int
