from typing import List, Optional

from fastapi import APIRouter, Depends

from src.db.repositories.users import UsersService, get_users_service
from src.schemas.user import UserCreate, UserOut, UserIn, UserBase

router = APIRouter()


@router.post("/", response_model=UserOut)
async def create_user(obj: UserCreate, user_service: UsersService = Depends(get_users_service)) -> UserOut:
    return await user_service.create(obj)


@router.get("/", response_model=List[UserOut])
async def get_users(user_service: UsersService = Depends(get_users_service),) -> Optional[List[UserOut]]:
    return await user_service.get_all()


@router.get("/{pk}", response_model=UserOut)
async def get_one(pk: int, user_service: UsersService = Depends(get_users_service)) -> Optional[UserOut]:
    return await user_service.get_one(pk)


@router.put("/{pk}", response_model=UserOut)
async def update_user(obj: UserOut, pk: int, user_service: UsersService = Depends(get_users_service)) -> UserOut:
    return await user_service.update(pk, obj)


@router.delete("/{pk}", response_model=bool)
async def delete_user(pk: int, user_service: UsersService = Depends(get_users_service)) -> bool:
    return await user_service.delete(pk)
