from pydantic import BaseModel

class Reports(BaseModel):
    month: str
    count: int

class ReportSchema(BaseModel):
    items: list[Reports]