from typing import List

from pydantic import BaseModel, EmailStr

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    # user: IUserRead


class TokenRead(BaseModel):
    email: EmailStr
    scopes: List[str] = []


class RefreshToken(BaseModel):
    refresh_token: str
