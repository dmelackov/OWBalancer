from quart import Blueprint, request, Response
from quart_login import login_required, current_user
import app.DataBase.db as db
import app.Site.utils as utils
from quart import jsonify
import logging
import re

module_logger = logging.getLogger("api")

api = Blueprint('players_api', __name__, template_folder='templates',
                static_folder='static')


@api.route('/getPlayers/')
@api.route('/getPlayers/<searchStr>')
@login_required
async def getPlayers(searchStr: str = "") -> Response:
    WU = utils.getWorkspaceProfileByRequest()
    if not WU:
        return Response("Not Found Workspace Profile", status=403)
    module_logger.info(f"{current_user.Username} trying to get players")
    players = WU.Workspace.searchPlayers(searchStr)
    return jsonify(list(map(lambda x: x.getJson(), players)))


@api.route('/setRoles/<int:Pid>', methods=['PUT'])
@login_required
async def setRoles(Pid) -> Response:
    WU = utils.getWorkspaceProfileByRequest()
    if not WU:
        return Response("Not Found Workspace Profile", status=403)
    if not WU.checkPermission("change_player_roles").status:
        return Response("Not enough permissions", status=403)
    data = await request.get_json()
    if not data or not data["roles"]:
        return Response("Invalid data", status=400)
    module_logger.info(
        f"{current_user.Username} trying to set player {Pid} roles '{data['roles']}'")
    if not re.fullmatch("[TDH]?[TDH]?[TDH]?", data['roles']):
        return Response("Invalid data", status=400)
    P = db.Player.getInstance(Pid)
    if not P:
        return Response("Invalid data", status=400)
    PR = db.PlayerRoles.getPR(WU, P).data
    if not PR:
        return Response(PR.error, status=403)
    PR.setRoles(data['roles'])
    return Response("ok", status=200)


@api.route('/setFlex/<int:Pid>', methods=['PUT'])
@login_required
async def setFlex(Pid) -> Response:
    WU = utils.getWorkspaceProfileByRequest()
    if not WU:
        return Response("Workspace Profile Not Found", status=403)
    if not WU.checkPermission("change_player_roles").status:
        return Response("Not enough permissions", status=403)
    data = await request.get_json()
    if not data or data.get("status", None) is None:
        return Response("Invalid data", status=400)
    module_logger.info(
        f"{current_user.Username} trying to set flex {Pid} to '{data['status']}'")
    P = db.Player.getInstance(Pid)
    if not P:
        return Response("Invalid data", status=400)
    PR = db.PlayerRoles.getPR(WU, P).data
    if not PR:
        pass
    PR.setFlex(data['status'])
    return Response("ok", status=200)


@api.route('/createPlayer', methods=['POST'])
@login_required
async def createPlayer() -> Response:
    WU = utils.getWorkspaceProfileByRequest()
    if not WU:
        return Response("Not Found Workspace Profile", status=403)
    if not WU.checkPermission("create_player").status:
        return Response("Not enough permissions", status=403)
    data = await request.get_json()
    if not data or not data["Username"]:
        return Response("Invalid data", status=400)
    module_logger.info(
        f"{current_user.Username} trying create player {data['Username']}")
    P = db.Player.create(WU, data["Username"])
    if not P:
        return Response(P.error, status=500)
    return Response("ok", status=200)
