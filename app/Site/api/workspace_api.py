from flask import Blueprint, Response, request
from flask import jsonify
import logging
from flask_login import current_user
import app.DataBase.db as db
import app.Site.utils as utils
import json 

module_logger = logging.getLogger("api")

api = Blueprint('profile_api', __name__, template_folder='templates',
                static_folder='static')


@api.route("/setWorkspace", methods=["POST"])
def setWorkspace():
    if not current_user.is_authenticated:
        return Response(status=403)
    data = request.get_json()
    if not data or not data["ID"]:
        return Response(status=400)
    W = db.Workspace.getInstance(data["ID"])
    if not W:
        return Response(status=404)
    res = Response(status=200)
    res.set_cookie("workspace", str(W.ID))
    return res


@api.route("/getWorkspace")
def getWorkspace():
    if not current_user.is_authenticated:
        return Response(status=403)
    


@api.route("/getWorkspaces")
def getWorkspaces():
    if not current_user.is_authenticated:
        return Response(status=403)


@api.route("/createWorkspace", methods=["POST"])
def createWorkspace():
    if not current_user.is_authenticated:
        return Response(status=403)
    json = request.get_json()
    if not json or not json["name"] or not json["params"]:
        return Response(status=400)
    W = db.Workspace.create(current_user, json["name"], json.dumps(json["params"])).data
    res = Response(status=200)
    res.set_cookie("workspace", str(W.ID))
    return res


@api.route("/activeInviteCode", methods=["POST"])
def activeInviteCode():
    if not current_user.is_authenticated:
        return Response(status=403)
