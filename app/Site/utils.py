from quart import request
from quart_login import current_user
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
    