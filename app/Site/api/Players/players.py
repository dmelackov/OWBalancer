from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_500_INTERNAL_SERVER_ERROR
from typing import Annotated
from pydantic import BaseModel

from app.DataBase.db import Profile, WorkspaceProfile, Player, PlayerRoles
from app.Site.loginManager import manager
from app.Site.utils import getWorkspaceProfile
from app.DataBase.methods import Permissions

import app.DataBase.dataModels as dataModels


router = APIRouter(
    prefix="/players",
    tags=["players"]
)


@router.get("/getPlayers/{searchStr}")
async def getPlayers(searchStr: str, workspaceProfile: WorkspaceProfile | None = Depends(getWorkspaceProfile)) -> list[dataModels.Player]:
    if workspaceProfile is None:
        raise HTTPException(HTTP_401_UNAUTHORIZED,
                            "Not found workspace profile")
    players = workspaceProfile.Workspace.searchPlayers(searchStr)
    return [i.getJson() for i in players]


@router.get("/getPlayers/")
async def getPlayers(workspaceProfile: WorkspaceProfile | None = Depends(getWorkspaceProfile)) -> list[dataModels.Player]:
    if workspaceProfile is None:
        raise HTTPException(HTTP_401_UNAUTHORIZED,
                            "Not found workspace profile")
    players = workspaceProfile.Workspace.searchPlayers("")
    return [i.getJson() for i in players]


class SetRolesRequest(BaseModel):
    roles: Annotated[str, Query(pattern="^[TDH]?[TDH]?[TDH]?$")]


@router.put("/setRoles/{playerID}")
async def setRoles(playerID: int, roles: SetRolesRequest, workspaceProfile: WorkspaceProfile | None = Depends(getWorkspaceProfile)):
    if workspaceProfile is None:
        raise HTTPException(HTTP_401_UNAUTHORIZED,
                            "Not found workspace profile")
    player = Player.getInstance(playerID)
    if player is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Not found")
    if player.Creator.Workspace != workspaceProfile.Workspace:
        raise HTTPException(HTTP_404_NOT_FOUND, "Not found")
    if workspaceProfile.checkPermission(Permissions.change_player_roles):
        raise HTTPException(HTTP_403_FORBIDDEN, "Not enough permissions")
    pr = PlayerRoles.getPR(workspaceProfile, player)
    if pr.data is None:
        raise HTTPException(HTTP_403_FORBIDDEN, pr.error)
    pr.data.setRoles(roles.roles)
    return {"message": "OK"}


class SetFlexRequest(BaseModel):
    status: bool


@router.put("/setFlex/{playerID}")
async def setFlex(playerID: int, flex: SetFlexRequest, workspaceProfile: WorkspaceProfile | None = Depends(getWorkspaceProfile)):
    if workspaceProfile is None:
        raise HTTPException(HTTP_401_UNAUTHORIZED,
                            "Not found workspace profile")
    player = Player.getInstance(playerID)
    if player is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Not found")
    if player.Creator.Workspace != workspaceProfile.Workspace:
        raise HTTPException(HTTP_404_NOT_FOUND, "Not found")
    if not workspaceProfile.checkPermission(Permissions.change_player_roles):
        raise HTTPException(HTTP_403_FORBIDDEN, "Not enough permissions")
    pr = PlayerRoles.getPR(workspaceProfile, player)
    if pr.data is None:
        raise HTTPException(HTTP_403_FORBIDDEN, pr.error)
    pr.data.setFlex(flex.status)
    return {"message": "OK"}


class CreatePlayerRequest(BaseModel):
    Username: str


@router.post("/createPlayer/")
async def createPlayer(player: CreatePlayerRequest, workspaceProfile: WorkspaceProfile | None = Depends(getWorkspaceProfile)):
    if workspaceProfile is None:
        raise HTTPException(HTTP_401_UNAUTHORIZED,
                            "Not found workspace profile")
    P = Player.create(workspaceProfile, player.Username)
    if P is None:
        raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, "Internal error")
    return {"message": "OK"}


@router.delete("/deletePlayer/{playerID}")
async def deletePlayer(playerID: int, workspaceProfile: WorkspaceProfile | None = Depends(getWorkspaceProfile)):
    if workspaceProfile is None:
        raise HTTPException(HTTP_401_UNAUTHORIZED,
                            "Not found workspace profile")
    player = Player.getInstance(playerID)
    if player is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Not found")
    if player.Creator.Workspace != workspaceProfile.Workspace:
        raise HTTPException(HTTP_404_NOT_FOUND, "Not found")
    if player.Creator == workspaceProfile:
        if not workspaceProfile.checkPermission(Permissions.delete_your_player) and not workspaceProfile.checkPermission(Permissions.delete_player):
            raise HTTPException(HTTP_403_FORBIDDEN, "Not enough permissions")
    else:
        if not workspaceProfile.checkPermission(Permissions.delete_player):
            raise HTTPException(HTTP_403_FORBIDDEN, "Not enough permissions")
    player.delete_instance(recursive=True)
    return {"message": "OK"}


class ChangePlayerNicknameRequest(BaseModel):
    Username: str


@router.put("/changeNickname/{playerID}")
async def deletePlayer(playerID: int, req: ChangePlayerNicknameRequest, workspaceProfile: WorkspaceProfile | None = Depends(getWorkspaceProfile)):
    if workspaceProfile is None:
        raise HTTPException(HTTP_401_UNAUTHORIZED,
                            "Not found workspace profile")
    player = Player.getInstance(playerID)
    if player is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Not found")
    if player.Creator.Workspace != workspaceProfile.Workspace:
        raise HTTPException(HTTP_404_NOT_FOUND, "Not found")
    if player.Creator == workspaceProfile:
        if not workspaceProfile.checkPermission(Permissions.change_your_player) and not workspaceProfile.checkPermission(Permissions.change_player):
            raise HTTPException(HTTP_403_FORBIDDEN, "Not enough permissions")
    else:
        if not workspaceProfile.checkPermission(Permissions.change_player):
            raise HTTPException(HTTP_403_FORBIDDEN, "Not enough permissions")
    player.Username = req.Username
    player.save()
    return {"message": "OK"}
