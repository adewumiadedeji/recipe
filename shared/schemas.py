from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
import re

class ErrorResponse(BaseModel):
    detail: str
    code: str

class HealthCheck(BaseModel):
    status: str
    version: str
    dependencies: dict