from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_session
from core.security import (
    get_current_active_user,
    check_superuser_credentials,
    check_company_credentials,
)
from db.repositories.users import UsersService, get_users_service
from schemas.job import JobOut
from schemas.token import Status
from schemas.user import UserCreate, UserOut, UserInDB, UserUpdate, UserResponse

router_users = APIRouter()


@router_users.post("/", response_model=UserOut)
async def create_user(
    obj_in: UserCreate,
    db: AsyncSession = Depends(get_session),
    user_service: UsersService = Depends(get_users_service),
) -> UserOut:
    return await user_service.create(obj_in, db)


@router_users.get("/", response_model=List[UserOut])
async def get_users(
    user_service: UsersService = Depends(get_users_service),
    db: AsyncSession = Depends(get_session),
    user: UserInDB = Depends(check_superuser_credentials),
) -> Optional[List[UserOut]]:
    return await user_service.get_all(db)


@router_users.get("/me", response_model=UserResponse)
async def get_me(
    user_service: UsersService = Depends(get_users_service),
    db: AsyncSession = Depends(get_session),
    current_user: UserOut = Depends(get_current_active_user),
):
    return await user_service.get_one(current_user.id, current_user, db)


@router_users.put("/me", response_model=UserOut)
async def update_me(
    obj_in: UserUpdate,
    user_service: UsersService = Depends(get_users_service),
    db: AsyncSession = Depends(get_session),
    current_user: UserOut = Depends(get_current_active_user),
):
    return await user_service.update(obj_in, current_user, db)


@router_users.get("/me/vacancies", response_model=List[JobOut])
async def get_company_jobs(
    user_service: UsersService = Depends(get_users_service),
    current_user: UserInDB = Depends(check_company_credentials),
    db: AsyncSession = Depends(get_session),
):
    return await user_service.get_company_vacancies(current_user, db)


@router_users.get("/{pk}", response_model=UserOut)
async def get_one(
    pk: int,
    user_service: UsersService = Depends(get_users_service),
    current_user: UserInDB = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_session),
):
    return await user_service.get_one(pk, current_user, db)


@router_users.put("/{pk}", response_model=UserUpdate)
async def update_user(
    obj_in: UserUpdate,
    user_service: UsersService = Depends(get_users_service),
    current_user: UserInDB = Depends(check_superuser_credentials),
    db: AsyncSession = Depends(get_session),
) -> UserOut:
    return await user_service.update(obj_in, current_user, db)


@router_users.delete("/{pk}", response_model=Status)
async def delete_user(
    pk: int,
    user_service: UsersService = Depends(get_users_service),
    db: AsyncSession = Depends(get_session),
    current_user: UserInDB = Depends(check_superuser_credentials),
) -> Status:
    return await user_service.delete(pk, current_user, db)
