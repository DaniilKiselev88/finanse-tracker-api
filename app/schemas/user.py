from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional
import re

# Валидатор для телефона
def validate_phone_format(v: str) -> str:
    if v is None:
        return v
    v = re.sub(r"[\s\-\(\)]", "", v)
    if not re.match(r"^(\+7|8)\d{10}$", v):
        raise ValueError("Неверный формат номера. Используй +7XXXXXXXXXX или 8XXXXXXXXXX")
    if v.startswith("8"):
        v = "+7" + v[1:]
    return v

class UserCreate(BaseModel):
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    password: str = Field(..., min_length=6)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        return validate_phone_format(v)

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    phone: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str