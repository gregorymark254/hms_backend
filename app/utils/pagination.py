from fastapi import Query

from pydantic import BaseModel


class Paginator(BaseModel):
    offset: int = Query(0, ge=0)
    limit: int = Query(50, ge=1, le=100)


class Pagination:
    def __init__(self, offset: int = 0, limit: int = 20, total: int = 0, count: int = 0, items: list = None):
        self.offset = offset
        self.limit = limit
        self.items = items
        self.total = total
        self.count = count
