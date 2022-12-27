from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class JobCreate(BaseModel):
    email: EmailStr
    user_id: int
    title: str
    description: str
    is_active: bool
    salary_from: int = Field(..., gt=0)
    salary_to: int = Field(..., gt=0)


class JobOut(JobCreate):
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda date: date.isoformat()[:-3] + 'Z'
        }
