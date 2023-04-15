import uvicorn

from fastapi import FastAPI, Request
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

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
    app.mount("/static", StaticFiles(directory=Path(__file__).parent/"static"), name="static")

    @app.exception_handler(AuthJWTException)
    def authjwt_exception_handler(request: Request, exc: AuthJWTException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message}
        )

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
