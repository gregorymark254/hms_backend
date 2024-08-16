from datetime import datetime

from pydantic import BaseModel


class AddBilling(BaseModel):
    amount: int
    billingDate: datetime
    patientId: int


class BillingSchema(AddBilling):
    billingId: int
    status: str
    createdAt: datetime


class ListBilling(BaseModel):
    items: list[BillingSchema]
    total: int
    count: int