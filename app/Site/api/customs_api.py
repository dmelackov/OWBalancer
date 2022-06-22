from flask import Blueprint, request, Response
import app.DataBase.db as db
import app.DataBase.methods.methods as db_methods
import app.DataBase.LobbyСollector as LobbyMethods
from flask_login import login_required, current_user
from flask import jsonify
import logging
from app.DataBase.methods.roles import checkProfilePermission

module_logger = logging.getLogger("api")

api = Blueprint('customs_api', __name__, template_folder='templates',
                static_folder='static')


@api.route('/getCustoms/<int:Pid>')
@login_required
def getCustoms(Pid):
    module_logger.info(f"{current_user.Username} trying to get customs for player with ID {Pid}")
    customs = db_methods.getCustoms_byPlayer(Pid)
    customList = []
    if customs:
        customList = list(map(lambda x: x.getJson(current_user), customs))
    module_logger.info(f"{current_user.Username}: Returning '{len(customList)}'")
    return jsonify(customList)


@api.route('/changeRoleSr', methods=['POST'])
@login_required
async def changeRoleSr() -> Response:
    if not checkProfilePermission(current_user, "change_your_custom"):
        return jsonify({"status": 403})
    data = request.get_json()
    module_logger.debug(data)
    data["customId"] = int(data["customId"])
    data["rating"] = int(data["rating"])
    module_logger.info(
        f"{current_user.Username} trying change rating for custom({data['customId']}); {data['role']} to {data['rating'] }")
    if not (0 <= data["rating"] <= 5000):
        return Response(status=200)
    if data['role'] == "T":
        db_methods.changeCustomSR_Tank(data["customId"], data["rating"])
    elif data['role'] == "D":
        db_methods.changeCustomSR_Dps(data["customId"], data["rating"])
    elif data['role'] == "H":
        db_methods.changeCustomSR_Heal(data["customId"], data["rating"])
    return Response(status=200)


@api.route('/createCustom', methods=['POST'])
@login_required
async def createCustom() -> Response:
    if not checkProfilePermission(current_user, "create_custom"):
        return jsonify({"status": 403})
    data = request.get_json()
    C = db_methods.createCustom(current_user, data["id"])
    module_logger.info(
        f"{current_user.Username} trying create custom for {C.Player.Username}")
    LobbyMethods.AddToLobby(current_user, C.ID)
    return Response(status=200)
