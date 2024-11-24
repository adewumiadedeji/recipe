import datetime
from pydantic import BaseModel, validator
from models import MealType
import enum
from datetime import date

class MealCreate(BaseModel):
    date: str
    meal_type: MealType
    recipe_id: int

    # @validator('meal_type')
    # def name_must_be_valid(cls, v):
    #     if not v in {meal.value for meal in MealType}:
    #         raise ValueError('Meal type can either be breakfast, lunch, dinner, or snack')
    #     return v

    
    
class Meal(MealCreate):
    id: int
    date: date
    created_at: datetime.datetime
    user_id: int
    
    class Config:
       from_attributes=True