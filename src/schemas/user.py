from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, validator, constr, Field


class UserBase(BaseModel):
    email: EmailStr
    name: str
    is_company: bool


class UserIn(UserBase):
    id: int
    hashed_password: str
    is_active: bool
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True


class UserOut(UserBase):
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: constr(min_length=8)
    confirmed_password: str

    @validator("confirmed_password")
    def match_passwords(cls, password, values, **kwargs):
        if "password" in values and values["password"] != password:
            raise ValueError("Please enter the same value for password and confirmed password field")
        return password

    class Config:
        orm_mode = True
