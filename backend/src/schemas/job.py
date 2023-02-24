from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, constr
from datetime import datetime

from schemas.user import UserOut


class JobCategory(str, Enum):
    finance = 'Finance'
    marketing = 'Marketing'
    agro = 'Agriculture'
    it = 'IT'
    metallurgy = 'Metallurgy'
    medicine = 'Medicine'
    construction = 'Construction'
    building = 'Building'
    services = 'Services'
    miscellaneous = 'Miscellaneous'


class JobCreate(BaseModel):
    email: EmailStr
    title: constr(min_length=1)
    description: constr(min_length=1)
    salary_from: int = Field(..., gt=0)
    salary_to: int = Field(..., gt=0)


class JobUpdate(BaseModel):
    email: Optional[EmailStr]
    title: Optional[constr(min_length=1)]
    description: Optional[constr(min_length=1)]
    salary_from: Optional[int] = Field(gt=0)
    salary_to: Optional[int] = Field(gt=0)


class JobOut(JobCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    category: JobCategory

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda date: date.isoformat()[:-3] + 'Z'
        }


class JobDetail(JobOut):
    user: UserOut


class JobApplied(JobOut):
    appliers: Optional[List[UserOut]]
