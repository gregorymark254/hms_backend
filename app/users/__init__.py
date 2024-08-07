from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/docs-login')

from . import routes