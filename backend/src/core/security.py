from fastapi import Depends, HTTPException, Security
from fastapi_jwt_auth import AuthJWT
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette import status
from starlette.status import HTTP_401_UNAUTHORIZED


from schemas.user import UserInDB, UserOut
from db.models.users import User
from db.base import get_session


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


async def get_user(database, email: str) -> UserInDB:
    query = select(User).where(User.email == email)
    db_obj = await database.execute(query)
    instance = db_obj.scalar()
    return instance


async def authenticate_user(database, email: str, password: str):
    user = await get_user(database, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(
    db: AsyncSession = Depends(get_session),
    Authorize: AuthJWT = Depends()
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "authenticate_value"},
    )
    Authorize.jwt_required()
    user_email = Authorize.get_jwt_subject()
    user = await get_user(db, email=user_email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: UserOut = Security(get_current_user)
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def check_company_credentials(
    user: UserOut = Security(get_current_active_user)
) -> UserOut:
    if not user.is_company:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="You are unauthorized"
        )
    return user


async def check_superuser_credentials(
    user: UserOut = Security(get_current_active_user)
) -> UserOut:
    if not user.is_superuser:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="You are unauthorized super"
        )
    return user
