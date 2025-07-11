
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.status import HTTP_401_UNAUTHORIZED

import backend.api as api
from environment.settings import settings
from infrastructure.database import DatabaseSessionManager, get_db_url
from domain.exceptions import DomainException
from backend.exception_mapping import exception_handler
from backend.exceptions import NotAuthenticatedException
from infrastructure.redis import AsyncRedisEngine, get_redis_url


@asynccontextmanager
async def lifespan(app: FastAPI):
    session_manager = DatabaseSessionManager(get_db_url(
        drivername=settings.db.driver,
        database=settings.db.name,
        host=settings.db.host,
        port=settings.db.port,
        username=settings.db.user,
        password=settings.db.password
    ))

    redis_engine = AsyncRedisEngine(
        get_redis_url(
            ip=settings.redis.host,
            port=settings.redis.port,
            db=str(settings.redis.db)
        ))

    app.state.redis_engine = redis_engine
    app.state.session_manager = session_manager
    yield
    if session_manager._engine is not None:
        await session_manager.close()
    if redis_engine.redis_pool is not None:
        await redis_engine.close()

app = FastAPI(
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    title='OWBalancer',
    version="1.3",
    middleware=[
        Middleware(CORSMiddleware, allow_origins=[
                   "localhost"], allow_methods=["*"])
    ],
    lifespan=lifespan)

app.include_router(api.router)


@app.exception_handler(NotAuthenticatedException)
def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
    res = Response("UNAUTHORIZED", HTTP_401_UNAUTHORIZED)
    res.set_cookie("access-token", "", max_age=0)
    return res


app.add_exception_handler(DomainException, exception_handler)
