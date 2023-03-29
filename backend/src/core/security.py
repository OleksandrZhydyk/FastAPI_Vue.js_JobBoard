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

# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl="/auth/login",
#     scheme_name="JWT"
# )


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


# def create_access_token(data: dict) -> str:
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
#     return encoded_jwt


# def create_refresh_token(data: dict) -> str:
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=Config.REFRESH_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(
#         to_encode, Config.JWT_REFRESH_SECRET_KEY, algorithm=Config.ALGORITHM
#     )
#     return encoded_jwt


# async def get_current_user(
#     security_scopes: SecurityScopes,
#     token: str = Depends(oauth2_scheme),
#     db: AsyncSession = Depends(get_session),
# ):
#     if security_scopes.scopes:
#         authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
#     else:
#         authenticate_value = "Bearer"
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "authenticate_value"},
#     )
#     try:
#         payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#         token_scopes = payload.get("scopes", [])
#         token_data = TokenRead(scopes=token_scopes, email=email)
#     except (JWTError, ValidationError):
#         raise credentials_exception
#     user = await get_user(db, email=token_data.email)
#     if user is None:
#         raise credentials_exception
#     for scope in security_scopes.scopes:
#         if scope not in token_data.scopes:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Not enough permissions",
#                 headers={"WWW-Authenticate": authenticate_value},
#             )
#     return user

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
