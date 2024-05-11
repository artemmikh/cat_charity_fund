from pydantic import BaseModel, Field, NonNegativeInt


class SchemasBaseModel(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: NonNegativeInt = Field(..., )
