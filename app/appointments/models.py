import enum
from datetime import datetime

from sqlalchemy import Column, Date, Integer, Text, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.utils.database import Base


class AppointmentEnums(enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    canceled = "canceled"


class Appointment(Base):
    __tablename__ = 'appointments'
    appointmentId = Column(Integer, primary_key=True, autoincrement=True)
    appointmentDate = Column(Date, nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(Enum(AppointmentEnums), default=AppointmentEnums.pending, nullable=False)
    patientId = Column(Integer, ForeignKey('patients.patientId'), nullable=False, index=True)
    doctorId = Column(Integer, ForeignKey('doctors.doctorId'), nullable=False, index=True)
    createdAt = Column(DateTime, nullable=False, default=datetime.utcnow())

    patient = relationship('Patient', back_populates='appointments', lazy='joined')
    doctor = relationship('Doctor', back_populates='appointments', lazy='joined')

    def to_json(self):
        patient_name = self.patient.firstName + " " + self.patient.lastName if self.patient else None
        doctor_name = self.doctor.firstName + " " + self.doctor.lastName if self.doctor else None

        return {
            'appointmentId': self.appointmentId,
            'appointmentDate': self.appointmentDate,
            'reason': self.reason,
            'status': self.status,
            'patientId': self.patientId,
            'patient_name': patient_name,
            'doctor_name': doctor_name,
            'doctorId': self.doctorId,
            'createdAt': self.createdAt,
        }
