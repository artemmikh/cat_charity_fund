from pydantic import BaseModel, Field, NonNegativeInt


class SchemasBaseModel(BaseModel):
    # TODO выпилить базовую модель
    full_amount: NonNegativeInt = Field(..., )
