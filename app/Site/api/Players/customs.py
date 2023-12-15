from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from starlette.status import (HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN,
                              HTTP_404_NOT_FOUND)

import app.DataBase.dataModels as dataModels
from app.DataBase.db import Custom, Player, WorkspaceProfile
from app.DataBase.permissions import Permissions
from app.Site.loginManager import manager
from app.Site.utils import getWorkspaceProfile

router = APIRouter(
    prefix="/customs",
    tags=["customs"]
)


@router.get("/getCustoms/{playerID}")
async def getCustoms(playerID: int, workspaceProfile: WorkspaceProfile | None = Depends(getWorkspaceProfile)) -> list[dataModels.Custom]:
    if workspaceProfile is None:
        raise HTTPException(HTTP_401_UNAUTHORIZED,
                            "Not found workspace profile")
    player = Player.getInstance(playerID)
    if player is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Not found")
    if player.Creator.Workspace != workspaceProfile.Workspace:
        raise HTTPException(HTTP_404_NOT_FOUND, "Not found")
    customs = Custom.get_byPlayer(player.ID).data
    return list(map(lambda x: x.getJson(workspaceProfile), customs))


class ChangeRoleSrRequest(BaseModel):
    role: dataModels.GameRole
    sr: Annotated[int, Query(gt=-1, lt=5001)]


@router.put("/changeRoleSr/{customID}")
async def changeRoleSr(customID: int, data: ChangeRoleSrRequest, workspaceProfile: WorkspaceProfile | None = Depends(getWorkspaceProfile)):
    if workspaceProfile is None:
        raise HTTPException(HTTP_401_UNAUTHORIZED,
                            "Not found workspace profile")
    custom = Custom.getInstance(customID)
    if custom is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Not found")
    if custom.Creator.Workspace != workspaceProfile.Workspace:
        raise HTTPException(HTTP_404_NOT_FOUND, "Not found")
    if custom.Creator == workspaceProfile:
        if not workspaceProfile.checkPermission(Permissions.change_your_custom):
            raise HTTPException(HTTP_403_FORBIDDEN, "Not enough permissions")
    else:
        raise HTTPException(HTTP_403_FORBIDDEN, "Not enough permissions")
    custom.changeSR(data.role.value, data.sr)
    return {"message": "OK"}


class CreateCustomRequest(BaseModel):
    id: int


@router.post("/createCustom")
async def createCustom(data: CreateCustomRequest, workspaceProfile: WorkspaceProfile | None = Depends(getWorkspaceProfile)) -> dataModels.Custom:
    if workspaceProfile is None:
        raise HTTPException(HTTP_401_UNAUTHORIZED,
                            "Not found workspace profile")
    player = Player.getInstance(data.id)
    if player is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Not found")
    if player.Creator.Workspace != workspaceProfile.Workspace:
        raise HTTPException(HTTP_404_NOT_FOUND, "Not found")
    if not workspaceProfile.checkPermission(Permissions.create_custom):
        raise HTTPException(HTTP_403_FORBIDDEN, "Not enough permissions")
    custom = Custom.create(workspaceProfile, player)
    if custom.data is None:
        return {"error": custom.error}
    return custom.data.getJson(workspaceProfile)

@router.delete("/deleteCustom/{customID}")
async def deleteCustom(customID: int, workspaceProfile: WorkspaceProfile | None = Depends(getWorkspaceProfile)):
    if workspaceProfile is None:
        raise HTTPException(HTTP_401_UNAUTHORIZED,
                            "Not found workspace profile")
    custom = Custom.getInstance(customID)
    if custom is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Not found")
    if custom.Creator.Workspace != workspaceProfile.Workspace:
        raise HTTPException(HTTP_404_NOT_FOUND, "Not found")
    if custom.Creator == workspaceProfile:
        if not workspaceProfile.checkPermission(Permissions.delete_your_custom) and not workspaceProfile.checkPermission(Permissions.delete_custom):
            raise HTTPException(HTTP_403_FORBIDDEN, "Not enough permissions")
    else:
        if not workspaceProfile.checkPermission(Permissions.delete_custom):
            raise HTTPException(HTTP_403_FORBIDDEN, "Not enough permissions")
    custom.delete_instance()
    return {"message": "OK"}
