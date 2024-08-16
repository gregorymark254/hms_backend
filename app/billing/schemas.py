from datetime import datetime

from pydantic import BaseModel


class AddBilling(BaseModel):
    amount: int
    billingDate: datetime
    status: str
    patientId: int