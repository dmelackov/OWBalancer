import app.DataBase.db as MainDB
import app.DataBase.methods as DataBaseMethods
import app.DataBase.RolesMethods as RolesMethods
from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from app.Site.forms.user import LoginForm, RegisterForm
from peewee import fn
from flask import jsonify, request
from app.Site.api.api import api
import logging
from flask_wtf.csrf import CSRFProtect
from app.params import site_port

module_logger = logging.getLogger("site")


class FlaskSite:
    class ParamsManager:
        params = {}
        init = False

        def __init__(self):
            pass

        def getParams(self):
            if not self.init:
                self.initParams()
            return self.params

        def initParams(self):
            self.init = True
            self.params['title'] = "OWBalancer"
            self.params['description'] = "Сайт для балансировки игроков между командами в Overwatch"

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FlaskSite, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        module_logger.info("Site init")
        self.initFlaskConfig()
        self.initRouters()
        self.ParamsManagerObject = self.ParamsManager()
        module_logger.info("Site init complete")

    def initFlaskConfig(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'VanyaPidoras'

        self.login_manager = LoginManager()
        self.login_manager.init_app(self.app)

        self.csrf = CSRFProtect()
        self.csrf.init_app(self.app)

        self.app.jinja_env.auto_reload = True
        self.app.config['TEMPLATES_AUTO_RELOAD'] = True

    def startFlask(self):
        self.app.run(port=site_port, host="0.0.0.0")

    def initRouters(self):
        @self.login_manager.user_loader
        def load_user(user_id):
            return MainDB.Profile.get(MainDB.Profile.ID == user_id)
        self.app.register_blueprint(api, url_prefix='/api')