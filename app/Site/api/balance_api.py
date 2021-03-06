from flask import Blueprint, request
from flask.wrappers import Response
import logging
import json
from flask_login import login_required, current_user
from app.DataBase.RolesMethods import checkProfilePermission
from flask import jsonify
from app.Calculation.GameBalance import createGame
from app.Calculation.StaticAnalisys import recountModel
module_logger = logging.getLogger("api")

api = Blueprint('balance_api', __name__, template_folder='templates',
                static_folder='static')


@api.route('/calcBalance', methods=['POST'])
@login_required
def calcBalance():
    module_logger.info(f"{current_user.Username} trying to calc Balance'")
    data = request.get_json()
    balance = {}
    balance["static"] = data.get("static", None)
    balance["active"] = data.get("active", None)
    if balance["static"] is None or balance["active"] is None:
        return Response(status=400)
    return jsonify(recountModel(balance["static"], balance["active"], current_user))


@api.route('/getBalances', methods=['GET'])
@login_required
def getBalances():
    if not checkProfilePermission(current_user, "do_balance"):
        return jsonify({"status": 403})
    module_logger.info(f"{current_user.Username} trying get balance")
    balance = createGame(current_user)
    if balance["result"] == 200:
        module_logger.info(
            f"{current_user.Username} recieve balance with size {len(balance['active'])}")
    else:
        module_logger.info(f"{current_user.Username} dont recieve balances with reason {balance['status']}")
    return json.dumps(balance)
