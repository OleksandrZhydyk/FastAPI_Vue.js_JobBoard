from pydantic import BaseModel


class Login(BaseModel):
    username: str
    password: str


class Status(BaseModel):
    message: bool


class AccessToken(BaseModel):
    access_token: str
