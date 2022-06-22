from flask import request
from flask_login import current_user
import app.DataBase.db as db


def getWorkspaceByRequest():
    if "workspace" not in request.cookies:
        return None
    try:
        workspaceID = int(request.cookies)
    except ValueError:
        return None
    return db.Workspace.getInstance(workspaceID)
    

def getWorkspaceProfileByRequest():
    W = getWorkspaceByRequest()
    if not W:
        return None
   
    