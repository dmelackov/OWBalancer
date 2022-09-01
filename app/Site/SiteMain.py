import app.DataBase.db as MainDB
from flask import Flask
from flask_login import LoginManager
from app.Site.api.api import api
import logging
from app.params import site_port, secretKey, debug
import uvicorn
from asgiref.wsgi import WsgiToAsgi

module_logger = logging.getLogger("site")


class FlaskSite:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FlaskSite, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        module_logger.info("Site init")
        self.initFlaskConfig()
        self.initRouters()
        module_logger.info("Site init complete")

    def initFlaskConfig(self) -> None:
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = secretKey
        self.app.config["SESSION_COOKIE_SAMESITE"] = "Strict"
        self.app.config["REMEMBER_COOKIE_SAMESITE"] = "Strict"

        self.login_manager = LoginManager()
        self.login_manager.init_app(self.app)

        self.asgi_app = WsgiToAsgi(self.app)

    def startFlask(self) -> None:
        uvicorn.run(self.asgi_app, host="0.0.0.0", port=site_port, debug=debug)

    def initRouters(self) -> None:
        #@self.app.before_request
        #def _db_connect() -> None:
        #    MainDB.db.connect()

        #@self.app.teardown_request
        #def _db_close(exc) -> None:
        #    if not MainDB.db.is_closed():
        #        MainDB.db.close()

        @self.login_manager.user_loader
        def load_user(user_id: int) -> MainDB.Profile:
            return MainDB.Profile.getInstance(user_id)

        self.app.register_blueprint(api, url_prefix='/api')
