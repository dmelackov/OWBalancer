import logging
import string
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
    print(data)
    if not validateSettings(data):
        module_logger.debug(
            f"{current_user.Username} set invalid settings data {str(data)}")
        return Response(status=400)
    current_user.setUserSettings(data)
    return Response(status=200)


settingsSchema = {"AutoCustom": bool,
                  "Autoincrement": bool,
                  "BalanceLimit": int,
                  "ExtendedLobby": bool,
                  "Network": bool,
                  "Amount": dict,
                  "TeamNames": dict}
teamCountSchema = {"T": int,
                   "D": int,
                   "H": int}
teamNameSchema = {"1": str,
                  "2": str}


def validateSettings(settings: dict):
    if set(settings.keys()) != set(settingsSchema.keys()):
        return False
    if set(settings["Amount"].keys()) != set(teamCountSchema.keys()):
        return False
    if set(settings["TeamNames"].keys()) != set(teamNameSchema.keys()):
        return False
    if not all([type(v) == settingsSchema[k] for k, v in settings.items()]):
        return False
    if not all([type(v) == teamCountSchema[k] for k, v in settings["Amount"].items()]):
        return False
    if not all([type(v) == teamNameSchema[k] for k, v in settings["TeamNames"].items()]):
        return False
    return True
