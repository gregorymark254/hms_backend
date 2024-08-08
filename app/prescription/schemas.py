from datetime import datetime

from pydantic import BaseModel


class AddPrescription(BaseModel):
    prescriptionName: str
    dosage: str
    instructions: str
    prescriptionDate: datetime
    patientId: int
    doctorId: int


class Prescription(AddPrescription):
    prescriptionId: int
    createdAt: datetime


class ListPrescription(BaseModel):
    items: list[Prescription]
    total: int
    count: int