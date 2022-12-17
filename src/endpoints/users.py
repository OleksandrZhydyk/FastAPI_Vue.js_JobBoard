from fastapi import APIRouter

from src.models.user import User

router = APIRouter()


@router.get("/", response_model=list[User])
async def read_users(limit: int = 100, skip: int = 100):
    return {}
