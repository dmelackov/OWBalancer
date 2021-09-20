import app.DataBase.db as MainDB
import app.DataBase.methods as DataBaseMethods
import app.DataBase.RolesMethods as RolesMethods
from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from app.Site.forms.user import LoginForm, RegisterForm
from peewee import fn
from flask import jsonify
from app.Site.api.api import api
import logging

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

        self.app.jinja_env.auto_reload = True
        self.app.config['TEMPLATES_AUTO_RELOAD'] = True

        self.app.register_blueprint(api, url_prefix='/api')

    def startFlask(self):
        self.app.run(port=5000, host="0.0.0.0")

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

        @self.app.route("/settings")
        def Setting():
            if not current_user.is_authenticated:
                return redirect("/login")
            return render_template('settings.html', **self.ParamsManagerObject.getParams())

        @self.app.route('/logout')
        @login_required
        def logout():
            logout_user()
            return redirect("/login")

        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            form = LoginForm()
            if form.validate_on_submit():
                user = MainDB.Profile.select().where(
                    fn.lower(MainDB.Profile.Username) == form.login.data.lower())
                if len(user) and user[0].check_password(form.password.data):
                    module_logger.info(f"Sucefful log in {form.login.data}")
                    login_user(user[0], remember=form.remember_me.data)
                    return redirect("/")
                module_logger.info(f"Incorrect log in {form.login.data}")
                return render_template('login.html',
                                       message="Неправильный логин или пароль",
                                       form=form, **self.ParamsManagerObject.getParams())
            return render_template('login.html', form=form, **self.ParamsManagerObject.getParams())

        @self.app.route('/register', methods=['GET', 'POST'])
        def reqister():
            form = RegisterForm()
            if current_user.is_authenticated:
                return redirect("/")
            if form.validate_on_submit():
                if form.password.data != form.password_again.data:
                    return render_template('register.html', **self.ParamsManagerObject.getParams(),
                                           form=form,
                                           message="Пароли не совпадают")
                if MainDB.Profile.select().where(fn.lower(MainDB.Profile.Username) == form.login.data.lower()):
                    return render_template('register.html', **self.ParamsManagerObject.getParams(),
                                           form=form,
                                           message="Такой пользователь уже есть")
                DataBaseMethods.createProfile(
                    form.login.data, form.password.data)
                RolesMethods.addRoleToProfile(
                    MainDB.Profile.get(
                        MainDB.Profile.Username == form.login.data),
                    MainDB.Roles.get(MainDB.Roles.ID == 1))
                return redirect('/login')
            return render_template('register.html', **self.ParamsManagerObject.getParams(), form=form)
