import uvicorn

from fastapi import FastAPI, Request, Response
from fastapi_login import LoginManager
from starlette.status import HTTP_401_UNAUTHORIZED

from app.params import DEBUG, SITE_IP, SITE_PORT
import app.Site.api.api as api
from app.Site.exceptions import NotAuthenticatedException


class Site:
    app: FastAPI
    loginManager: LoginManager

    def __init__(self) -> None:
        self.app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json", title='OWBalancer', version="1.3")
        self.initRouters()
        self.initHandlers()

    def initRouters(self) -> None:
        self.app.include_router(api.router)

    def initHandlers(self) -> None:
        @self.app.exception_handler(NotAuthenticatedException)
        def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
            res = Response("UNAUTHORIZED", HTTP_401_UNAUTHORIZED)
            res.set_cookie("access-token", "", max_age=0)
            return res

    def start(self) -> None:
        uvicorn.run(self.app, host=SITE_IP, port=SITE_PORT)
