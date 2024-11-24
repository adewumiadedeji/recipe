import datetime
from typing import List
from pydantic import BaseModel, validator

class RateCreate(BaseModel):
    recipe_id: int
    rate: int

    @validator('rate')
    def rate_must_be_valid(cls, v):
        if v < 1 or v > 10:
            raise ValueError('Rate should be between the scale of 1 to 10')
        return v

    
    
class Rate(RateCreate):
    id: int
    created_at: datetime.datetime
    
    class Config:
        from_attributes=True

class Rating(BaseModel):
    recipe_id: int
    rate: int
    id: int
    created_at: datetime.datetime
    
class Recipe(BaseModel):
    id: int
    title: str
    description: str
    instructions: str
    created_at: datetime.datetime
    
    
class RateResponse(Recipe):
    mean_rating: float
    ratings: List[Rating]  # List of Rating objects
    
