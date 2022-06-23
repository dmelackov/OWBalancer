from quart import Blueprint, Response, jsonify
from quart_login import login_required, login_user, logout_user, current_user
import logging
from app.Site.forms.user import LoginForm, RegisterForm
import app.DataBase.db as db

module_logger = logging.getLogger("api")

api = Blueprint('auth_api', __name__, template_folder='templates',
                static_folder='static')


@api.route('/login', methods=['POST'])
async def login() -> Response:
    if current_user.is_authenticated:
        return Response("Not enough permissions", status=403)
    module_logger.info(f"Trying log in")
    form = LoginForm()
    if form.validate_on_submit():
        U = db.Profile.check(form.login.data, form.password.data).data
        if U:
            module_logger.info(f"Sucefful log in {form.login.data}")
            login_user(U, remember=form.remember_me.data)
            return jsonify({"status": 200})
        module_logger.info(f"Incorrect log in {form.login.data}")
    return jsonify({"status": 400, "message": "Incorrect login or password"})



@api.route('/registration', methods=['POST'])
async def registration() -> Response:
    if current_user.is_authenticated:
        return Response("Not enough permissions", status=403)
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return jsonify({"status": 400, "message": "Passwords don't match"})
        if db.Profile.getProfile(form.login.data):
            return jsonify({"status": 400, "message": "User already exist"})
        db.Profile.create(form.login.data, form.password.data)
        return jsonify({"status": 200, "message": "OK"})
    return jsonify({"status": 400})


@login_required
@api.route('/logout', methods=['POST'])
async def logout() -> Response:
    logout_user()
    return jsonify({"status": 200, "message": "OK"})
