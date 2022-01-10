import logging
from flask import Blueprint, request, Response, send_file, jsonify
from flask_login import login_required, current_user

module_logger = logging.getLogger("api")

api = Blueprint('settings_api', __name__, template_folder='templates',
                static_folder='static')


@api.route('/getSettings', methods=['GET'])
@login_required
def getSettings():
    return jsonify(current_user.getUserSettings())

@api.route('/setSettings', methods=['POST'])
@login_required
def setSetting():
    data = request.get_json()
    if data.get("setting", None) is None:
        return Response(status=400)
    if data.get("value", None) is None:
        return Response(status=400)
    if type(data["setting"]) != str:
        module_logger.debug(f"{current_user.Username} set invalid settings data {str(data)}")
        return Response(status=400)
    if data["setting"] == "AutoCustom":
        if type(data["value"]) != bool:
            module_logger.debug(f"{current_user.Username} set invalid settings data {str(data)}")
            return Response(status=400)
        current_user.settingsAutoCustom(data["value"])
    return Response(status=200)


@api.route('/setTanksCount', methods=['POST'])
@login_required
def setTanksCount():
    data = request.get_json()
    if data.get("setting", None) is None:
        return Response(status=400)
    if type(data["setting"]) != int:
        module_logger.debug(str(data))
        return Response(status=400)
    current_user.settingsChangeTanks(data["setting"])
    return Response(status=200)


@api.route('/setDamageCount', methods=['POST'])
@login_required
def setDamageCount():
    data = request.get_json()
    if data.get("setting", None) is None:
        return Response(status=400)
    if type(data["setting"]) != int:
        module_logger.debug(str(data))
        return Response(status=400)
    current_user.settingsChangeDps(data["setting"])
    return Response(status=200)


@api.route('/setHealsCount', methods=['POST'])
@login_required
def setHealsCount():
    data = request.get_json()
    if data.get("setting", None) is None:
        return Response(status=400)
    if type(data["setting"]) != int:
        module_logger.debug(str(data))
        return Response(status=400)
    current_user.settingsChangeHeal(data["setting"])
    return Response(status=200)


@api.route('/setTeamName1', methods=['POST'])
@login_required
def setTeamName1():
    data = request.get_json()
    print(data)
    if data.get("setting", None) is None:
        return Response(status=400)
    if type(data["setting"]) != str:
        module_logger.debug(str(data))
        return Response(status=400)
    current_user.settingsTeamOne(data["setting"])
    return Response(status=200)


@api.route('/setTeamName2', methods=['POST'])
@login_required
def setTeamName2():
    data = request.get_json()
    if data.get("setting", None) is None:
        return Response(status=400)
    if type(data["setting"]) != str:
        module_logger.debug(str(data))
        return Response(status=400)
    current_user.settingsTeamTwo(data["setting"])
    return Response(status=200)


@api.route('/setAutoCustom', methods=['POST'])
@login_required
def setAutoCustom():
    data = request.get_json()
    if data.get("setting", None) is None:
        return Response(status=400)
    if type(data["setting"]) != bool:
        module_logger.debug(str(data))
        return Response(status=400)
    current_user.settingsAutoCustom(data["setting"])
    return Response(status=200)


@api.route('/setExtendedLobby', methods=['POST'])
@login_required
def setExtendedLobby():
    data = request.get_json()
    if data.get("setting", None) is None:
        return Response(status=400)
    if type(data["setting"]) != bool:
        module_logger.debug(str(data))
        return Response(status=400)
    current_user.settingsExtendedLobby(data["setting"])
    return Response(status=200)
