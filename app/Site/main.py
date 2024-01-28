import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.status import HTTP_401_UNAUTHORIZED
from app.Calculation.TTT import recalculateWorkspace

import app.Site.api.api as api
#from app.DataBase.db2 import create_db_and_tables
from app.DataBase.methods import createDB
from app.params import DEBUG, SITE_IP, SITE_PORT
from app.Site.exceptions import NotAuthenticatedException

app = FastAPI(
    docs_url="/api/docs", openapi_url="/api/openapi.json", title='OWBalancer', version="1.3", middleware=[Middleware(CORSMiddleware, allow_origins=["*"])])

app.include_router(api.router)

@app.exception_handler(NotAuthenticatedException)
def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
    res = Response("UNAUTHORIZED", HTTP_401_UNAUTHORIZED)
    res.set_cookie("access-token", "", max_age=0)
    return res


@app.on_event("startup")
async def startup():
    createDB()