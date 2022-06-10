from flask import Blueprint, request, Response
from flask_login import login_required, current_user
import app.DataBase.db as db
import app.DataBase.LobbyСollector as LobbyMethods
from flask import jsonify
import logging
from app.DataBase.methods.roles import checkProfilePermission

module_logger = logging.getLogger("api")

api = Blueprint('lobby_api', __name__, template_folder='templates',
                static_folder='static')


@api.route('/getLobby')
@login_required
def getLobby():
    module_logger.info(f"{current_user.Username} trying to get lobby")
    players = current_user.getLobbyInfo()
    data = [i.getJson(current_user) for i in db.Custom.select().where(db.Custom.ID << players)]
    for PData in data:
        if PData['Creator']['ID'] == current_user.ID:
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
def addToLobby():
    if not checkProfilePermission(current_user, "add_customs_tolobby"):
        return jsonify({"status": 403})
    data = request.get_json()
    module_logger.info(
        f"{current_user.Username} trying add to lobby custom with id {data['id']}")
    LobbyMethods.AddToLobby(current_user, data['id'])
    return jsonify({"status": 200})


@api.route('/deleteFromLobby', methods=['POST'])
@login_required
def deleteFromLobby():
    if not checkProfilePermission(current_user, "add_customs_tolobby"):
        return jsonify({"status": 403})
    data = request.get_json()
    module_logger.info(
        f"{current_user.Username} trying delete from lobby custom with id {data['id']}")
    LobbyMethods.DeleteFromLobby(current_user, data['id'])
    return Response(status=200)


@api.route('/clearLobby', methods=['POST'])
@login_required
def clearLobby():
    if not checkProfilePermission(current_user, "add_customs_tolobby"):
        return jsonify({"status": 403})
    module_logger.info(f"{current_user.Username} trying clear lobby")
    current_user.updateLobbyInfo([])
    # LobbyMethods.ClearLobby(current_user.ID)
    return Response(status=200)
