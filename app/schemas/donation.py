from typing import Optional
from datetime import datetime

from pydantic import Field, NonNegativeInt, StrictBool, BaseModel


class DonationCreate(BaseModel):
    full_amount: NonNegativeInt = Field(..., example=10)
    comment: Optional[str] = Field(..., example="For cats!!!")


class DonationDB(DonationCreate):
    id: int
    full_amount: int
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class DonationDBSuperuser(DonationCreate):
    id: int
    full_amount: int
    create_date: datetime
    close_date: Optional[datetime]
    user_id: int
    invested_amount: NonNegativeInt
    fully_invested: StrictBool

    class Config:
        orm_mode = True
