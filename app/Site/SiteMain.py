from app.DataBase.db import db as MainDB

from flask import Flask, url_for, request, render_template, redirect, abort, send_file
import datetime
from flask_login import LoginManager, login_manager, login_required, login_user, logout_user, current_user
from io import BytesIO


class FlaskSite:
    def __init__(self):
        self.initFlaskConfig()
        self.initRouters()

    def initFlaskConfig(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'VanyaPidoras'

        self.login_manager = LoginManager()
        self.login_manager.init_app(self.app)

        self.app.jinja_env.auto_reload = True
        self.app.config['TEMPLATES_AUTO_RELOAD'] = True

    def startFlask(self):
        self.app.run(port=80, host="0.0.0.0")

    def initRouters(self):

        @self.login_manager.user_loader
        def load_user(user_id):
            return MainDB.User.get(MainDB.User.ID == user_id)

        @self.app.route("/")
        @self.app.route("/index")
        def MainPage():
            return "Hello World!"

    class ParamsManager:
        params = []
        init = False
        def getParams(self):
            if not self.init:
                self.initParams()
            return self.params

        def initParams(self):
            self.init = True
            self.params['title'] = "OWBalancer"