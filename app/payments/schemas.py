from datetime import datetime

from fastapi import HTTPException
from pydantic import BaseModel, field_validator

from app.utils.validation import validate_phone


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

    @field_validator('phoneNumber')
    def validate_phone(cls, v):
        valid_number, phoneNumber = validate_phone(v)
        if not valid_number:
            raise HTTPException(status_code=400, detail='Invalid phone number')
        return phoneNumber

class PaymentSchema(AddPayment):
    paymentId: int
    patientName: str
    status: str
    paymentDate: datetime
    createdAt: datetime


class StkPush(BaseModel):
    amount: int
    phone: int

    @field_validator('phone')
    def validate_phone(cls, v):
        valid_number , phone = validate_phone(v)
        if not valid_number:
            raise ValueError('Invalid phone number')
        return phone

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


class CheckTransaction(BaseModel):
    transaction_id: str


class ListTransactions(BaseModel):
    items: list[TransactionStatus]
    total: int
    count: int

class ListPayment(BaseModel):
    items: list[PaymentSchema]
    total: int
    count: int
