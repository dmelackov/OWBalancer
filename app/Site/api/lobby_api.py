from flask import Blueprint, request, Response
from flask_login import login_required, current_user
import app.DataBase.db as MainDB
import app.DataBase.LobbyСollector as LobbyMethods
from flask import jsonify
import logging
from app.DataBase.RolesMethods import checkProfilePermission

module_logger = logging.getLogger("api")

api = Blueprint('lobby_api', __name__, template_folder='templates',
                static_folder='static')


@api.route('/getLobby')
@login_required
def getLobby():
    module_logger.info(f"{current_user.Username} trying to get lobby")
    players = current_user.getLobbyInfo()
    Cs = MainDB.Custom.select().where(MainDB.Custom.ID << players)
    data = [Cs[i].getJsonInfo() for i in range(len(players))]
    for i in data:
        if i['Author']['id'] == current_user.ID:
            i['editable'] = True
        else:
            i['editable'] = False
        if (i["SR"]["Damage"] == 0 and i["SR"]["Heal"] == 0 and i["SR"]["Tank"] == 0) \
                or (not i["Roles"]["Damage"] and not i["Roles"]["Heal"] and not i["Roles"]["Tank"]):
            i["warn"] = True
        else:
            i["warn"] = False
    return jsonify(data)


@api.route('/addToLobby', methods=['POST'])
@login_required
def addToLobby():
    if not checkProfilePermission(current_user, "add_customs_tolobby"):
        return jsonify({"status": 403})
    data = request.get_json()
    module_logger.info(
        f"{current_user.Username} trying add to lobby custom with id {data['id']}")
    LobbyMethods.AddToLobby(current_user.ID, data['id'])
    return jsonify({"status": 200})


@api.route('/deleteFromLobby', methods=['POST'])
@login_required
def deleteFromLobby():
    if not checkProfilePermission(current_user, "add_customs_tolobby"):
        return jsonify({"status": 403})
    data = request.get_json()
    module_logger.info(
        f"{current_user.Username} trying delete from lobby custom with id {data['id']}")
    LobbyMethods.DeleteFromLobby(current_user.ID, data['id'])
    return Response(status=200)


@api.route('/clearLobby', methods=['POST'])
@login_required
def clearLobby():
    if not checkProfilePermission(current_user, "add_customs_tolobby"):
        return jsonify({"status": 403})
    module_logger.info(f"{current_user.Username} trying clear lobby")
    LobbyMethods.ClearLobby(current_user.ID)
    return Response(status=200)
