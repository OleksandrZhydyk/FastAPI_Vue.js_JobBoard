from typing import List

from fastapi import APIRouter

from models.user import User

router = APIRouter()


@router.get("/", response_model=List[User])
async def read_users(limit: int = 100, skip: int = 100):
    return {}
