from datetime import datetime
import os
from typing import Optional
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from utils.database import Base


class User(Base):
    __tablename__ = "users"
    __allow_unmapped__ = True
    __table_args__ = {"schema": os.getenv("MYSQL_DB", "recipe_db")}
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(200), unique=True, index=True)
    name = Column(String(200))
    hashed_password = Column(String(200))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    
class UserInDB(User):
    hashed_password: str
    

class UserUpdate(User):
    email: Optional[str] = None
    name: Optional[str] = None
    is_active: Optional[bool] = True

