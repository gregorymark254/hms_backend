from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from . import router, schemas, models
from .models import get_current_user, get_admin
from ..utils.database import get_db
from ..utils.pagination import Pagination, Paginator


@router.get('/', response_model=schemas.ListUsers, dependencies=[Depends(get_admin)])
async def get_users(email:str | None = None, db: Session = Depends(get_db), pagination: Paginator = Depends()):
    query = db.query(models.User)

    if email:
        query = query.filter_by(email=email)

    total = query.count()
    users = query.offset(pagination.offset).limit(pagination.limit).all()
    count = len(users)
    return Pagination(items=users, total=total, count=count)


@router.post('/', response_model=schemas.Users, dependencies=[Depends(get_admin)])
async def add_user(user: schemas.AddUser, db: Session = Depends(get_db)):
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/me', response_model=schemas.Users, dependencies=[Depends(get_current_user)])
async def get_current_user_details(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.get('/{userId}', response_model=schemas.Users, dependencies=[Depends(get_admin)])
async def get_user_by_id(userId: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(userId=userId).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return user


@router.put('/{userId}', dependencies=[Depends(get_admin)])
async def update_user(userId: int, request: schemas.UpdateUser, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(userId=userId).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.firstName = request.firstName
    user.lastName = request.lastName
    user.role = request.role

    db.commit()
    db.refresh(user)
    return {'message': f'User {user.email} has been updated.'}
