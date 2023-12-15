import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi_login import LoginManager
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

import app.Site.api.api as api
from app.params import DEBUG, SITE_IP, SITE_PORT
from app.Site.exceptions import NotAuthenticatedException

from app.DataBase.methods import createDB
class Site:
    app: FastAPI
    loginManager: LoginManager

    def __init__(self) -> None:
        createDB()
        app = FastAPI(
            docs_url="/api/docs", openapi_url="/api/openapi.json", title='OWBalancer', version="1.3", middleware=[ Middleware(CORSMiddleware, allow_origins=["*"])])

        self.initRouters(app)
        self.initHandlers(app)
        self.app = app


    def initRouters(self, app) -> None:
        app.include_router(api.router)

    def initHandlers(self, app) -> None:
        @app.exception_handler(NotAuthenticatedException)
        def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
            res = Response("UNAUTHORIZED", HTTP_401_UNAUTHORIZED)
            res.set_cookie("access-token", "", max_age=0)
            return res

    def start(self) -> None:
        uvicorn.run(self.app, host=SITE_IP, port=SITE_PORT)

site = Site()
app = site.app