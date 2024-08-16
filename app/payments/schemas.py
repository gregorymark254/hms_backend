from datetime import datetime

from pydantic import BaseModel


class AddPayment(BaseModel):
    transactionId: str
    amount: int
    paymentMethod: str
    paymentDate: datetime
    patientId: int
    billingId: int


class PaymentSchema(AddPayment):
    paymentId: int
    createdAt: datetime


class ListPayment(BaseModel):
    items: list[PaymentSchema]
    total: int
    count: int