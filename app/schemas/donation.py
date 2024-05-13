from typing import Optional
from datetime import datetime

from pydantic import Field, NonNegativeInt, StrictBool

from app.schemas.base import SchemasBaseModel


class DonationCreate(SchemasBaseModel):
    comment: str = Field(..., example="Donation")


class DonationUpdate(SchemasBaseModel):
    pass


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
