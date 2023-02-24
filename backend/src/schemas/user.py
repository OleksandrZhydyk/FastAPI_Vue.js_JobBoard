from datetime import datetime
from typing import Optional, List

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, validator, constr

# from schemas.job import JobOut


class UserBase(BaseModel):
    email: EmailStr
    name: constr(min_length=1)


class UserOut(UserBase):
    id: int
    is_company: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda date: str(date)[:-3] + 'Z'
        }


class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    is_company: Optional[bool]
    name: Optional[constr(min_length=1)]
    password: Optional[constr(min_length=8)]

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda date: str(date)[:-3] + 'Z'
        }

    @validator("name")
    def validate_name(cls, name):
        if name.isalpha():
            return name
        raise HTTPException(
            status_code=422, detail="Name should contains only letters"
        )



class UserCreate(UserBase):
    is_company: bool
    password: constr(min_length=8)
    confirmed_password: str

    @validator("confirmed_password")
    def match_passwords(cls, password, values, **kwargs):
        if "password" in values and values["password"] != password:
            raise ValueError("Please enter the same value for password and confirmed password field")
        return password

    class Config:
        orm_mode = True


# class CompanyJobsSchema(UserOut):
#     jobs: List[JobOut]

class UserInDB(UserOut):
    hashed_password: str
