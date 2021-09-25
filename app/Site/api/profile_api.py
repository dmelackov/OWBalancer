from flask import Blueprint, request, send_file
from flask.wrappers import Response
from flask_login import login_required, current_user
from flask import jsonify
from app.Calculation.PILBalance import createImage as createImageThemeOne
from app.Calculation.PILBalance2 import createImage as createImageThemeTwo
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


def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, format='JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


@api.route('/balanceImage', methods=['POST'])
@login_required
def balanceImage():
    module_logger.info(f"{current_user.Username} trying get balance image'")
    data = request.get_json()
    theme = data.get("theme", 0)
    playersData = data.get("playersData", None)
    if playersData is None:
        return Response(status=400)
    if theme == 0:
        return serve_pil_image(createImageThemeOne(playersData, current_user))
    elif theme == 1:
        return serve_pil_image(createImageThemeTwo(playersData, current_user))
    else:
        return serve_pil_image(createImageThemeOne(playersData, current_user))


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


@api.route('/getPermissions', methods=['GET'])
@login_required
def getPermissions():
    module_logger.info(f"{current_user.Username} trying get permissions")
    perms = getUserPermissions(current_user)
    if perms is None:
        return jsonify([])
    perms = list(map(lambda x: x.Name, perms))
    return jsonify(perms)