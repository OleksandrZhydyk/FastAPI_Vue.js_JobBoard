from datetime import datetime
from typing import Optional, List

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, validator, constr


class UserBase(BaseModel):
    email: EmailStr


class UserOut(UserBase):
    id: int
    is_company: bool
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    avatar: Optional[str] = None
    resume: Optional[str] = None
    name: Optional[constr(min_length=1)] = None

    class Config:
        orm_mode = True
        json_encoders = {datetime: lambda date: str(date)[:-3] + "Z"}


class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    name: Optional[constr(min_length=2)]
    password: Optional[constr(min_length=8)]

    class Config:
        orm_mode = True
        json_encoders = {datetime: lambda date: str(date)[:-3] + "Z"}

    @validator("name")
    def validate_name(cls, name):
        if name:
            if name.isalpha():
                return name
            raise HTTPException(status_code=422, detail="Name should contains only letters")
        return name


class UserUpdateSuperuser(UserUpdate):
    is_company: bool
    is_active: bool

class UserResponse(UserOut):
    vacancies: Optional[List]


class UserCreate(UserBase):
    is_company: bool = False
    password: constr(min_length=8)
    confirmed_password: str

    @validator("confirmed_password")
    def match_passwords(cls, password, values, **kwargs):
        if "password" in values and values["password"] != password:
            raise ValueError(
                "Please enter the same value for password and confirmed password field"
            )
        return password

    class Config:
        orm_mode = True


class UserInDB(UserOut):
    hashed_password: str
