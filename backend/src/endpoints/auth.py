from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import authenticate_user
from db.base import get_session
from schemas.token import AccessToken

router_auth = APIRouter()


@router_auth.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                Authorize: AuthJWT = Depends(),
                db: AsyncSession = Depends(get_session)) -> AccessToken:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = Authorize.create_access_token(subject=user.email)
    refresh_token = Authorize.create_refresh_token(subject=user.email)
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    return AccessToken(access_token=access_token)


@router_auth.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()) -> AccessToken:
    """
    Refresh token endpoint. This will generate a new access token from
    the refresh token, but will mark that access token as non-fresh,
    as we do not actually verify a password in this endpoint.
    """
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user, fresh=False)
    Authorize.set_access_cookies(new_access_token)
    return AccessToken(access_token=new_access_token)


@router_auth.delete('/logout')
def logout(Authorize: AuthJWT = Depends()):
    """
    Because the JWT are stored in an httponly cookie now, we cannot
    log the user out by simply deleting the cookies in the frontend.
    We need the backend to send us a response to delete the cookies.
    """
    Authorize.jwt_required()

    Authorize.unset_jwt_cookies()
    return {"msg": "Successfully logout"}
