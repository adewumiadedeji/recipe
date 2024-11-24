import datetime
from pydantic import BaseModel, validator

class IngredientCreate(BaseModel):
    name: str
    unit: str
    amount: float

    @validator('name')
    def name_must_be_valid(cls, v):
        if v is None:
            raise ValueError('Name must be at least 1 characters long')
        return v

    # @validator('unit')
    # def unit_must_be_valid(cls, v):
    #     if v is None:
    #         raise ValueError('Name must be at least 1 characters long')
    #     return v
    
    # @validator('amount')
    # def amount_must_be_valid(cls, v):
    #     if v < 0.0:
    #         raise ValueError('Amount must be greater than 0')
    #     return v
    
class Ingredient(IngredientCreate):
    id: int
    created_at: datetime.datetime
    class Config:
       from_attributes=True