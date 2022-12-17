from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator, constr, Field


class UserBase(BaseModel):
    email: EmailStr
    name: str
    is_company: bool


class User(UserBase):
    id: Optional[str]
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class UserCreate(UserBase):
    password: constr(min_length=8)
    confirmed_password: str

    @validator("confirmed_password")
    def match_passwords(cls, password, values, **kwargs):
        if "password" in values and values["password"] != password:
            raise ValueError("Wrong password")
        return password
