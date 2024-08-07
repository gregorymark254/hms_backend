from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from datetime import datetime

from sqlalchemy.orm import relationship

from app.utils.database import Base


class Prescription(Base):
    __tablename__ = 'prescription'
    prescriptionId = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    prescriptionName = Column(String(50), nullable=False)
    dosage = Column(String(50), nullable=False)
    instructions = Column(String(50), nullable=False)
    prescriptionDate = Column(Date, nullable=False)
    patientId = Column(Integer, ForeignKey('patients.patientId'), nullable=False, unique=True, index=True)
    doctorId = Column(Integer, ForeignKey('doctors.doctorId'), nullable=False, unique=True, index=True)
    createdAt = Column(DateTime, nullable=False, default=datetime.utcnow())

    patient = relationship('Patient', back_populates='prescriptions')
    doctor = relationship('Doctor', back_populates='prescriptions')
