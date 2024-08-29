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

    billings = relationship("Billing", back_populates="payment")


class Transaction(Base):
    __tablename__ = 'transactions'

    merchant_req_id = Column(String(100), primary_key=True, index=True)
    phoneNumber = Column(String(20), nullable=False)
    amount = Column(Integer, nullable=False)
    status = Column(Enum(TransactionStatusEnum), nullable=False)
    billingId = Column(Integer, nullable=False, index=True)
    patientId = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())