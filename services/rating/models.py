from datetime import datetime
import os
from typing import List
from sqlalchemy import Column, Integer, DateTime, Date, DateTime, Enum
import enum
from utils.database import Base


class Rating(Base):
    __tablename__ = "ratings"
    __allow_unmapped__ = True
    __table_args__ = {"schema": os.getenv("MYSQL_DB", "recipe_db")} 

    id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_id = Column(Integer, nullable=False)
    rate = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


