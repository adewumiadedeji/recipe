import enum
from typing import Optional
from pydantic import BaseModel

class GenerateUserToken(BaseModel):
    email: str
    password: str

class UserCredentials(BaseModel):
    email: str
    password: str

class UserRegisteration(BaseModel):
    name: str
    email: str
    password: str

class GenerateOtp(BaseModel):
    email: str

class VerifyOtp(BaseModel):
    email: str
    otp: int
    
    
class RecipeCreate(BaseModel):
    title: str
    description: Optional[str]
    instructions: str
    # ingredients: List[int]
    
class IngredientCreate(BaseModel):
    name: str
    unit: str
    amount: float
    
class MealType(enum.Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    snack = "snack"
    
class MealCreate(BaseModel):
    date: str
    meal_type: MealType
    recipe_id: int
    
    
class RateCreate(BaseModel):
    recipe_id: int
    rate: int