from fastapi import FastAPI

from src.endpoints.users import router
from src.db.base import database

app = FastAPI(title="Employment exchange")

app.include_router(router, prefix="/users", tags=["users"])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

