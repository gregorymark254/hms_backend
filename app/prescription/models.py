from sqlalchemy import Column, Integer, String, Date, DateTime
from datetime import datetime


from app.utils.database import Base


class Prescription(Base):
    __tablename__ = 'prescription'
    prescriptionId = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    prescriptionName = Column(String(50), nullable=False)
    dosage = Column(String(50), nullable=False)
    instructions = Column(String(50), nullable=False)
    duration = Column(String(10), nullable=False)
    createdAt = Column(DateTime, nullable=False, default=datetime.utcnow())
