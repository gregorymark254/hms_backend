from datetime import datetime

from pydantic import BaseModel


class AddMedication(BaseModel):
    diagnosis: str
    treatment: str
    notes: str
    recordDate: datetime
    patientID: int
    doctorID: int


class Medication(AddMedication):
    medicationIid: int
    createdAt: datetime


class ListMedications(BaseModel):
    items: list[Medication]
    total: int
    count: int
