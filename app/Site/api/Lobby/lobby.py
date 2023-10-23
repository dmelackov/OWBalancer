from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN

from app.DataBase.db import Custom, WorkspaceProfile
from app.Site.loginManager import manager
from app.Site.utils import getWorkspaceProfile
from app.DataBase.permissions import Permissions

import app.DataBase.dataModels as dataModels

router = APIRouter(
    prefix="/lobby",
    tags=["lobby"]
)



@router.get("/getLobby")
async def getLobby(workspaceProfile: WorkspaceProfile | None = Depends(getWorkspaceProfile)) -> list[dataModels.Custom]:
    if workspaceProfile is None:
        raise HTTPException(HTTP_401_UNAUTHORIZED,
                            "Not found workspace profile")
    players = workspaceProfile.getLobbyInfo()
    return [Custom.getInstance(i).getJson(workspaceProfile) for i in players]

@router.post("/addToLobby/{customID}")
async def addToLobby(customID: int, workspaceProfile: WorkspaceProfile | None = Depends(getWorkspaceProfile)):
    if workspaceProfile is None:
        raise HTTPException(HTTP_401_UNAUTHORIZED,
                            "Not found workspace profile")
    if not workspaceProfile.checkPermission(Permissions.add_customs_toLobby):
        raise HTTPException(HTTP_403_FORBIDDEN, "Not enough permissions")
    custom = Custom.getInstance(customID)
    if custom is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Not found")
    if custom.Creator.Workspace != workspaceProfile.Workspace:
        raise HTTPException(HTTP_404_NOT_FOUND, "Not found")
    answer = workspaceProfile.addToLobby(custom)
    if answer.status:
        return {"message": "OK"}
    else:
        return {"message": answer.error}

@router.delete("/deleteFromLobby/{customID}")
async def deleteFromLobby(customID: int, workspaceProfile: WorkspaceProfile | None = Depends(getWorkspaceProfile)):
    if workspaceProfile is None:
        raise HTTPException(HTTP_401_UNAUTHORIZED,
                            "Not found workspace profile")
    if not workspaceProfile.checkPermission(Permissions.add_customs_toLobby):
        raise HTTPException(HTTP_403_FORBIDDEN, "Not enough permissions")
    custom = Custom.getInstance(customID)
    if custom is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Not found")
    if custom.Creator.Workspace != workspaceProfile.Workspace:
        raise HTTPException(HTTP_404_NOT_FOUND, "Not found")
    answer = workspaceProfile.DeleteFromLobby(custom)
    if answer.status:
        return {"message": "OK"}
    else:
        return {"message": answer.error}
    
@router.delete("/clearLobby")
async def getInfo(workspaceProfile: WorkspaceProfile | None = Depends(getWorkspaceProfile)) -> list[dataModels.Custom]:
    if workspaceProfile is None:
        raise HTTPException(HTTP_401_UNAUTHORIZED,
                            "Not found workspace profile")
    if not workspaceProfile.checkPermission(Permissions.add_customs_toLobby):
        raise HTTPException(HTTP_403_FORBIDDEN, "Not enough permissions")
    workspaceProfile.ClearLobby()
    return {"message": "OK"}