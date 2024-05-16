from typing import Optional
from datetime import datetime
from http import HTTPStatus

from pydantic import (Field, NonNegativeInt, StrictBool, BaseModel,
                      root_validator, validator)
from fastapi import HTTPException


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(..., min_length=1)
    full_amount: Optional[NonNegativeInt] = Field(..., )

    @validator('full_amount')
    def check_full_amount(cls, value):
        if value is not None and (not isinstance(value, int) or value <= 0):
            raise ValueError(
                'сумма пожертвования должна быть целочисленной и больше 0')
        return value


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: Optional[NonNegativeInt]


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[NonNegativeInt]
    invested_amount: Optional[NonNegativeInt]
    create_date: Optional[datetime]
    close_date: Optional[datetime]
    fully_invested: Optional[StrictBool]

    # TODO Сделать с этим что-нибудь
    # @validator('invested_amount')
    # def check_from_reserve_before_to_reserve(cls, value):
    #     invested_amount = value.get('invested_amount')
    #     print(invested_amount)
    #     if invested_amount is not None:
    #         raise HTTPException(
    #             status_code=HTTPStatus.BAD_REQUEST,
    #             detail='Никто не может менять размер внесённых средств')
    #     return value


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: NonNegativeInt = Field(..., example=0, )
    fully_invested: StrictBool = Field(..., example=False)
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
