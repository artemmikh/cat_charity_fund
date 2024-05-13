from typing import Optional
from datetime import datetime

from pydantic import Field, NonNegativeInt, StrictBool

from app.schemas.base import SchemasBaseModel


class CharityProjectCreate(SchemasBaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)


class CharityProjectUpdate(SchemasBaseModel):
    pass


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: NonNegativeInt = Field(..., example=0, )
    fully_invested: StrictBool = Field(..., example=False)
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
