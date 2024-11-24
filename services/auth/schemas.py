import re

import datetime
from pydantic import BaseModel, validator



class UserBase(BaseModel):
    name: str
    email: str
    
    @validator('email')
    def email_must_be_valid(cls, v):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise ValueError('Email must be at least 3 characters long')        
        return v
    
    class Config:
       from_attributes=True

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def password_must_be_valid(cls, v):
        SpecialSym =['$', '@', '#', '%']
     
        if len(v) < 6:
            raise ValueError('length should be at least 6')
            
        if len(v) > 20:
            raise ValueError('length should be not be greater than 8')
            
        if not any(char.isdigit() for char in v):
            raise ValueError('Password should have at least one numeral')
            
        if not any(char.isupper() for char in v):
            raise ValueError('Password should have at least one uppercase letter')
            
        if not any(char.islower() for char in v):
            raise ValueError('Password should have at least one lowercase letter')
            
        if not any(char in SpecialSym for char in v):
            raise ValueError('Password should have at least one of the symbols $@#')
        
        return v
    class Config:
       from_attributes=True

class User(UserBase):
    id: int
    created_at: datetime.datetime
    class Config:
       from_attributes=True


class GenerateUserToken(BaseModel):
    email: str
    password: str
    
    @validator('email')
    def email_must_be_valid(cls, v):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise ValueError('Email must be at least 3 characters long')        
        return v
    
    class Config:
        from_attributes=True


class GenerateOtp(BaseModel):
    email: str
    
class VerifyOtp(BaseModel):
    email: str
    otp: int