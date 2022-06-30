from quart import Blueprint, request, Response
import logging
import json
from quart_login import login_required, current_user
from quart import jsonify
from app.Calculation.GameBalance import createGame
from app.Calculation.StaticAnalisys import recountModel
import app.Site.utils as utils
module_logger = logging.getLogger("api")

api = Blueprint('balance_api', __name__, template_folder='templates',
                static_folder='static')


@api.route('/calcBalance', methods=['POST'])
@login_required
async def calcBalance() -> Response:
    WU = utils.getWorkspaceProfileByRequest()
    if not WU:
        return Response("Not Found Workspace Profile", status=403)
    if not WU.checkPermission("do_balance").status:
        return Response("Not enough permissions", status=403)
    module_logger.info(f"{current_user.Username} trying to calc Balance'")
    data = await request.get_json()
    balance = {}
    balance["static"] = data.get("static", None)
    balance["active"] = data.get("active", None)
    if balance["static"] is None or balance["active"] is None:
        return Response("Invalid data", status=400)
    return jsonify(recountModel(balance["static"], balance["active"], current_user))


@api.route('/getBalances', methods=['GET'])
@login_required
async def getBalances() -> Response:
    WU = utils.getWorkspaceProfileByRequest()
    if not WU:
        return Response("Not Found Workspace Profile", status=403)
    if not WU.checkPermission("do_balance").status:
        return Response("Not enough permissions", status=403)
    module_logger.info(f"{current_user.Username} trying get balance")
    balance = createGame(WU)
    if balance["result"] == 200:
        module_logger.info(
            f"{current_user.Username} recieve balance with size {len(balance['active'])}")
    else:
        module_logger.info(f"{current_user.Username} dont recieve balances with reason {balance['status']}")
    return json.dumps(balance)
