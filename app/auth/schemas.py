from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator
from ..users.models import Role, User
from ..utils.database import get_db_context


class AuthSchema(BaseModel):
    email: str
    password: str


class RegisterSchema(BaseModel):
    firstName: str
    lastName: str
    email: str
    role: Role = Field(Role.patient, alias='role')
    password: str = Field(..., min_length=8)

    @field_validator('email')
    def validate_email(cls, email):
        with get_db_context() as db:
            if db.query(User).filter_by(email=email).first() is not None:
                raise HTTPException(status_code=400, detail=f'Email {email} already exist')


class UserDetails(BaseModel):
    firstName: str
    lastName: str
    email: str
    role: str


class AuthToken(BaseModel):
    access_token: str
    user_data: UserDetails

