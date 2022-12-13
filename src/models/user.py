import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator, constr


class User(BaseModel):
    id: Optional[str]
    email: EmailStr
    name: str
    hashed_password: str
    is_company: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserIn(BaseModel):
    email: EmailStr
    name: str
    password: constr(min_length=8)
    confirmed_password: str
    is_company: bool

    @validator("confirmed_password")
    def match_passwords(cls, password, fields, **kwargs):
        if "password" in fields and fields["password"] != password:
            raise ValueError("Wrong password")
        return password
