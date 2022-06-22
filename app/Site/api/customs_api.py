from flask import Blueprint, request, Response
import app.DataBase.db as db
import app.DataBase.LobbyСollector as LobbyMethods
from flask_login import login_required, current_user
from flask import jsonify
import logging
import app.Site.utils as utils

module_logger = logging.getLogger("api")

api = Blueprint('customs_api', __name__, template_folder='templates',
                static_folder='static')


@api.route('/getCustoms/<int:Pid>')
@login_required
def getCustoms(Pid):
    WU = utils.getWorkspaceProfileByRequest()
    if not WU:
        return Response(status=403)
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
    WU = utils.getWorkspaceProfileByRequest()
    if not WU:
        return Response(status=403)
    if not WU.checkPermission("change_your_custom").status:
        return Response(status=403)
    data = request.get_json()
    if not data or not data["customId"] or not data["rating"] or not data["role"]:
        return Response(status=400)
    module_logger.info(
        f"{current_user.Username} trying change rating for custom({data['customId']}); {data['role']} to {data['rating'] }")
    if not (0 <= data["rating"] <= 5000):
        return Response(status=400)
    C = db.Custom.getInstance(data["customId"])
    if not C:
        return Response(status=400)
    C.changeSR(data['role'], data["rating"])
    return Response(status=200)


@api.route('/createCustom', methods=['POST'])
@login_required
async def createCustom() -> Response:
    WU = utils.getWorkspaceProfileByRequest()
    if not WU:
        return Response(status=403)
    if not WU.checkPermission("create_custom").status:
        return Response(status=403)
    data = request.get_json()
    if not data or not data["id"]:
        return Response(status=400)
    P = db.Player.getInstance(data["id"])
    if not P:
        return Response(status=400)
    module_logger.info(
        f"{current_user.Username} trying create custom for {P.Username}")  
    C = db.Custom.create(WU, P)
    LobbyMethods.AddToLobby(current_user, C.ID) # Жду новых методов
    return Response(status=200)
