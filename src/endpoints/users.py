from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.core.security import authenticate_user, create_access_token
from src.db.base import db
from src.schemas.token import Token
from src.db.repositories.users import UsersService, get_users_service
from src.schemas.user import UserCreate, UserOut, UserUpdate

router_users = APIRouter()


@router_users.post("/", response_model=UserOut)
async def create_user(obj: UserCreate, user_service: UsersService = Depends(get_users_service)) -> UserOut:
    return await user_service.create(obj)


@router_users.get("/", response_model=List[UserOut])
async def get_users(user_service: UsersService = Depends(get_users_service),) -> Optional[List[UserOut]]:
    return await user_service.get_all()


@router_users.get("/{pk}", response_model=UserOut)
async def get_one(pk: int, user_service: UsersService = Depends(get_users_service)) -> Optional[UserOut]:
    return await user_service.get_one(pk)


@router_users.put("/{pk}", response_model=UserUpdate)
async def update_user(obj: UserOut, pk: int, user_service: UsersService = Depends(get_users_service)) -> UserUpdate:
    return await user_service.update(pk, obj)


@router_users.delete("/{pk}", response_model=bool)
async def delete_user(pk: int, user_service: UsersService = Depends(get_users_service)) -> bool:
    return await user_service.delete(pk)


@router_users.post("/auth", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email}, )
    return {"access_token": access_token, "token_type": "bearer"}

