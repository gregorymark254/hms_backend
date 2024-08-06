from pydantic import BaseModel


class AuthSchema(BaseModel):
    email: str
    password: str


class UserDetails(BaseModel):
    firstName: str
    lastName: str
    email: str


class AuthToken(BaseModel):
    access_token: str

