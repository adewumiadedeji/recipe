import datetime
from pydantic import BaseModel, validator
from typing import List, Optional

class RecipeCreate(BaseModel):
    title: str
    description: Optional[str]
    instructions: str
    # ingredients: List[int]

    @validator('title')
    def title_must_be_valid(cls, v):
        if len(v) < 3:
            raise ValueError('Title must be at least 3 characters long')
        if len(v) > 100:
            raise ValueError('Title must not exceed 100 characters')
        return v

    @validator('instructions')
    def instructions_must_be_detailed(cls, v):
        if len(v) < 50:
            raise ValueError('Instructions must be at least 50 characters long')
        return v
    
class Recipe(RecipeCreate):
    id: int
    created_at: datetime.datetime
    class Config:
        from_attributes=True
        
        
class Ingredient(BaseModel):
    id: int
    name: str
    
class RecipeResponse(RecipeCreate):
    id: int
    ingredients: List[Ingredient]