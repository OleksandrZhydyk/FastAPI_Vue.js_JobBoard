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
    ACCESS_TOKEN_EXPIRE_SECONDS = os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS", 60)
    REFRESH_TOKEN_EXPIRE_SECONDS = os.getenv("REFRESH_TOKEN_EXPIRE_SECONDS", 3600)
    COOKIE_MAX_AGE = os.getenv("COOKIE_MAX_AGE", 7200)
    ALGORITHM = os.getenv("ALGORITHM", "HS256")

    STATIC_ROOT = os.getenv("STATIC_ROOT", "static")
    HOSTED_DOMAIN = os.getenv("HOSTED_DOMAIN", "http://localhost:8000")

    USE_S3 = os.getenv('USE_S3')
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_MEDIA_LOCATION = os.getenv("AWS_MEDIA_LOCATION")


class AuthJWTSettings(BaseModel):
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False
    authjwt_cookie_samesite: str = 'lax'
    authjwt_cookie_secure: bool = False
    authjwt_secret_key: str = Config.SECRET_KEY
    authjwt_algorithm: str = Config.ALGORITHM
    authjwt_access_token_expires: int = Config.ACCESS_TOKEN_EXPIRE_SECONDS
    authjwt_refresh_token_expires: int = Config.REFRESH_TOKEN_EXPIRE_SECONDS
    authjwt_cookie_max_age: int = 7200


@AuthJWT.load_config
def get_config():
    return AuthJWTSettings()
