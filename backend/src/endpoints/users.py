import json
from typing import List, Optional

import pydantic
from fastapi import APIRouter, Depends, UploadFile, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from db.base import get_session
from core.security import (
    get_current_active_user,
    check_superuser_credentials,
    check_company_credentials,
)
from db.repositories.users import UsersService, get_users_service
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
    email: str = Form(None),
    name: str = Form(None),
    clear_avatar: bool = Form(False),
    clear_resume: bool = Form(False),
    password: str = Form(None),
    avatar: UploadFile | None = None,
    resume: UploadFile | None = None,
    user_service: UsersService = Depends(get_users_service),
    db: AsyncSession = Depends(get_session),
    current_user: UserOut = Depends(get_current_active_user),
):
    try:
        user_update_data = UserUpdate(email=email, name=name, password=password)
    except pydantic.ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=json.loads(e.json())
        )

    return await user_service.update(user_update_data, avatar, clear_avatar, resume, clear_resume, current_user, db)


@router_users.get("/{pk}", response_model=UserOut)
async def get_one(
    pk: int,
    user_service: UsersService = Depends(get_users_service),
    current_user: UserInDB = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_session),
):
    return await user_service.get_one(pk, current_user, db)


@router_users.put("/{pk}", response_model=UserOut)
async def update_user(
    email: str = Form(None),
    name: str = Form(None),
    is_company: bool = Form(None),
    is_active: bool = Form(None),
    password: str = Form(None),
    clear_avatar: bool = Form(False),
    clear_resume: bool = Form(False),
    avatar: UploadFile | None = None,
    resume: UploadFile | None = None,
    user_service: UsersService = Depends(get_users_service),
    current_user: UserInDB = Depends(check_superuser_credentials),
    db: AsyncSession = Depends(get_session),
) -> UserOut:
    try:
        user_update_data = UserUpdate(
            email=email, name=name, password=password,
            is_company=is_company, is_active=is_active)
    except pydantic.ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=json.loads(e.json())
        )
    return await user_service.update(user_update_data, avatar, clear_avatar, resume, clear_resume, current_user, db)


@router_users.delete("/{pk}", response_model=Status)
async def delete_user(
    pk: int,
    user_service: UsersService = Depends(get_users_service),
    db: AsyncSession = Depends(get_session),
    current_user: UserInDB = Depends(check_superuser_credentials),
) -> Status:
    return await user_service.delete(pk, current_user, db)
