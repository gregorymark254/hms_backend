from pydantic import BaseModel, Field
from ..users.models import Role


class AuthSchema(BaseModel):
    email: str
    password: str


class RegisterSchema(BaseModel):
    firstName: str
    lastName: str
    email: str
    role: Role = Field(Role.patient, alias='role')
    password: str = Field(..., min_length=8)


class UserDetails(BaseModel):
    firstName: str
    lastName: str
    email: str
    role: str


class AuthToken(BaseModel):
    access_token: str
    user_data: UserDetails

