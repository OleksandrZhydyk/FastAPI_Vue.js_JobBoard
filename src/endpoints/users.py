from typing import List, Optional

from fastapi import APIRouter, Depends

from src.db.repositories.users import UsersService, get_users_service
from src.schemas.user import UserCreate, UserOut, UserIn, UserBase

router = APIRouter()


@router.post("/", response_model=UserOut)
async def create_user(obj: UserCreate, user_service: UsersService = Depends(get_users_service)) -> UserOut:
    user = await user_service.create(obj)
    return user


@router.get("/", response_model=List[UserOut])
async def get_users(user_service: UsersService = Depends(get_users_service),) -> Optional[List[UserOut]]:
    users = await user_service.get_all()
    return [user for user in users]


