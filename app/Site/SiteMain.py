import app.DataBase.db as MainDB
import app.DataBase.methods as DataBaseMethods
from flask import Flask, url_for, request, render_template, redirect, abort, send_file
import datetime
from flask_login import LoginManager, login_manager, login_required, login_user, logout_user, current_user
from io import BytesIO
from app.Site.forms.user import LoginForm
from peewee import fn
from flask import jsonify
from app.Site.api import api


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

    def __init__(self):
        self.initFlaskConfig()
        self.initRouters()
        self.ParamsManagerObject = self.ParamsManager()

    def initFlaskConfig(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'VanyaPidoras'

        self.login_manager = LoginManager()
        self.login_manager.init_app(self.app)

        self.app.jinja_env.auto_reload = True
        self.app.config['TEMPLATES_AUTO_RELOAD'] = True

        self.app.register_blueprint(api, url_prefix='/api')

    def startFlask(self):
        self.app.run(port=80, host="0.0.0.0")

    def initRouters(self):

        @self.login_manager.user_loader
        def load_user(user_id):
            return MainDB.Profile.get(MainDB.Profile.ID == user_id)

        @self.app.route("/")
        @self.app.route("/index")
        def MainPage():
            if not current_user.is_authenticated:
                return redirect("/login")
            return render_template('mainPage.html', **self.ParamsManagerObject.getParams())

        @self.app.route('/logout')
        @login_required
        def logout():
            logout_user()
            return redirect("/")

        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            form = LoginForm()
            if form.validate_on_submit():
                user = MainDB.Profile.select().where(
                    fn.lower(MainDB.Profile.Username) == form.login.data.lower())
                if len(user) and user[0].check_password(form.password.data):
                    login_user(user[0], remember=form.remember_me.data)
                    return redirect("/")
                return render_template('login.html',
                                       message="Неправильный логин или пароль",
                                       form=form, **self.ParamsManagerObject.getParams())
            return render_template('login.html', form=form, **self.ParamsManagerObject.getParams())