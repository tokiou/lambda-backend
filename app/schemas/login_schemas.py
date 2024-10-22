
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserLogin(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: Optional[str] = None