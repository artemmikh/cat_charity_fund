from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, validator, NonNegativeInt, StrictBool


class CharityProjectBase(BaseModel):
    # TODO запилить SchemasBaseModel
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: NonNegativeInt = Field(..., )
    invested_amount: NonNegativeInt = Field(..., example=0, )


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectBase):
    id: int
    create_date: datetime
    close_date: datetime
    fully_invested: StrictBool = Field(..., example=False)

    class Config:
        orm_mode = True
