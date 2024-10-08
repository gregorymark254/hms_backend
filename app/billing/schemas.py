from datetime import datetime, date

from pydantic import BaseModel


class AddBilling(BaseModel):
    amount: int
    billingDate: date
    patientId: int


class BillingSchema(AddBilling):
    billingId: int
    patient_name: str
    phoneNumber: str
    status: str
    createdAt: datetime


class PayBill(BaseModel):
    amount: int
    phoneNumber: str
    patientId: int
    billingId: int


class ListBilling(BaseModel):
    items: list[BillingSchema]
    total: int
    count: int
