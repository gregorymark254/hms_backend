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
    status: str
    paymentDate: datetime
    createdAt: datetime


class StkPush(BaseModel):
    amount: int
    phone: int

class TransactionStatus(BaseModel):
    merchant_req_id: str
    checkout_req_id: str
    response_code: int
    response_description: str
    customer_message: str
    phoneNumber: str
    amount: int
    status: str
    billingId: int
    patientId: int

class ListTransactions(BaseModel):
    items: list[TransactionStatus]
    total: int
    count: int

class ListPayment(BaseModel):
    items: list[PaymentSchema]
    total: int
    count: int