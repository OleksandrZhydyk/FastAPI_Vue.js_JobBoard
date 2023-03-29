import os

from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel


class Config:
    if os.environ.get("TESTING"):
        DB_USER = "postgres"
        DB_PASSWORD = "admin"
        DB_NAME = "test_fastapi"
        DB_HOST = "localhost"
        DB_PORT = "5432"
    else:
        DB_USER = os.getenv("POSTGRES_USER", "postgres")
        DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin")
        DB_NAME = os.getenv("POSTGRES_NAME", "fastapi")
        DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
        DB_PORT = os.getenv("POSTGRES_PORT", "5432")
    if os.environ.get("GITHUB_WORKFLOW"):
        DB_USER = "postgres"
        DB_PASSWORD = "admin"
        DB_NAME = "github_actions"
        DB_HOST = "localhost"
        DB_PORT = "5432"
    DB_CONFIG = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        f"?prepared_statement_cache_size=0"
    )
    SECRET_KEY = os.getenv(
        "SECRET_KEY", "44f4c1953195bdcbdaad74b399171c3a48a9c56c8f9738352502ce4a261f4149"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15)
    REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 2880)
    JWT_REFRESH_SECRET_KEY = os.getenv(
        "JWT_REFRESH_SECRET_KEY",
        "1e3c5b421af30b2495e0af81bc71af012a369bd0ce6a1315833c4810f3fae500",
    )
    ALGORITHM = os.getenv("ALGORITHM", "HS256")


SECRET_KEY = os.getenv(
        "SECRET_KEY", "44f4c1953195bdcbdaad74b399171c3a48a9c56c8f9738352502ce4a261f4149"
    )
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15) * 60
REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 2880) * 60

class Settings(BaseModel):
    authjwt_secret_key: str = SECRET_KEY
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False
    authjwt_cookie_samesite: str = 'lax'
    authjwt_cookie_secure: bool = False
    authjwt_algorithm = ALGORITHM
    authjwt_access_token_expires = 60
    authjwt_refresh_token_expires = REFRESH_TOKEN_EXPIRE_MINUTES
    authjwt_cookie_max_age = ACCESS_TOKEN_EXPIRE_MINUTES


@AuthJWT.load_config
def get_config():
    return Settings()

