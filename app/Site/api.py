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
import logging
import re
from app.DataBase.RolesMethods import checkProfilePermission, getUserPermissions
module_logger = logging.getLogger("api")

api = Blueprint('api', __name__, template_folder='templates',
                static_folder='static')



@api.route('/getPlayers/')
@api.route('/getPlayers/<searchStr>')
@login_required
def getPlayers(searchStr=""):
    module_logger.info(f"{current_user.Username} trying to get players")
    players = DataBaseMethods.searchPlayer(searchStr)
    return jsonify(list(map(lambda x: x.getJsonInfo(), players)))


@api.route('/getLobby')
@login_required
def getLobby():
    module_logger.info(f"{current_user.Username} trying to get lobby")
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
    module_logger.info(f"{current_user.Username} trying to get customs")
    custom = DataBaseMethods.getCustomID(current_user.ID, id)
    if custom:
        data = MainDB.Custom.get(MainDB.Custom.ID == custom).getJsonInfo()
        data = {'data': data}
        data['type'] = 'custom'
        module_logger.info(f"{current_user.Username}: Custom returning type '{data['type']}'")
        return jsonify(data)
    customs = DataBaseMethods.getCustoms_byPlayer(id)
    if customs:
        data = list(map(lambda x: MainDB.Custom.get(
            MainDB.Custom.ID == x).getJsonInfo(), customs))
        data = {'data': data}
        data['type'] = 'list'
        module_logger.info(f"{current_user.Username}: Custom returning type '{data['type']}'")
        return jsonify(data)
    module_logger.info(f"{current_user.Username}: Custom returning type 'none'")
    return jsonify({'status': 200, 'message': 'Customs not found', 'type': 'none'})


@api.route('/addToLobby', methods=['POST'])
@login_required
def addToLobby():
    if not checkProfilePermission(current_user, "add_customs_tolobby"):
        return jsonify({"status": 403})
    data = request.get_json()
    module_logger.info(f"{current_user.Username} trying add to lobby custom with id {data['id']}")
    LobbyMethods.AddToLobby(current_user.ID, data['id'])
    return jsonify({"status": 200})


@api.route('/deleteFromLobby', methods=['POST'])
@login_required
def deleteFromLobby():
    if not checkProfilePermission(current_user, "add_customs_tolobby"):
        return jsonify({"status": 403})
    data = request.get_json()
    module_logger.info(f"{current_user.Username} trying delete from lobby custom with id {data['id']}")
    LobbyMethods.DeleteFromLobby(current_user.ID, data['id'])
    return Response(status=200)


@api.route('/setRoles', methods=['POST'])
@login_required
def setRoles():
    if not checkProfilePermission(current_user, "change_player_roles"):
        return jsonify({"status": 403})
    data = request.get_json()
    module_logger.info(f"{current_user.Username} trying to set custom {data['id']} roles '{data['roles']}'")
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
    module_logger.info(f"{current_user.Username} trying to set flex {data['id']} to '{data['status']}'")
    DataBaseMethods.confirmFlex(MainDB.Custom.get(
        MainDB.Custom.ID == data['id']).Player.ID, bool(data['status']))
    return Response(status=200)


@api.route('/balanceImage', methods=['POST'])
@login_required
def balanceImage():
    module_logger.info(f"{current_user.Username} trying get balance image'")
    data = request.get_json()
    return serve_pil_image(createImage(data, current_user))


@api.route('/changeRoleSr', methods=['POST'])
@login_required
def changeRoleSr():
    if not checkProfilePermission(current_user, "change_your_custom"):
        return jsonify({"status": 403})
    data = request.get_json()
    module_logger.debug(data)
    data["customId"] = int(data["customId"])
    data["rating"] = int(data["rating"])
    module_logger.info(f"{current_user.Username} trying change rating for custom({data['customId']}); {data['role']} to {data['rating'] }")
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
    if not checkProfilePermission(current_user, "do_balance"):
        return jsonify({"status": 403})
    module_logger.info(f"{current_user.Username} trying get balance")
    balance = createGame(current_user.ID)
    newBalance = {}
    if balance:
        newBalance["External"] = balance[0]
        newBalance["Balances"] = balance[1][:5000]
        newBalance["ok"] = True
        module_logger.info(f"{current_user.Username} recieve balance with size {len(newBalance['Balances'])}")
    else:
        newBalance["ok"] = False
        module_logger.info(f"{current_user.Username} dont recieve balances")
    return json.dumps(newBalance)


@api.route('/createCustom', methods=['POST'])
@login_required
def createCustom():
    if not checkProfilePermission(current_user, "create_custom"):
        return jsonify({"status": 403})
    data = request.get_json()
    C = DataBaseMethods.createCustom(current_user.ID, data["id"])
    module_logger.info(f"{current_user.Username} trying create custom for {C.Player.Username}")
    LobbyMethods.AddToLobby(current_user.ID, C.ID)
    return Response(status=200)


@api.route('/createPlayer', methods=['POST'])
@login_required
def createPlayer():
    if not checkProfilePermission(current_user, "create_player"):
        return jsonify({"status": 403})
    data = request.get_json()
    module_logger.info(f"{current_user.Username} trying create player {data['Username']}")
    DataBaseMethods.createPlayer(data["Username"], current_user)
    return Response(status=200)


@api.route('/clearLobby', methods=['POST'])
@login_required
def clearLobby():
    if not checkProfilePermission(current_user, "add_customs_tolobby"):
        return jsonify({"status": 403})
    module_logger.info(f"{current_user.Username} trying clear lobby")
    LobbyMethods.ClearLobby(current_user.ID)
    return Response(status=200)


@api.route('/getPermissions', methods=['GET'])
@login_required
def getPermissions():
    module_logger.info(f"{current_user.Username} trying get permissions")
    perms = list(map(lambda x: x.Name, getUserPermissions(current_user)))
    return jsonify(perms)



def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, format='JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')
