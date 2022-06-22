from flask import Blueprint, Response, request
from flask import jsonify
import logging
from flask_login import current_user, login_required
import app.DataBase.db as db
import json 

module_logger = logging.getLogger("api")

api = Blueprint('workspace_api', __name__, template_folder='templates',
                static_folder='static')


@api.route("/setWorkspace", methods=["POST"])
@login_required
def setWorkspace():
    data = request.get_json()
    if not data or not data["ID"]:
        return Response(status=400)
    W = db.Workspace.getInstance(data["ID"])
    if not W:
        return Response(status=404)
    res = Response(status=200)
    res.set_cookie("workspace", str(W.ID), max_age=60*60*24*365)
    return res


@api.route("/getWorkspace/<ID:int>")
@login_required
def getWorkspace(ID):
    W = db.Workspace.getInstance(ID)
    return W.getJson()    


@api.route("/getWorkspaces")
@login_required
def getWorkspaces():
    Wl = current_user.getWorkspaceList()
    Wljson = [i.getJson() for i in Wl]
    return jsonify(Wljson)


@api.route("/createWorkspace", methods=["POST"])
@login_required
def createWorkspace():
    jsonS = request.get_json()
    if not jsonS or not jsonS["name"] or not jsonS["params"]:
        return Response(status=400)
    W = db.Workspace.create(current_user, jsonS["name"], json.dumps(jsonS["params"])).data
    R = db.Roles.getRole("Administrator").data
    WU = db.WorkspaceProfile.create(current_user, W).data
    WU.setRole(R)
    return Response(status=200)


@api.route("/activeInviteCode", methods=["POST"])
@login_required
def activeInviteCode():
    jsonS = request.get_json()
    if not jsonS or not jsonS["keyCode"]:
        return Response(status=400)
    W = db.Workspace.getByKey(jsonS["keyCode"]).data
    if not W:
        return Response(status=404)
    status = W.joinWorkspace(current_user, jsonS["keyCode"]).status
    if not status:
        return Response(status=404)
    return Response(status=200)

@api.route("/getInviteCodeInfo/<code>")
def getInviteCodeInfo(code):
    KD = db.KeyData.getByKey(code).data
    if not KD:
        return Response(status=404)
    return jsonify(KD.getJson())



