from flask import Blueprint, Response, jsonify, redirect, current_app, session
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
import logging
from app.Site.forms.user import LoginForm, RegisterForm
import app.DataBase.db as MainDB
import app.DataBase.methods as DataBaseMethods
import app.DataBase.RolesMethods as RolesMethods
from peewee import fn
from flask_wtf import csrf
module_logger = logging.getLogger("api")

api = Blueprint('auth_api', __name__, template_folder='templates',
                static_folder='static')


@api.route('/login', methods=['POST'])
def loginPost():
    if current_user.is_authenticated:
        return Response(status=403)
    module_logger.info(f"Trying log in")
    form = LoginForm()
    if form.validate_on_submit():
        user = MainDB.Profile.select().where(
            fn.lower(MainDB.Profile.Username) == form.login.data.lower())
        if len(user) and user[0].check_password(form.password.data):
            module_logger.info(f"Sucefful log in {form.login.data}")
            login_user(user[0], remember=form.remember_me.data)
            return jsonify({"status": 200})
        module_logger.info(f"Incorrect log in {form.login.data}")
    return jsonify({"status": 400, "message": "Incorrect login or password"})


@api.route('/registration', methods=['POST'])
def registration():
    if current_user.is_authenticated:
        return Response(status=403)
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return jsonify({"status": 400, "message": "Passwords don't match"})
        if MainDB.Profile.select().where(fn.lower(MainDB.Profile.Username) == form.login.data.lower()):
            return jsonify({"status": 400, "message": "User already exist"})
        DataBaseMethods.createProfile(
            form.login.data, form.password.data)
        RolesMethods.addRoleToProfile(
            MainDB.Profile.get(
                MainDB.Profile.Username == form.login.data),
            MainDB.Roles.get(MainDB.Roles.ID == 1))
        return Response(status=200)
    return jsonify({"status": 400})


@login_required
@api.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect("/")


@api.route('/getCSRF', methods=['GET'])
def getCSRF():
    return csrf.generate_csrf()
