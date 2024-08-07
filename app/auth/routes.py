from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import router, schemas
from ..users.models import User, create_access_token
from ..utils.database import get_db
from ..users import models


def get_access_token(email: str, password: str, db: Session):
    user: User | None = db.query(User).filter_by(email=email).first()
    if user and user.check_password(password):
        return {
            'access_token': create_access_token(user),
            'user_data': {
                'firstName': user.firstName,
                'lastName': user.lastName,
                'email': user.email,
                'role': user.role
            }
        }

    raise HTTPException(status_code=404, detail='Incorrect email or password')


@router.post('/', response_model=schemas.AuthToken)
def login(request: schemas.AuthSchema, db: Session = Depends(get_db)):
    return get_access_token(request.email, request.password, db)


@router.post('/register')
def register(request: schemas.RegisterSchema, db: Session = Depends(get_db)):
    user = models.User(**request.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return {'message': f'User {user.email} registered successfully'}


@router.post('/docs-login', response_model=schemas.AuthToken, include_in_schema=False)
def docs_login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return get_access_token(request.username, request.password, db)

