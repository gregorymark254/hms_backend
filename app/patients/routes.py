from fastapi import Depends
from sqlalchemy.orm import Session

from . import router, models
from ..patients import schemas
from ..users.models import get_current_user
from ..utils.database import get_db
from ..utils.pagination import Pagination, Paginator


@router.get('/', response_model=schemas.ListPatients, dependencies=[Depends(get_current_user)])
async def get_patients(db: Session = Depends(get_db), pagination: Paginator = Depends()):
    query = db.query(models.Patient)
    total = query.count()
    patients = query.offset(pagination.offset).limit(pagination.offset).all()
    count = len(patients)
    return Pagination(items=patients, total=total, count=count)
