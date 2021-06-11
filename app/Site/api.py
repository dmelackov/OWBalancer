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
    data = list(map(lambda x: MainDB.Custom.get(MainDB.Custom.ID == x).getJsonInfo(), players))
    return jsonify(data)

@api.route('/addToLobby', methods=['POST'])
@login_required
def addToLobby():
    data = request.get_json()
    print(data)
    return jsonify({"status": 200})

@api.route('/deleteFromLobby', methods=['POST'])
@login_required
def deleteFromLobby():
    data = request.get_json()
    print(data)
    LobbyMethods.DeleteFromLobby(current_user.ID, data['id'])
    return Response(status=200)