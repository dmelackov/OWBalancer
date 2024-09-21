
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.status import HTTP_401_UNAUTHORIZED
from contextlib import asynccontextmanager

import Site.api.api as api
from DataBase.database import create_db_and_tables
from Site.exceptions import NotAuthenticatedException
from DataBase.database import sessionmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()

app = FastAPI(
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    title='OWBalancer',
    version="1.3",
    middleware=[
        Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])
    ],
    lifespan=lifespan)

app.include_router(api.router)


@app.exception_handler(NotAuthenticatedException)
def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
    res = Response("UNAUTHORIZED", HTTP_401_UNAUTHORIZED)
    res.set_cookie("access-token", "", max_age=0)
    return res
