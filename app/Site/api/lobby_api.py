from quart import Blueprint, request, Response
from quart_login import login_required, current_user
import app.DataBase.db as db
import app.DataBase.LobbyСollector as LobbyMethods
from quart import jsonify
import logging
import app.Site.utils as utils

module_logger = logging.getLogger("api")

api = Blueprint('lobby_api', __name__, template_folder='templates',
                static_folder='static')


@api.route('/getLobby')
@login_required
async def getLobby() -> Response:
    WU = utils.getWorkspaceProfileByRequest()
    if not WU:
        return Response("Not Found Workspace Profile", status=403)
    module_logger.info(f"{current_user.Username} trying to get lobby")
    players = WU.getLobbyInfo()
    data = [db.Custom.getInstance(i).getJson(WU) for i in players]
    for PData in data:
        if PData['Creator']['ID'] == WU.ID:
            PData['editable'] = True
        else:
            PData['editable'] = False
        if not sum([1 if PData["Roles"][i]["sr"] else 0 for i in range(3)]) or \
                not sum([PData["Roles"][i]["active"] for i in range(3)]):
            PData["warn"] = True
        else:
            PData["warn"] = False
    return jsonify(data)


@api.route('/addToLobby', methods=['POST'])
@login_required
async def addToLobby() -> Response:
    WU = utils.getWorkspaceProfileByRequest()
    if not WU:
        return Response("Not Found Workspace Profile", status=403)
    if not WU.checkPermission("add_customs_tolobby").status:
        return Response("Not enough permissions", status=403)
    data = await request.get_json()
    if not data or not data["id"]:
        return Response("Invalid data", status=400)
    module_logger.info(
        f"{current_user.Username} trying add to lobby custom with id {data['id']}")
    af = WU.addToLobby(data['id'])
    if af.status:
        return Response("ok", status=200)
    else:
        return Response(af.error, status=400)


@api.route('/deleteFromLobby', methods=['POST'])
@login_required
async def deleteFromLobby() -> Response:
    WU = utils.getWorkspaceProfileByRequest()
    if not WU:
        return Response("Not Found Workspace Profile", status=403)
    if not WU.checkPermission("add_customs_tolobby").status:
        return Response("Not enough permissions", status=403)
    data = await request.get_json()
    module_logger.info(
        f"{current_user.Username} trying delete from lobby custom with id {data['id']}")
    LobbyMethods.DeleteFromLobby(current_user, data['id']) # TODO
    return Response("ok", status=200)


@api.route('/clearLobby', methods=['POST'])
@login_required
async def clearLobby() -> Response:
    WU = utils.getWorkspaceProfileByRequest()
    if not WU:
        return Response("Not Found Workspace Profile", status=403)
    if not WU.checkPermission("add_customs_tolobby").status:
        return Response("Not enough permissions", status=403)
    module_logger.info(f"{current_user.Username} trying clear lobby")
    WU.updateLobbyInfo([]) # TODO change to method clearLobby
    return Response("ok", status=200)
