from sqlalchemy import Column, Integer, String, Date, DateTime, func

from app.utils.database import Base


class Patient(Base):
    __tablename__ = 'patients'
    patientId = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    firstName = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)
    dateOfBirth = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    address = Column(String(20), nullable=False)
    phoneNumber = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    emergencyNumber = Column(String(20), nullable=False)
    insuranceNumber = Column(String(20), nullable=False)
    insuranceName = Column(String(50), nullable=False)
    createdAt = Column(DateTime, nullable=False, default=func.now())
