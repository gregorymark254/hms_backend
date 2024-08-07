from datetime import datetime

from sqlalchemy import Column, Integer, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.utils.database import Base


class Billing(Base):
    __tablename__ = 'billing'
    billingId = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Integer, nullable=False)
    billingDate = Column(Date, nullable=False)
    status = Column(Integer, nullable=False)
    patientId = Column(Integer, ForeignKey('patients.patientId'), nullable=False, unique=True)
    createdAt = Column(DateTime, nullable=False, default=datetime.utcnow())

    patient = relationship('Patient', back_populates='billing')
    payments = relationship('Payment', back_populates='billing')