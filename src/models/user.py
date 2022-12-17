from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator, constr, Field


class User(BaseModel):
    id: Optional[str]
    email: EmailStr
    name: str
    hashed_password: str
    is_company: bool
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class UserIn(BaseModel):
    email: EmailStr
    name: str
    password: constr(min_length=8)
    confirmed_password: str
    is_company: bool

    @validator("confirmed_password")
    def match_passwords(cls, password, values, **kwargs):
        if "password" in values and values["password"] != password:
            raise ValueError("Wrong password")
        return password
