from quart import Blueprint, request, Response
import app.DataBase.db as db
from quart_login import login_required, current_user
from quart import jsonify
import logging
import app.Site.utils as utils

module_logger = logging.getLogger("api")

api = Blueprint('customs_api', __name__, template_folder='templates',
                static_folder='static')


@api.route('/getCustoms/<int:Pid>')
@login_required
def getCustoms(Pid):
    WU = utils.getWorkspaceProfileByRequest()
    if not WU:
        return Response("Not Found Workspace Profile", status=403)
    module_logger.info(f"{current_user.Username} trying to get customs for player with ID {Pid}")
    customsAF = db.Custom.get_byPlayer(Pid)
    if customsAF.data is None:
        return Response(customsAF.error, status=403)
    customList = list(map(lambda x: x.getJson(WU), customsAF.data))
    module_logger.info(f"{current_user.Username}: Returning '{len(customList)}' customs")
    return jsonify(customList)


@api.route('/changeRoleSr/<int:Cid>', methods=['PUT'])
@login_required
async def changeRoleSr(Cid) -> Response:
    WU = utils.getWorkspaceProfileByRequest()
    if not WU:
        return Response("Not Found Workspace Profile", status=403)
    if not WU.checkPermission("change_your_custom").status:
        return Response("Not enough permissions", status=403)
    data = await request.get_json()
    if not data or not Cid or not data["rating"] or not data["role"]:
        return Response("Invalid data", status=400)
    module_logger.info(
        f"{current_user.Username} trying change rating for custom({Cid}); {data['role']} to {data['rating'] }")
    if not (0 <= data["rating"] <= 5000):
        return Response("Invalid data", status=400)
    C = db.Custom.getInstance(Cid)
    if not C:
        return Response("Invalid data", status=400)
    C.changeSR(data['role'], data["rating"])
    return Response("ok", status=200)


@api.route('/createCustom', methods=['POST'])
@login_required
async def createCustom() -> Response:
    WU = utils.getWorkspaceProfileByRequest()
    if not WU:
        return Response("Not Found Workspace Profile", status=403)
    if not WU.checkPermission("create_custom").status:
        return Response("Not enough permissions", status=403)
    data = await request.get_json()
    if not data or not data["id"]:
        return Response("Invalid data", status=400)
    P = db.Player.getInstance(data["id"])
    if not P:
        return Response("Invalid data", status=400)
    module_logger.info(
        f"{current_user.Username} trying create custom for {P.Username}")  
    C = db.Custom.create(WU, P)
    if C:
        return jsonify(C.data.getJson(WU))
    else:
        return Response(C.error, status=500)
