from flask import Blueprint, request, Response
from flask_login import login_required, current_user
import app.DataBase.db as MainDB
import app.DataBase.methods as DataBaseMethods
from flask import jsonify
import logging
import re
from app.DataBase.RolesMethods import checkProfilePermission

module_logger = logging.getLogger("api")

api = Blueprint('players_api', __name__, template_folder='templates',
                static_folder='static')


@api.route('/getPlayers/')
@api.route('/getPlayers/<searchStr>')
@login_required
def getPlayers(searchStr=""):
    module_logger.info(f"{current_user.Username} trying to get players")
    players = DataBaseMethods.searchPlayer(searchStr)
    return jsonify(list(map(lambda x: x.getJsonInfo(), players)))


@api.route('/setRoles', methods=['POST'])
@login_required
def setRoles():
    if not checkProfilePermission(current_user, "change_player_roles"):
        return jsonify({"status": 403})
    data = request.get_json()
    module_logger.info(
        f"{current_user.Username} trying to set custom {data['id']} roles '{data['roles']}'")
    if(not re.fullmatch("[TDH]?[TDH]?[TDH]?", data['roles'])):
        return Response(status=200)
    DataBaseMethods.changeRoles(MainDB.Custom.get(
        MainDB.Custom.ID == data['id']).Player.ID, data['roles'])
    return Response(status=200)


@api.route('/setFlex', methods=['POST'])
@login_required
def setFlex():
    if not checkProfilePermission(current_user, "change_player_roles"):
        return jsonify({"status": 403})
    data = request.get_json()
    module_logger.info(
        f"{current_user.Username} trying to set flex {data['id']} to '{data['status']}'")
    DataBaseMethods.confirmFlex(MainDB.Custom.get(
        MainDB.Custom.ID == data['id']).Player.ID, bool(data['status']))
    return Response(status=200)


@api.route('/createPlayer', methods=['POST'])
@login_required
def createPlayer():
    if not checkProfilePermission(current_user, "create_player"):
        return jsonify({"status": 403})
    data = request.get_json()
    module_logger.info(
        f"{current_user.Username} trying create player {data['Username']}")
    DataBaseMethods.createPlayer(data["Username"], current_user)
    return Response(status=200)
