from datetime import datetime, date

from pydantic import BaseModel


class AddPatientSchema(BaseModel):
    firstName: str
    lastName: str
    email: str
    dateOfBirth: date
    gender: str
    address: str
    phoneNumber: str
    emergencyNumber: str
    insuranceNumber: str
    insuranceName: str


class UpdatePatient(BaseModel):
    firstName: str
    lastName: str
    dateOfBirth: date
    gender: str
    address: str
    phoneNumber: str
    emergencyNumber: str
    insuranceNumber: str
    insuranceName: str


class PatientSchema(AddPatientSchema):
    patientId: int
    createdAt: datetime


class ListPatients(BaseModel):
    items: list[PatientSchema]
    total: int
    count: int
