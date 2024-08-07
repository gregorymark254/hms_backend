from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.utils.database import Base


class Doctor(Base):
    __tablename__ = 'doctors'
    doctorId = Column(Integer, primary_key=True, autoincrement=True)
    firstName = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    phoneNumber = Column(String(50), nullable=False)
    speciality = Column(String(50), nullable=False)
    createdAt = Column(DateTime, nullable=False, default=datetime.utcnow())

    appointment = relationship('Appointment', back_populates='doctor')
    medications = relationship('Medication', back_populates='doctor')
    prescriptions = relationship('Prescription', back_populates='doctor')
