from datetime import datetime

from pydantic import BaseModel, Field

from app.users.models import Role
from app.utils.pagination import Paginator


class AddUser(BaseModel):
    firstName: str
    lastName: str
    email: str
    role: Role = Field(Role.patient, alias='role')
    password: str = Field(..., min_length=8)


class Users(BaseModel):
    userId: int
    firstName: str
    lastName: str
    role: str
    email: str
    createdAt: datetime


class ListUsers(Paginator):
    items: list[Users]
    total: int
    count: int
