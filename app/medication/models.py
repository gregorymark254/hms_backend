from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.utils.database import Base


class Medication(Base):
    __tablename__ = 'medication'
    medicationId = Column(Integer, primary_key=True, autoincrement=True)
    diagnosis = Column(String(255), nullable=False)
    treatment = Column(String(255), nullable=False)
    notes = Column(String(255), nullable=False)
    patientId = Column(Integer, ForeignKey('patients.patientId'), nullable=False, index=True)
    prescriptionId = Column(Integer, ForeignKey('prescription.prescriptionId'), nullable=False, index=True)
    createdAt = Column(DateTime, default=datetime.utcnow())

    patient = relationship('Patient', back_populates='medications', lazy='joined')
    prescription = relationship('Prescription', back_populates='medications', lazy='joined')

    def to_json(self):
        patient_name = self.patient.firstName + " " + self.patient.lastName if self.patient else None

        return {
            'medicationId': self.medicationId,
            'diagnosis': self.diagnosis,
            'treatment': self.treatment,
            'notes': self.notes,
            'patientId': self.patientId,
            'patient_name': patient_name,
            'prescriptionId': self.prescriptionId,
            'prescriptionName': self.prescription.prescriptionName,
            'createdAt': self.createdAt
        }