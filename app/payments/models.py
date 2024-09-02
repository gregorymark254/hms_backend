import enum
from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Enum
from sqlalchemy.orm import relationship

from app.utils.database import Base

class PaymentEnum(enum.Enum):
    cash = 'cash'
    mpesa = 'mpesa'

class PaymentStatusEnum(enum.Enum):
    Completed = 'Completed'
    Pending = 'Pending'

class TransactionStatusEnum(enum.Enum):
    Completed = 'Completed'
    Pending = 'Pending'


class Payment(Base):
    __tablename__ = 'payments'

    paymentId = Column(Integer, primary_key=True, autoincrement=True)
    transactionId = Column(String(100), unique=True, index=True)
    amount = Column(Integer, nullable=False)
    phoneNumber = Column(String(100), nullable=False)
    paymentMethod = Column(Enum(PaymentEnum), nullable=False)
    paymentDate = Column(DateTime, nullable=False, default=datetime.utcnow())
    patientId = Column(Integer, ForeignKey('patients.patientId'), nullable=False, index=True)
    billingId = Column(Integer, ForeignKey('billing.billingId'), nullable=False, index=True)
    createdAt = Column(DateTime, default=datetime.utcnow())
    status = Column(Enum(PaymentStatusEnum), nullable=False, default=PaymentStatusEnum.Completed)

    billings = relationship("Billing", back_populates="payment", lazy='joined')
    patient = relationship("Patient", back_populates="payment")

    def to_json(self):
        patient_name = self.patient.firstName + " " + self.patient.lastName if self.patient else None

        return {
            'paymentId': self.paymentId,
            'transactionId': self.transactionId,
            'amount': self.amount,
            'phoneNumber': self.phoneNumber,
            'paymentMethod': self.paymentMethod,
            'paymentDate': self.paymentDate,
            'patientName': patient_name,
            'patientId': self.patientId,
            'billingId': self.billingId,
            'createdAt': self.createdAt,
            'status': self.status,
        }


class Transaction(Base):
    __tablename__ = 'transactions'

    merchant_req_id = Column(String(100), primary_key=True, index=True)
    checkout_req_id = Column(String(100), unique=True, index=True)
    response_code = Column(String(10), nullable=False)
    response_description = Column(String(255), nullable=False)
    customer_message = Column(String(255), nullable=False)
    phoneNumber = Column(String(20), nullable=False)
    amount = Column(Integer, nullable=False)
    status = Column(Enum(TransactionStatusEnum), nullable=False)
    billingId = Column(Integer, nullable=False, index=True)
    patientId = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())