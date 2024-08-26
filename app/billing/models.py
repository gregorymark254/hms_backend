import enum
from datetime import datetime

from sqlalchemy import Column, Integer, Date, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship

from app.utils.database import Base

class BillingEnum(enum.Enum):
    pending = "pending"
    paid = "paid"


class Billing(Base):
    __tablename__ = 'billing'
    billingId = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Integer, nullable=False)
    billingDate = Column(Date, nullable=False)
    status = Column(Enum(BillingEnum), default=BillingEnum.pending, nullable=False)
    patientId = Column(Integer, ForeignKey('patients.patientId'), nullable=False, index=True)
    createdAt = Column(DateTime, nullable=False, default=datetime.utcnow())

    payment = relationship('Payment', back_populates='billings', lazy='joined')
    patient = relationship('Patient', back_populates='billings', lazy='joined')

    def to_json(self):
        patient_name = self.patient.firstName + " " + self.patient.lastName if self.patient else None

        return {
            'billingId': self.billingId,
            'amount': self.amount,
            'billingDate': self.billingDate,
            'status': self.status,
            'patientId': self.patientId,
            'patient_name': patient_name,
            'phoneNumber': self.patient.phoneNumber,
            'createdAt': self.createdAt,
        }
