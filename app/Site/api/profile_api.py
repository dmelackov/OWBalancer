from flask import Blueprint, request, send_file
from flask_login import login_required, current_user
from flask import jsonify
from app.Calculation.PILBalance import createImage
from app.Calculation.GameBalance import createGame
from io import BytesIO
import json
import logging
from app.DataBase.RolesMethods import checkProfilePermission, getUserPermissions
from app.Site.api.settings_api import api as settings_api

module_logger = logging.getLogger("api")

api = Blueprint('profile_api', __name__, template_folder='templates',
                static_folder='static')

api.register_blueprint(settings_api, url_prefix='/settings')


@api.route('/balanceImage', methods=['POST'])
@login_required
def balanceImage():
    module_logger.info(f"{current_user.Username} trying get balance image'")
    data = request.get_json()
    return serve_pil_image(createImage(data, current_user))


@api.route('/getBalances', methods=['GET'])
@login_required
def getBalances():
    if not checkProfilePermission(current_user, "do_balance"):
        return jsonify({"status": 403})
    module_logger.info(f"{current_user.Username} trying get balance")
    balance = createGame(current_user.ID)
    newBalance = {}
    if balance:
        newBalance["External"] = balance[0]
        newBalance["Balances"] = balance[1][:5000]
        newBalance["ok"] = True
        module_logger.info(
            f"{current_user.Username} recieve balance with size {len(newBalance['Balances'])}")
    else:
        newBalance["ok"] = False
        module_logger.info(f"{current_user.Username} dont recieve balances")
    return json.dumps(newBalance)


def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, format='JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


@api.route('/getPermissions', methods=['GET'])
@login_required
def getPermissions():
    module_logger.info(f"{current_user.Username} trying get permissions")
    perms = getUserPermissions(current_user)
    if perms is None:
        return jsonify([])
    perms = list(map(lambda x: x.Name, perms))
    return jsonify(perms)
