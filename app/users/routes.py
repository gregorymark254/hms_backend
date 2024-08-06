from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from . import router, schemas, models
from ..utils.database import get_db


@router.get('/', response_model=schemas.ListUsers)
def get_users(db: Session = Depends(get_db)):
    query = db.query(models.User)
    users = query.all()
    return {"users": users}


@router.post('/', response_model=schemas.Users)
def add_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{userId}', response_model=schemas.Users)
def get_user_by_id(userId: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.userId == userId).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return user
