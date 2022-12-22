from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator, constr, Field


class UserBase(BaseModel):
    email: EmailStr
    name: str
    is_company: bool
    is_active: bool


class UserIn(UserBase):
    id: int
    hashed_password: str
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class UserOut(UserBase):
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: constr(min_length=8)
    confirmed_password: str

    @validator("confirmed_password")
    def match_passwords(cls, password, values, **kwargs):
        if "password" in values and values["password"] != password:
            raise ValueError("Wrong password")
        return password

    class Config:
        orm_mode = True
