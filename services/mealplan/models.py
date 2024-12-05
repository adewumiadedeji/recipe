from datetime import datetime
import os
from sqlalchemy import Column, Integer, DateTime, Date, DateTime, Enum
import enum
from utils.database import Base


class MealType(enum.Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    snack = "snack"
    
    
class MealPlan(Base):
    __tablename__ = "meal_plans"
    __allow_unmapped__ = True
    __table_args__ = {"schema": os.getenv("MYSQL_DB", "recipe_db")} 

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    meal_type = Column(Enum(MealType), nullable=False)
    
    user_id = Column(Integer, nullable=False)
    recipe_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


    