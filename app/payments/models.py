import enum
from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Enum
from sqlalchemy.orm import relationship

from app.utils.database import Base

class PaymentEnum(enum.Enum):
    cash = 'cash'
    mpesa = 'mpesa'

class Payment(Base):
    __tablename__ = 'payments'
    paymentId = Column(Integer, primary_key=True, autoincrement=True)
    transactionId = Column(String(100), nullable=False, unique=True, index=True)
    amount = Column(Integer, nullable=False)
    paymentMethod = Column(Enum(PaymentEnum), nullable=False)
    paymentDate = Column(DateTime, nullable=False, default=datetime.utcnow())
    patientId = Column(Integer, ForeignKey('patients.patientId'), nullable=False, index=True)
    billingId = Column(Integer, ForeignKey('billing.billingId'), nullable=False, index=True)
    createdAt = Column(DateTime, default=datetime.utcnow())
    status = Column(String(50), nullable=False)
    mpesaRef = Column(String(100), nullable=True)

    billings = relationship("Billing", back_populates="payment")


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    merchant_req_id = Column(String(100), unique=True, index=True)
    phone_no = Column(String(20), nullable=False)
    amount = Column(Integer, nullable=False)
    status = Column(String(20))
    mpesa_ref = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())