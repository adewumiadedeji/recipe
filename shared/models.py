from datetime import datetime
import os
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Text, ForeignKey, DateTime, Enum
from pydantic import BaseModel, EmailStr
from typing import Optional
from .database import Base, engine
from sqlalchemy.orm import relationship
import enum


class MealType(enum.Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    snack = "snack"


class User(Base):
    __tablename__ = "users"
    __allow_unmapped__ = True
    __table_args__ = {"schema": os.getenv("MYSQL_DB") or 'recipe_db', 'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(200), unique=True, index=True)
    name = Column(String(200))
    hashed_password = Column(String(200))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    
class Recipe(Base):
    __tablename__ = "recipes"
    __allow_unmapped__ = True
    __table_args__ = {"schema": os.getenv("MYSQL_DB", "recipe_db")}  # Use default if env var is missing
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), index=True, nullable=False)
    description = Column(Text, nullable=True)
    instructions = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('recipe_db.users.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    ingredients = relationship("RecipeIngredient", back_populates="recipe")

    
class Ingredients(Base):
    __tablename__ = "ingredients"
    __table_args__ = {"schema": os.getenv("MYSQL_DB", "recipe_db")}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), index=True, nullable=False)
    description = Column(Text, nullable=True)
    unit = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    
class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"
    __table_args__ = {"schema": os.getenv("MYSQL_DB", "recipe_db")}
    
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id", ondelete="CASCADE"), primary_key=True)
    quantity = Column(Integer)
    
    recipe = relationship("Recipe", back_populates="ingredients")
    
    
    

class MealPlan(Base):
    __tablename__ = "meal_plans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    meal_type = Column(Enum(MealType), nullable=False)
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Optional: Add relationships if you need to access related data
    recipe = relationship("Recipe", backref="meal_plans")
    
    

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    
    
class EmailRequest(BaseModel):
    recipient: EmailStr
    subject: str
    body: str
    
# _db.Base.metadata.create_all(bind=_db.engine)