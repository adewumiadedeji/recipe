import os
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from utils.database import Base



class Recipe(Base):
    __tablename__ = "recipes"
    __allow_unmapped__ = True
    __table_args__ = {"schema": os.getenv("MYSQL_DB", "recipe_db")}  # Use default if env var is missing
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), index=True, nullable=False)
    description = Column(Text, nullable=True)
    instructions = Column(Text, nullable=False)
    user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    

    
class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"
    __table_args__ = {"schema": os.getenv("MYSQL_DB", "recipe_db")}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_id = Column(Integer, nullable=False)
    ingredient_id = Column(Integer, nullable=False)
    quantity = Column(Integer)
    
