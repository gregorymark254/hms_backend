from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from app.utils.database import Base


class Payment(Base):
    __tablename__ = 'payments'
    paymentId = Column(Integer, primary_key=True, autoincrement=True)
    transactionId = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    paymentMethod = Column(String(20), nullable=False)
    paymentDate = Column(DateTime, nullable=False)
    patientId = Column(Integer, ForeignKey('patients.patientId'), nullable=False, unique=True)
    billingId = Column(Integer, ForeignKey('billing.billingId'), nullable=False, unique=True)
    createdAt = Column(DateTime, default=datetime.utcnow())

    patient = relationship("Patient", back_populates="payments")
    billing = relationship("Billing", back_populates="payments")
