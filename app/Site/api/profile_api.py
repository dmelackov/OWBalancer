from quart import Blueprint, Response
from quart import jsonify
import logging
from quart_login import current_user
from app.Site.api.settings_api import api as settings_api
from app.Site.api.auth_api import api as auth_api
from app.Site.api.balance_api import api as balance_api
from app.Site.api.workspace_api import api as workspace_api
import app.Site.utils as utils

module_logger = logging.getLogger("api")

api = Blueprint('profile_api', __name__, template_folder='templates',
                static_folder='static')

api.register_blueprint(settings_api, url_prefix='/settings')
api.register_blueprint(auth_api, url_prefix='/auth')
api.register_blueprint(balance_api, url_prefix='/balance')
api.register_blueprint(workspace_api, url_prefix='/workspace')


@api.route('/getPermissions', methods=['GET'])
async def getPermissions() -> Response:
    if not current_user.is_authenticated:
        return jsonify([])
    module_logger.info(f"{current_user.Username} trying get permissions")
    WU = utils.getWorkspaceProfileByRequest()
    if not WU:
        return jsonify([])
    perms = WU.getPermissions().data
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
        info["Workspace"] = None
        req = jsonify(info)
    else:
        WU = utils.getWorkspaceProfileByRequest()
        info = current_user.getJson()
        info["Auth"] = True
        if WU:
            info["Workspace"] = WU.Workspace.getJson()
            info["Role"] = WU.Role.Name
            req = jsonify(info)
        else:
            info["Workspace"] = None
            info["Role"] = None
            req = jsonify(info)
            req.set_cookie('workspace', '', expires=0)
    return req
