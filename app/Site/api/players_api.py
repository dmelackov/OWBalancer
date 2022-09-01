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
@utils.WorkspaceUser
async def getPlayers(WU: db.WorkspaceProfile, searchStr: str = "") -> Response:
    module_logger.info(f"{current_user.Username} trying to get players")
    players = WU.Workspace.searchPlayers(searchStr)
    return jsonify(list(map(lambda x: x.getJson(), players)))


@api.route('/setRoles/<int:Pid>', methods=['PUT'])
@login_required
@utils.WorkspaceUser
@utils.PermsRequredOR("change_player_roles")
async def setRoles(WU: db.WorkspaceProfile, Pid: int) -> Response:
    data = request.get_json()
    if not data or "roles" not in data:
        return Response("Invalid data", status=400)
    module_logger.info(
        f"{current_user.Username} trying to set player {Pid} roles '{data['roles']}'")
    if not re.fullmatch("[TDH]?[TDH]?[TDH]?", data['roles']):
        return Response("Invalid data", status=400)
    P = db.Player.getInstance(Pid)
    if not P:
        return Response("Invalid data", status=400)
    if P.Creator.Workspace != WU.Workspace:
        return Response("Not enough permissions", status=403) 
    PR = db.PlayerRoles.getPR(WU, P).data
    if not PR:
        return Response(PR.error, status=403)
    PR.setRoles(data['roles'])
    return Response("ok", status=200)


@api.route('/setFlex/<int:Pid>', methods=['PUT'])
@login_required
@utils.WorkspaceUser
@utils.PermsRequredOR("change_player_roles")
async def setFlex(WU: db.WorkspaceProfile, Pid: int) -> Response:
    data = request.get_json()
    if not data or "status" not in data:
        return Response("Invalid data", status=400)
    module_logger.info(
        f"{current_user.Username} trying to set flex {Pid} to '{data['status']}'")
    P = db.Player.getInstance(Pid)
    if not P:
        return Response("Invalid data", status=400)
    if P.Creator.Workspace != WU.Workspace:
        return Response("Not enough permissions", status=403) 
    PR = db.PlayerRoles.getPR(WU, P).data
    if not PR:
        pass
    PR.setFlex(data['status'])
    return Response("ok", status=200)


@api.route('/createPlayer', methods=['POST'])
@login_required
@utils.WorkspaceUser
@utils.PermsRequredOR("create_player")
async def createPlayer(WU: db.WorkspaceProfile) -> Response:
    data = request.get_json()
    if not data or not data["Username"]:
        return Response("Invalid data", status=400)
    module_logger.info(
        f"{current_user.Username} trying create player {data['Username']}")
    P = db.Player.create(WU, data["Username"])
    if not P:
        return Response(P.error, status=500)
    return Response("ok", status=200)


@api.route('/deletePlayer/<int:Pid>', methods=['DELETE'])
@login_required
@utils.WorkspaceUser
@utils.PermsRequredOR(["delete_your_player", "delete_player"])
async def deletePlayer(WU: db.WorkspaceProfile, Pid: int) -> Response:
    P = db.Player.getInstance(Pid)
    if not P:
        return Response("Invalid data", status=400)
    if P.Creator.Workspace != WU.Workspace:
        return Response("Not enough permissions", status=403) 
    if P.Creator != WU and not WU.checkPermission("delete_player").status:
        return Response("Not enough permissions", status=403)
    P.delete_instance(recursive=True)
    return Response("ok", status=200)


@api.route('/changeNickname/<int:Pid>', methods=['PUT'])
@login_required
@utils.WorkspaceUser
# TODO delete_player -> change_player
@utils.PermsRequredOR(["change_your_player", "delete_player"])
async def changeNickname(WU: db.WorkspaceProfile, Pid: int) -> Response:
    data = request.get_json()
    if not data or not data["Username"]:
        return Response("Invalid data", status=400)
    P = db.Player.getInstance(Pid)
    if not P:
        return Response("Invalid data", status=400)
    if P.Creator.Workspace != WU.Workspace:
        return Response("Not enough permissions", status=403) 
    # TODO delete_player -> change_player
    if P.Creator != WU and not WU.checkPermission("delete_player").status:
        return Response("Not enough permissions", status=403)
    P.Username = data["Username"]
    P.save()
    return Response("ok", status=200)
