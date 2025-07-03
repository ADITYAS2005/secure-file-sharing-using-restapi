from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import List

class RoleEnum(str, Enum):
    ops = "ops"
    client = "client"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: RoleEnum

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class FileOut(BaseModel):
    id: int
    filename: str
    created_at: str

    class Config:
        orm_mode = True
