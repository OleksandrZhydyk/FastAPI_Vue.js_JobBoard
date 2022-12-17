import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator, constr


class UserBase(BaseModel):
    email: EmailStr
    name: str
    is_company: bool


class User(UserBase):
    id: Optional[str]
    hashed_password: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserCreate(UserBase):
    password: constr(min_length=8)
    confirmed_password: str

    # @validator("confirmed_password")
    # def match_passwords(cls, value, fields, **kwargs):
    #     if "password" in fields and fields["password"] != value:
    #         raise ValueError("Wrong password")
    #     return value
