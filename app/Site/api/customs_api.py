from flask import Blueprint, request, Response
from flask_login import login_required, current_user
import app.DataBase.db as db
import app.DataBase.methods as db_methods
import app.DataBase.LobbyСollector as LobbyMethods
from flask import jsonify
import logging
from app.DataBase.RolesMethods import checkProfilePermission

module_logger = logging.getLogger("api")

api = Blueprint('customs_api', __name__, template_folder='templates',
                static_folder='static')


@api.route('/getCustoms/<int:id>')
@login_required
def getCustoms(Pid):
    module_logger.info(f"{current_user.Username} trying to get customs")
    if current_user.getUserSettings()["AutoCustom"]:
        Cid = db_methods.getCustomID(current_user.ID, Pid)
        if Cid:
            C = db.Custom.get(db.Custom.ID == Cid).getJson(current_user)
            data = {'data': C, 'type': 'custom'}
            module_logger.info(
                f"{current_user.Username}: Custom returning type '{data['type']}'")
            return jsonify(data)
    else:
        customs = db_methods.getCustoms_byPlayer(Pid)
        if customs:
            data = {'data': customs, 'type': 'list'}
            module_logger.info(
                f"{current_user.Username}: Custom returning type '{data['type']}'")
            return jsonify(data)
    module_logger.info(
        f"{current_user.Username}: Custom returning type 'none'")
    return jsonify({'status': 200, 'message': 'Customs not found', 'type': 'none'})


@api.route('/changeRoleSr', methods=['POST'])
@login_required
def changeRoleSr():
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
def createCustom():
    if not checkProfilePermission(current_user, "create_custom"):
        return jsonify({"status": 403})
    data = request.get_json()
    C = db_methods.createCustom(current_user, data["id"])
    module_logger.info(
        f"{current_user.Username} trying create custom for {C.Player.Username}")
    LobbyMethods.AddToLobby(current_user, C.ID)
    return Response(status=200)
