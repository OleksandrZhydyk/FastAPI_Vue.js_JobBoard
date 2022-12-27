from fastapi import FastAPI

from src.endpoints.users import router
from src.db.base import db


def init_app():
    db.init()

    app = FastAPI(
        title="Employment exchange"
    )

    @app.on_event("startup")
    async def startup():
        await db.create_all()

    @app.on_event("shutdown")
    async def shutdown():
        await db.close()

    return app


app = init_app()

app.include_router(router, prefix="/users", tags=["users"])

# @app.on_event("startup")
# async def startup():
#     await db.connect()
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     await db.disconnect()

