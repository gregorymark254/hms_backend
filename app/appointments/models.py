import enum
from datetime import datetime

from sqlalchemy import Column, Date, Integer, Text, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.utils.database import Base


class AppointmentEnum(enum.Enum):
    pending = "pending"
    confirmed = "confirmed"


class Appointment(Base):
    __tablename__ = 'appointments'
    appointmentId = Column(Integer, primary_key=True, autoincrement=True)
    appointmentDate = Column(Date, nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(Enum(AppointmentEnum), default=AppointmentEnum.pending)
    patientId = Column(Integer, ForeignKey('patients.patientId'), nullable=False, unique=True, index=True)
    doctorId = Column(Integer, ForeignKey('doctors.doctorId'), nullable=False, unique=True, index=True)
    createdAt = Column(DateTime, nullable=False, default=datetime.utcnow())

    patient = relationship("Patient", back_populates="appointment")
    doctor = relationship("Doctor", back_populates="appointment")
