from flask import Blueprint, request, Response
from flask_login import login_required, current_user
import app.DataBase.db as db
from flask import jsonify
import logging
import app.Site.utils as utils

module_logger = logging.getLogger("api")

api = Blueprint('lobby_api', __name__, template_folder='templates',
                static_folder='static')


@api.route('/getLobby')
@login_required
@utils.WorkspaceUser
async def getLobby(WU: db.WorkspaceProfile) -> Response:
    module_logger.info(f"{current_user.Username} trying to get lobby")
    players = WU.getLobbyInfo()
    data = [db.Custom.getInstance(i).getJson(WU) for i in players]
    return jsonify(data)


@api.route('/addToLobby/<int:Cid>', methods=['POST'])
@login_required
@utils.WorkspaceUser
@utils.PermsRequredOR("add_customs_tolobby")
async def addToLobby(WU: db.WorkspaceProfile, Cid: int) -> Response:
    module_logger.info(
        f"{current_user.Username} trying add to lobby custom with id {Cid}")
    C = db.Custom.getInstance(Cid)
    if not C:
        return Response("Invalid data", status=403)
    af = WU.addToLobby(C)
    if af.status:
        return Response("ok", status=200)
    else:
        return Response(af.error, status=400)


@api.route('/deleteFromLobby/<int:Cid>', methods=['DELETE'])
@login_required
@utils.WorkspaceUser
@utils.PermsRequredOR("add_customs_tolobby")
async def deleteFromLobby(WU: db.WorkspaceProfile, Cid: int) -> Response:
    module_logger.info(
        f"{current_user.Username} trying delete from lobby custom with id {Cid}")
    C = db.Custom.getInstance(Cid)
    if C:
        WU.DeleteFromLobby(C)
        return Response("ok", status=200)
    else:
        return Response("Invalid data", status=403)


@api.route('/clearLobby', methods=['DELETE'])
@login_required
@utils.WorkspaceUser
@utils.PermsRequredOR("add_customs_tolobby")
async def clearLobby(WU: db.WorkspaceProfile) -> Response:
    module_logger.info(f"{current_user.Username} trying clear lobby")
    WU.ClearLobby()
    return Response("ok", status=200)
