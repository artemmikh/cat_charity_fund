from typing import Optional
from datetime import datetime
from http import HTTPStatus

from pydantic import (Field, NonNegativeInt, StrictBool, BaseModel,
                      root_validator)
from fastapi import HTTPException


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(..., min_length=1)
    full_amount: Optional[NonNegativeInt] = Field(..., )


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: Optional[NonNegativeInt]


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[NonNegativeInt]

    # TODO может пригодиться если надо будет выкидывать ошибку
    #  код ниже не работает, потому что поле игнорируется
    # @root_validator(skip_on_failure=True)
    # def check_from_reserve_before_to_reserve(cls, values):
    #     invested_amount = values.get('invested_amount')
    #     print(invested_amount)
    #     if invested_amount is not None:
    #         raise HTTPException(
    #             status_code=HTTPStatus.BAD_REQUEST,
    #             detail='Никто не может менять размер внесённых средств')
    #     return values


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: NonNegativeInt = Field(..., example=0, )
    fully_invested: StrictBool = Field(..., example=False)
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
