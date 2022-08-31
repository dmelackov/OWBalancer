from functools import wraps
from math import perm
from typing import List, Union
from quart import request, Response
from flask_login import current_user
import app.DataBase.db as db


def getWorkspaceIdByRequest() -> int:
    if "workspace" not in request.cookies:
        return None
    try:
        workspaceID = int(request.cookies["workspace"])
    except ValueError:
        return None
    return workspaceID

def getWorkspaceByRequest() -> db.Workspace:
    Wid = getWorkspaceIdByRequest()
    if not Wid:
        return None
    return db.Workspace.getInstance(Wid)
    

def getWorkspaceProfileByRequest() -> db.WorkspaceProfile:
    Wid = getWorkspaceIdByRequest()
    if not Wid:
        return None
    if "workspace" not in request.cookies:
        return None
    WU = db.WorkspaceProfile.getWU(current_user, Wid).data
    return WU


def WorkspaceUser(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        WU = getWorkspaceProfileByRequest()
        if not WU:
            return Response("Not Found Workspace Profile", status=403)
        return func(WU, *args, **kwargs)
    return _wrapper


def PermsRequredOR(perms: Union[List[str], str]):
    def _decorator(func):
        @wraps(func)
        def _wrapper(WU: db.WorkspaceProfile, *args, **kwargs):
            if isinstance(perms, str):
                NewPerms = [perms]
            else:
                NewPerms = perms
            for perm in NewPerms:
                if WU.checkPermission(perm).status:
                    return func(WU, *args, **kwargs)
            return Response("Not enough permissions", status=403)
        return _wrapper
    return _decorator

