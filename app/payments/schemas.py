from datetime import datetime

from pydantic import BaseModel


class AddPayment(BaseModel):
    transactionId: str
    amount: int
    paymentMethod: str
    phoneNumber: str
    patientId: int
    billingId: int

class MpesaPayment(BaseModel):
    amount: int
    paymentMethod: str
    phoneNumber: str
    patientId: int
    billingId: int

class PaymentSchema(AddPayment):
    paymentId: int
    paymentDate: datetime
    createdAt: datetime


class StkPush(BaseModel):
    amount: int
    phone: int

class ListPayment(BaseModel):
    items: list[PaymentSchema]
    total: int
    count: int