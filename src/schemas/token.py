from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str
    # refresh_token: str
    # user: IUserRead


class TokenRead(BaseModel):
    email: EmailStr


class RefreshToken(BaseModel):
    refresh_token: str
