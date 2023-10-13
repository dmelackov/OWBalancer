from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from app.DataBase.db import Profile, WorkspaceProfile
from app.Site.loginManager import manager
from app.Site.utils import getWorkspaceProfile

router = APIRouter(
    prefix="/profile",
    tags=["profile"]
)


@router.get("/getCurrentUserInfo/")
async def getInfo(user: Profile | None = Depends(manager.optional), workspaceProfile: WorkspaceProfile | None = Depends(getWorkspaceProfile)):
    if user is None:
        return {"auth": False}
    if workspaceProfile is None:
        return {"auth": True, "profile": {"username": user.Username}}
    return {"auth": True,
            "profile": {
                "username": user.Username,
                "workspace": workspaceProfile.Workspace.getJson(),
                "role": workspaceProfile.Role.Name
            }}


@router.get("/getPermissions/")
async def getPermissions(workspaceProfile: WorkspaceProfile | None = Depends(getWorkspaceProfile)):
    if workspaceProfile is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Invalid workspace/user")
    return list(map(lambda x: x.Name, workspaceProfile.getPermissions().data))
