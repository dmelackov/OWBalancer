from flask import Blueprint, Response, request
from flask import jsonify
import logging
from flask_login import current_user
from app.Site.api.settings_api import api as settings_api
from app.Site.api.auth_api import api as auth_api
from app.Site.api.balance_api import api as balance_api

module_logger = logging.getLogger("api")

api = Blueprint('profile_api', __name__, template_folder='templates',
                static_folder='static')

api.register_blueprint(settings_api, url_prefix='/settings')
api.register_blueprint(auth_api, url_prefix='/auth')
api.register_blueprint(balance_api, url_prefix='/balance')


@api.route('/getPermissions', methods=['GET'])
async def getPermissions() -> Response:
    if not current_user.is_authenticated:
        return jsonify([])
    module_logger.info(f"{current_user.Username} trying get permissions")
    perms = getUserPermissions(current_user)
    if perms is None:
        return jsonify([])
    perms = list(map(lambda x: x.Name, perms))
    return jsonify(perms)


@api.route('/getCurrentUserInfo', methods=['GET'])
async def getCurrentUserInfo() -> Response:
    info = {}
    if not current_user.is_authenticated:
        info["Username"] = None
        info["Auth"] = False
    else:
        info["Username"] = current_user.Username
        info["Auth"] = True
        info["ID"] = current_user.ID
    return jsonify(info)
