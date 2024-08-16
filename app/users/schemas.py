from datetime import datetime

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator

from app.users.models import Role, User
from app.utils.database import get_db_context


class AddUser(BaseModel):
    firstName: str
    lastName: str
    email: str
    role: Role = Field(Role.reception, alias='role')
    password: str = Field(..., min_length=8)

    @field_validator('email')
    def validate_email(cls, email):
        with get_db_context() as db:
            if db.query(User).filter_by(email=email).first() is not None:
                raise HTTPException(status_code=400, detail=f'Email {email} already exist')
        return email


class Users(BaseModel):
    userId: int
    firstName: str
    lastName: str
    role: str
    email: str
    createdAt: datetime


class UpdateUser(BaseModel):
    firstName: str
    lastName: str
    role: str


class ListUsers(BaseModel):
    items: list[Users]
    total: int
    count: int
