from datetime import datetime
import enum

import bcrypt
from sqlalchemy import Column, Integer, String, Enum, DateTime

from app.utils.database import Base


class Role(enum.Enum):
    admin = 'admin'
    doctor = 'doctor'
    patient = 'patient'
    pharmacy = 'pharmacy'


class User(Base):
    __tablename__ = 'users'
    userId = Column(Integer, primary_key=True, autoincrement=True)
    firstName = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)
    role = Column(Enum(Role), nullable=False, default=Role.patient)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    createdAt = Column(DateTime, nullable=False, default=datetime.utcnow())

    @property
    def hash_password(self):
        return self.password

    @hash_password.setter
    def hash_password(self, password: str):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.password = hashed_password.decode('utf-8')

    def verify_password(self, password: str):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))