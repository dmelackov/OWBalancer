from flask import Blueprint, request, Response
from flask_login import login_required, current_user
import app.DataBase.db as MainDB
import app.DataBase.methods as DataBaseMethods
import app.DataBase.LobbyСollector as LobbyMethods
from flask import jsonify

api = Blueprint('api', __name__, template_folder='templates',
                static_folder='static')


@api.route('/getPlayers/')
@api.route('/getPlayers/<searchStr>')
@login_required
def getPlayers(searchStr=""):
    players = DataBaseMethods.searchPlayer(searchStr)
    return jsonify(list(map(lambda x: x.getJsonInfo(), players)))


@api.route('/getLobby')
@login_required
def getLobby():
    players = LobbyMethods.GetLobby(current_user.ID)
    data = list(map(lambda x: MainDB.Custom.get(
        MainDB.Custom.ID == x).getJsonInfo(), players))
    return jsonify(data)


@api.route('/getCustoms/<int:id>')
@login_required
def getCustoms(id):
    print("Custom", current_user.ID, id)
    custom = DataBaseMethods.getCustomID(current_user.ID, id)
    print(custom)
    if custom:
        data = MainDB.Custom.get(MainDB.Custom.ID == custom).getJsonInfo()
        data = {'data': data}
        data['type'] = 'custom'
        return jsonify(data)
    customs = DataBaseMethods.getCustoms_byPlayer(id)
    if customs:
        data = list(map(lambda x: MainDB.Custom.get(
            MainDB.Custom.ID == x).getJsonInfo(), customs))
        data = {'data': data}
        data['type'] = 'list'
        return jsonify(data)
    return jsonify({'status': 200, 'message': 'Customs not found', 'type': 'none'})


@api.route('/addToLobby', methods=['POST'])
@login_required
def addToLobby():
    data = request.get_json()
    print(data)
    LobbyMethods.AddToLobby(current_user.ID, data['id'])
    return jsonify({"status": 200})


@api.route('/deleteFromLobby', methods=['POST'])
@login_required
def deleteFromLobby():
    data = request.get_json()
    print(data)
    LobbyMethods.DeleteFromLobby(current_user.ID, data['id'])
    return Response(status=200)


@api.route('/setRoles', methods=['POST'])
@login_required
def setRoles():
    data = request.get_json()
    print(data)
    DataBaseMethods.changeRoles(MainDB.Custom.get(MainDB.Custom.ID == data['id']).Player.ID, data['roles'])
    return Response(status=200)