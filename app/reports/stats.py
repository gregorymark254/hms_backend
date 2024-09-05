from collections import Counter
from datetime import date

from fastapi import Depends
from sqlalchemy.orm import Session

from . import router, schemas
from ..utils.database import get_db
from ..users import models


@router.get('/stats', response_model=schemas.ReportSchema)
async def get_stats(start_date: date | None = None, end_date: date | None = None, db: Session = Depends(get_db)):
    query = db.query(models.User)

    if start_date:
        query = query.filter(models.User.createdAt >= start_date)

    if end_date:
        query = query.filter(models.User.createdAt <= end_date)

    users = query.all()

    count = Counter()
    for user in users:
        month = user.createdAt.strftime('%Y-%m-%d')
        count[month] += 1

    result = [schemas.Reports(month=month, count=count) for month, count in count.items()]

    return schemas.ReportSchema(items=result)