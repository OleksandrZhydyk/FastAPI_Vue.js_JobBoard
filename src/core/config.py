import os
# from starlette.config import Config
#
# config = Config(".env")


class Config:
    DB_USER = os.getenv("POSTGRES_USER", "postgres")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin")
    DB_NAME = os.getenv("POSTGRES_NAME", "fastapi")
    DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
    DB_PORT = os.getenv("POSTGRES_PORT", "5432")
    DB_CONFIG = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    # DB_CONFIG = "postgresql+asyncpg://postgres:admin@localhost:5432/fastapi"

# DATABASE_URL = config("EE_DATABASE_URL", cast=str, default="")

# DATABASE_URL = "postgresql://postgres:admin@localhost:5432/fastapi"

# DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost:5432/fastapi"
