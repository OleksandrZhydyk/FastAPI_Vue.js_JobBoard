import uvicorn
from fastapi import FastAPI, Request
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from endpoints.auth import router_auth
from endpoints.jobs import router_vacancies
from endpoints.users import router_users
from db.base import init_models


def get_application() -> FastAPI:
    app = FastAPI(title="Employment exchange")

    @app.on_event("startup")
    async def startup():
        await init_models()

    app.include_router(router_auth, prefix="/auth", tags=["auth"])
    app.include_router(router_users, prefix="/users", tags=["users"])
    app.include_router(router_vacancies, prefix="/vacancies", tags=["vacancies"])

    @app.exception_handler(AuthJWTException)
    def authjwt_exception_handler(request: Request, exc: AuthJWTException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message}
        )

    # @app.post("/auth", response_model=Token)
    # async def login_for_access_token(
    #     db: AsyncSession = Depends(get_session),
    #     form_data: OAuth2PasswordRequestForm = Depends(),
    # ) -> Token:
    #     print(form_data.username)
    #     user = await authenticate_user(db, form_data.username, form_data.password)
    #
    #     if not user:
    #         raise HTTPException(
    #             status_code=status.HTTP_401_UNAUTHORIZED,
    #             detail="Incorrect username or password",
    #             headers={"WWW-Authenticate": "Bearer"},
    #         )
    #     access_token = create_access_token(
    #         data={"sub": user.email, "scopes": form_data.scopes},
    #     )
    #     refresh_token = create_refresh_token(
    #         data={"sub": user.email, "scopes": form_data.scopes},
    #     )
    #     return {
    #         "access_token": access_token,
    #         "refresh_token": refresh_token,
    #         "token_type": "bearer",
    #     }

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    add_pagination(app)

    return app


app = get_application()

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)
