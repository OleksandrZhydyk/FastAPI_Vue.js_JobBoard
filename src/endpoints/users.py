from typing import List, Optional

from fastapi import APIRouter, Depends

from src.core.security import get_current_user, get_current_active_user, check_company_credentials, \
    check_superuser_credentials
from src.db.repositories.users import UsersService, get_users_service
from src.schemas.user import UserCreate, UserOut, UserInDB, UserUpdate

router_users = APIRouter()


@router_users.post("/", response_model=UserOut)
async def create_user(obj: UserCreate, user_service: UsersService = Depends(get_users_service), user: UserInDB = Depends(get_current_user)) -> UserOut:
    return await user_service.create(obj)


@router_users.get("/", response_model=List[UserOut])
async def get_users(user_service: UsersService = Depends(get_users_service),
                    user: UserInDB = Depends(check_superuser_credentials)) -> Optional[List[UserOut]]:
    return await user_service.get_all()


@router_users.get("/{pk}", response_model=UserOut)
async def get_one(pk: int, user_service: UsersService = Depends(get_users_service),
                  user: UserInDB = Depends(check_superuser_credentials)) -> Optional[UserOut]:
    return await user_service.get_one(pk)


@router_users.get("/me", response_model=UserOut)
async def get_me(current_user: UserOut = Depends(get_current_active_user)) -> UserOut:
    return current_user


@router_users.put("/me", response_model=UserUpdate)
async def update_user(obj: UserOut, user_service: UsersService = Depends(get_users_service),
                      current_user: UserOut = Depends(get_current_active_user)):
    return await user_service.update(current_user.id, obj, current_user)


@router_users.put("/{pk}", response_model=UserUpdate)
async def update_user(obj: UserOut, pk: int, user_service: UsersService = Depends(get_users_service),
                      user: UserInDB = Depends(check_superuser_credentials)) -> UserUpdate:
    return await user_service.update(pk, obj, user)


@router_users.delete("/{pk}", response_model=bool)
async def delete_user(pk: int, user_service: UsersService = Depends(get_users_service),
                      user: UserInDB = Depends(check_superuser_credentials)) -> bool:
    return await user_service.delete(pk)



