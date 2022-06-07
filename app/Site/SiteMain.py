import app.DataBase.db as MainDB
from flask import Flask
from flask_login import LoginManager
from app.Site.api.api import api
import logging
from flask_wtf.csrf import CSRFProtect
from app.params import site_port
from waitress import serve


module_logger = logging.getLogger("site")


class FlaskSite:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FlaskSite, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        module_logger.info("Site init")
        self.initFlaskConfig()
        self.initRouters()
        module_logger.info("Site init complete")

    def initFlaskConfig(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'VanyaPidoras'

        self.login_manager = LoginManager()
        self.login_manager.init_app(self.app)

        self.csrf = CSRFProtect()
        self.csrf.init_app(self.app)

        self.app.config.setdefault(
            "WTF_CSRF_HEADERS", ["X-CSRFToken", "X-CSRF-Token", "X-Csrf-Token"])

    def startFlask(self):
        serve(self.app, host="0.0.0.0", port=site_port)

    def initRouters(self):

        @self.login_manager.user_loader
        def load_user(user_id):
            return MainDB.Profile.get(MainDB.Profile.ID == user_id)

        self.app.register_blueprint(api, url_prefix='/api')
