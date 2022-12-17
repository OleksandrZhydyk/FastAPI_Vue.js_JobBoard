import uvicorn
from fastapi import FastAPI
from endpoints.users import router
from db.base import database

app = FastAPI()
app.include_router(router, prefix="/users", tags=["users"])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# if __name__ == "__main__":
#     uvicorn.run()
