from datetime import datetime
import os
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Ingredient(Base):
    __tablename__ = "ingredients"
    __allow_unmapped__ = True
    __table_args__ = {"schema": os.getenv("MYSQL_DB", "recipe_db")}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    unit = Column(String(10))
    amount = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
