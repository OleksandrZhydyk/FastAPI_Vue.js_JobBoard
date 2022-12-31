from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.core.security import authenticate_user, create_access_token, create_refresh_token
from src.schemas.token import Token
from src.endpoints.jobs import router_jobs
from src.endpoints.users import router_users
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

app.include_router(router_users, prefix="/users", tags=["users"])
app.include_router(router_jobs, prefix="/jobs", tags=["jobs"])


@app.post("/auth", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email, "scopes": form_data.scopes}, )
    refresh_token = create_refresh_token(data={"sub": user.email, "scopes": form_data.scopes},)
    return {"access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"}

