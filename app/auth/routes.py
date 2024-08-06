from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from . import router, schemas
from ..users import models
from ..utils.database import get_db


@router.post('/')
def register():
    pass


@router.post('/', response_model=schemas.AuthToken)
def login(auth: schemas.AuthSchema, db: Session = Depends(get_db)):
    pass