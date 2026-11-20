from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserRegister(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=6, max_length=30)
    password: str = Field(..., min_length=6, max_length=100)
    confirm_password: str
    address: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserProfileUpdate(BaseModel):
    full_name: str
    phone: str
    address: Optional[str] = None

class ChangePassword(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=6)
    confirm_new_password: str
