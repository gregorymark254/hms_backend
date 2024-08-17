from datetime import datetime

from pydantic import BaseModel


class AddMedication(BaseModel):
    diagnosis: str
    treatment: str
    notes: str
    patientId: int
    prescriptionId: int


class Medication(AddMedication):
    medicationId: int
    patient_name: str
    prescriptionName: str
    createdAt: datetime


class ListMedications(BaseModel):
    items: list[Medication]
    total: int
    count: int
