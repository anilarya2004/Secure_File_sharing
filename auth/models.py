from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str  # 'ops' or 'client'

class UserLogin(BaseModel):
    email: EmailStr
    password: str
