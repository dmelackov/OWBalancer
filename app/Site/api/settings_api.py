from typing import Union
import logging
from flask import Blueprint, request, Response, jsonify
from flask_login import login_required, current_user

module_logger = logging.getLogger("api")

api = Blueprint('settings_api', __name__, template_folder='templates',
                static_folder='static')


@api.route('/getSettings', methods=['GET'])
@login_required
async def getSettings() -> Response:
    return jsonify(current_user.getUserSettings())


@api.route('/setSettings', methods=['POST'])
@login_required
async def setSetting() -> Response:
    data = request.get_json()
    if not validateSettings(data):
        module_logger.debug(
            f"{current_user.Username} set invalid settings data {str(data)}")
        return Response(status=400)
    current_user.setUserSettings(data)
    return Response(status=200)


NumberTypes = (int, float)

settingsSchema = {"AutoCustom": bool,
                  "Autoincrement": bool,
                  "BalanceLimit": int,
                  "ExtendedLobby": bool,
                  "ExpandedResult": bool,
                  "Amount": dict,
                  "TeamNames": dict,
                  "fColor": str,
                  "sColor": str,
                  "Math": dict}
teamCountSchema = {"T": int,
                   "D": int,
                   "H": int}
teamNameSchema = {"1": str,
                  "2": str}
mathSchema = {
    "alpha": NumberTypes,
    "beta": NumberTypes,
    "gamma": NumberTypes,
    "p": NumberTypes,
    "q": NumberTypes,
    "tWeight": NumberTypes,
    "dWeight": NumberTypes,
    "hWeight": NumberTypes
}


def validateSettings(settings: dict[str, Union[int, bool, dict, str]]) -> bool:
    if set(settings.keys()) != set(settingsSchema.keys()):
        module_logger.debug("Main keys error")
        return False
    if set(settings["Amount"].keys()) != set(teamCountSchema.keys()):
        module_logger.debug("Amount keys error")
        return False
    if set(settings["TeamNames"].keys()) != set(teamNameSchema.keys()):
        module_logger.debug("TeamNames keys error")
        return False
    if set(settings["Math"].keys()) != set(mathSchema.keys()):
        module_logger.debug("Math keys error")
        return False
    if not all([isinstance(v, settingsSchema[k]) for k, v in settings.items()]):
        module_logger.debug("Main types error")
        return False
    if not all([isinstance(v, teamCountSchema[k]) for k, v in settings["Amount"].items()]):
        module_logger.debug("Amount types error")
        return False
    if not all([isinstance(v, teamNameSchema[k]) for k, v in settings["TeamNames"].items()]):
        module_logger.debug("TeamNames types error")
        return False
    if not all([isinstance(v, mathSchema[k]) for k, v in settings["Math"].items()]):
        module_logger.debug("Math types error")
        return False
    return True
