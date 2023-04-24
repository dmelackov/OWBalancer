from flask import Blueprint, Response, request
from flask import jsonify
import logging
from flask_login import current_user, login_required
import app.DataBase.db as db
import json 
import app.Site.utils as utils

module_logger = logging.getLogger("api")

api = Blueprint('workspace_api', __name__, template_folder='templates',
                static_folder='static')


@api.route("/setWorkspace/<int:Wid>", methods=["PUT"])
@login_required
async def setWorkspace(Wid):
    W = db.Workspace.getInstance(Wid)
    if not W:
        return Response("Instance Not Exist", status=404)
    res = Response("ok", status=200)
    res.set_cookie("workspace", str(W.ID), max_age=60*60*24*365)
    return res


@api.route("/getWorkspace/<int:ID>")
@login_required
async def getWorkspace(ID):
    W = db.Workspace.getInstance(ID)
    return W.getJson()    


@api.route("/getWorkspaces")
@login_required
async def getWorkspaces():
    Wl = current_user.getWorkspaceList().data
    Wljson = [i.getJson() for i in Wl]
    return jsonify(Wljson)


@api.route("/createWorkspace", methods=["POST"])
@login_required
async def createWorkspace():
    jsonS = request.get_json()
    if not jsonS or not jsonS["name"] or not jsonS["params"]:
        return Response("Invalid data", status=400)
    W = db.Workspace.create(current_user, jsonS["name"], json.dumps(jsonS["params"])).data
    R = db.Roles.getRole("Administrator").data
    WU = db.WorkspaceProfile.create(current_user, W).data
    WU.setRole(R)
    return Response("ok", status=200)


@api.route("/activateInviteCode", methods=["POST"])
@login_required
async def activateInviteCode():
    jsonS = request.get_json()
    if not jsonS or not jsonS["keyCode"]:
        return Response("Invalid data", status=400)
    KD = db.KeyData.getByKey(jsonS["keyCode"]).data
    if not KD:
        return Response(status=404)
    status = KD.Workspace.joinWorkspace(current_user, jsonS["keyCode"]).status
    if not status:
        return Response(status=404)
    return Response("ok", status=200)

@api.route("/getInviteCodeInfo/<code>")
async def getInviteCodeInfo(code):
    KD = db.KeyData.getByKey(code).data
    if not KD:
        return Response(status=404)
    return jsonify(KD.getJson())


@api.route('/changeWorkspaceUserRole', methods=['PUT'])
@login_required
@utils.WorkspaceUser
@utils.PermsRequredOR("moderate_workspace")
async def changeWorkspaceUserRole(WU: db.WorkspaceProfile) -> Response:
    jsonS = request.get_json()
    module_logger.info(f"{current_user.Username} trying manage workspace user role")
    if "userID" not in jsonS or isinstance(jsonS["userID"], int):
        return Response("Invalid data", status=400)
    if "roleID" not in jsonS or jsonS["roleID"] or isinstance(jsonS["roleID"], int):
        return Response("Invalid data", status=400)
    WP = db.WorkspaceProfile.getInstance(jsonS["userID"])
    R = db.Roles.getInstance(jsonS["roleID"])
    if not R or not WP:
        return Response("Invalid data", status=400)
    if WP.Workspace.ID != WU.Workspace.ID:
        return Response("Not enough permissions", status=403)
    if WP.Role.ID > WU.Role.ID:
        return Response("Not enough permissions", status=403)





@api.route('/kickWorkspaceUser', methods=['POST'])
@login_required
@utils.WorkspaceUser
@utils.PermsRequredOR("moderate_workspace")
async def kickWorkspaceUser(WU: db.WorkspaceProfile) -> Response:
    jsonS = request.get_json()
    module_logger.info(f"{current_user.Username} trying kick user from workspace {WU.Workspace.Name}")
    if "userID" not in jsonS or not jsonS["userID"]:
        return Response("Invalid data", status=400)
    WP = db.WorkspaceProfile.getInstance(jsonS["userID"])
    if WP is None:
        return Response("User Not Found", status=400)
    if WP.Workspace.ID != WU.Workspace.ID:
        return Response("Not enough permissions", status=403)
    if WP.Role.ID > WU.Role.ID:
        return Response("Not enough permissions", status=403)
    WP.Active = False
    WP.save()
    return Response("ok", status=200)



@api.route('/leaveFromWorkspace', methods=['POST'])
@login_required
@utils.WorkspaceUser
async def leaveFromWorkspace(WU: db.WorkspaceProfile) -> Response:
    module_logger.info(f"{current_user.Username} trying leave from workspace {WU.Workspace.Name}")
    WU.Active = False
    WU.save()
    res = Response("ok", status=200)
    res.set_cookie("workspace", "", max_age=0)
    return res
