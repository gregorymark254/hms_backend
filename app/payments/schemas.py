from datetime import datetime

from pydantic import BaseModel


class AddPayment(BaseModel):
    transactionId: str
    amount: int
    paymentMethod: str
    patientId: int
    billingId: int


class PaymentSchema(AddPayment):
    paymentId: int
    paymentDate: datetime
    createdAt: datetime


class ListPayment(BaseModel):
    items: list[PaymentSchema]
    total: int
    count: int