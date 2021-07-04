from flask import Blueprint, request, Response, send_file
from flask_login import login_required, current_user
import app.DataBase.db as MainDB
import app.DataBase.methods as DataBaseMethods
import app.DataBase.LobbyСollector as LobbyMethods
from flask import jsonify
from app.Calculation.PILBalance import createImage
from app.Calculation.GameBalance import createGame
from io import BytesIO
import json

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
    DataBaseMethods.changeRoles(MainDB.Custom.get(
        MainDB.Custom.ID == data['id']).Player.ID, data['roles'])
    return Response(status=200)


@api.route('/balanceImage', methods=['POST'])
@login_required
def balanceImage():
    data = request.get_json()
    print(data)
    return serve_pil_image(createImage(data))


@api.route('/changeRoleSr', methods=['POST'])
@login_required
def changeRoleSr():
    data = request.get_json()
    data["customId"] = int(data["customId"])
    data["rating"] = int(data["rating"])
    if not (0 <= data["rating"] <= 5000):
        return Response(status=200)
    if (data['role'] == "T"):
        DataBaseMethods.changeCustomSR_Tank(data["customId"], data["rating"])
    elif (data['role'] == "D"):
        DataBaseMethods.changeCustomSR_Dps(data["customId"], data["rating"])
    elif (data['role'] == "H"):
        DataBaseMethods.changeCustomSR_Heal(data["customId"], data["rating"])
    return Response(status=200)


@api.route('/getBalances', methods=['GET'])
@login_required
def getBalances():
    balance = createGame(current_user.ID)
    newBalance = {}
    if balance:
        newBalance["External"] = balance[0]
        newBalance["Balances"] = balance[1][:5000]
        newBalance["ok"] = True
    else:
        newBalance["ok"] = False
    return json.dumps(newBalance)


@api.route('/createCustom', methods=['POST'])
@login_required
def createCustom():
    data = request.get_json()
    print(data)
    C = DataBaseMethods.createCustom(current_user.ID, data["id"])
    LobbyMethods.AddToLobby(current_user.ID, C.ID)
    return Response(status=200)


def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, format='JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')
