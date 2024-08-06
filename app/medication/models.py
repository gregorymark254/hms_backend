from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.utils.database import Base


class Medication(Base):
    __tablename__ = 'medication'
    medicationIid = Column(Integer, primary_key=True, autoincrement=True)
    diagnosis = Column(String(255), nullable=False)
    treatment = Column(String(255), nullable=False)
    notes = Column(String(255), nullable=False)
    recordDate = Column(DateTime, nullable=False)
    patientId = Column(Integer, ForeignKey('patients.patientId'), nullable=False, unique=True)
    doctorId = Column(Integer, ForeignKey('doctors.doctorId'), nullable=False, unique=True)
    createdAt = Column(DateTime, default=datetime.utcnow())

    patient = relationship('Patient', back_populates='medications')
    doctor = relationship('Doctor', back_populates='medications')
