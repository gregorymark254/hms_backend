import os
from datetime import datetime, timedelta
import enum

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import Session

from app.users import oauth2_scheme
from app.utils.database import Base, get_db

SECRET_KEY = os.getenv('SECRET_KEY')


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
    password_hash = Column(String(255), nullable=False)
    createdAt = Column(DateTime, nullable=False, default=datetime.utcnow())

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, raw_password: str):
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
        self.password_hash = hashed_password.decode('utf-8')

    def check_password(self, password) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))


# create jwt access token
def create_access_token(user: User):
    return jwt.encode({
        "exp": datetime.utcnow() + timedelta(hours=3),
        'userId': user.userId,
        'role': user.role.value,
    }, SECRET_KEY, algorithm='HS256')


# decode the jwt access token to get userId
def load_user_from_access_token(token, db):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        userId = data.get('userId')
        return db.query(User).filter_by(userId=userId).first()
    except Exception:
        return None


# get the current logged-in user from the jwt token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    user = load_user_from_access_token(token, db)
    if not user:
        raise HTTPException(status_code=401, detail='You are not authenticated or Invalid Token')
    return user


# get user role from the jwt and give access to admin routes
def require_admin(current_user: User = Depends(get_current_user)):
    if not current_user or current_user.role.value != 'admin':
        raise HTTPException(status_code=403, detail="Unauthorized! Admin Only")
