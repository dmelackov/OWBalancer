from fastapi import Cookie, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.DataBase.db import Profile, Workspace, WorkspaceProfile
#from app.DataBase.db2 import async_session
from app.Site.loginManager import manager



def getWorkspace(response: Response, workspace: str | None = Cookie(default=None)) -> Workspace | None:
    if workspace is None:
        return None
    if not workspace.isdigit():
        response.set_cookie("workspace",  "", max_age=0)
        return None
    workspace = int(workspace)
    workspace = Workspace.getInstance(workspace)
    if workspace is None:
        response.set_cookie("workspace",  "", max_age=0)
    return workspace


def getWorkspaceProfile(response: Response, user: Profile | None = Depends(manager.optional), workspace: Workspace | None = Depends(getWorkspace)) -> WorkspaceProfile | None:
    if user is None:
        return None
    if workspace is None:
        return None
    workspaceProfile = WorkspaceProfile.getWU(user, workspace).data
    if not workspaceProfile.Active:
        workspaceProfile = None
    if workspaceProfile is None:
        response.set_cookie("workspace",  "", max_age=0)
    return workspaceProfile
