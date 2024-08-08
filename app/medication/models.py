from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from app.utils.database import Base


class Medication(Base):
    __tablename__ = 'medication'
    medicationId = Column(Integer, primary_key=True, autoincrement=True)
    diagnosis = Column(String(255), nullable=False)
    treatment = Column(String(255), nullable=False)
    notes = Column(String(255), nullable=False)
    recordDate = Column(DateTime, nullable=False)
    patientId = Column(Integer, ForeignKey('patients.patientId'), nullable=False, index=True)
    prescriptionId = Column(Integer, ForeignKey('prescription.prescriptionId'), nullable=False, index=True)
    createdAt = Column(DateTime, default=datetime.utcnow())
