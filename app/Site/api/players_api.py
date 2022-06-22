from flask import Blueprint, request, Response
from flask_login import login_required, current_user
import app.DataBase.db as db
import app.Site.utils as utils
from flask import jsonify
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
        return Response(status=403)
    module_logger.info(f"{current_user.Username} trying to get players")
    players = db_methods.searchPlayer(searchStr) # Жду метода
    return jsonify(list(map(lambda x: x.getJson(), players)))


@api.route('/setRoles', methods=['POST'])
@login_required
async def setRoles() -> Response:
    WU = utils.getWorkspaceProfileByRequest()
    if not WU:
        return Response(status=403)
    if not WU.checkPermission("change_player_roles").status:
        return Response(status=403)
    data = request.get_json()
    module_logger.info(
        f"{current_user.Username} trying to set player {data['id']} roles '{data['roles']}'")
    if not re.fullmatch("[TDH]?[TDH]?[TDH]?", data['roles']):
        return Response(status=400)
    P = db.Player.getInstance(data["id"])
    if not P:
        return Response(status=400)
    PR = db.PlayerRoles.getPR(WU, P).data
    if not PR:
        return
    PR.setRole(data['roles'])
    return Response(status=200)


@api.route('/setFlex', methods=['POST'])
@login_required
async def setFlex() -> Response:
    WU = utils.getWorkspaceProfileByRequest()
    if not WU:
        return Response(status=403)
    if not WU.checkPermission("change_player_roles").status:
        return Response(status=403)
    data = request.get_json()
    module_logger.info(
        f"{current_user.Username} trying to set flex {data['id']} to '{data['status']}'")
    P = db.Player.getInstance(data["id"])
    if not P:
        return Response(status=400)
    PR = db.PlayerRoles.getPR(WU, P).data
    if not PR:
        pass
    PR.setFlex(data['status'])
    return Response(status=200)


@api.route('/createPlayer', methods=['POST'])
@login_required
async def createPlayer() -> Response:
    WU = utils.getWorkspaceProfileByRequest()
    if not WU:
        return Response(status=403)
    if not WU.checkPermission("create_player").status:
        return Response(status=403)
    data = request.get_json()
    if not data or not data["Username"]:
        return Response(status=400)
    module_logger.info(
        f"{current_user.Username} trying create player {data['Username']}")
    if not db.Player.create(WU, data["Username"]):
        return Response(status=500)
    return Response(status=200)
