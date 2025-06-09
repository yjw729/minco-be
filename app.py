"""graffiti app."""

from contextlib import asynccontextmanager

from fastapi import APIRouter, Depends, FastAPI
from starlette.middleware.cors import CORSMiddleware
from router import router as api_router
from router import auth_router as auth_api_router
from auth.jwt_auth import JWTAuthBearer
from exception_handler import global_exception_handlers

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    yield
    # Clean up the ML models and release the resources


app = FastAPI(
    title="minco BE 🚀🚀🚀",
    lifespan=lifespan,
    description="minco BE is based on FastAPI framework. 🚀🚀🚀",
    version="0.0.1",
    terms_of_service="https://mindco.com",
    contact={
        "name": "MAC team",
        "url": "https://mindco.com",
        "email": "test@mindco.com",
    },
    exception_handlers=global_exception_handlers,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

auth_router = APIRouter(dependencies=[Depends(JWTAuthBearer())])
app.include_router(router=api_router, prefix="/api/v1", tags=["账号管理"])
app.include_router(router=auth_api_router, prefix="/api/v1", tags=["账号管理"])
