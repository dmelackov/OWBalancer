import json

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from pydantic_core import to_json
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from app.Calculation.TTT import recalculateWorkspace
from fastapi.templating import Jinja2Templates

import app.DataBase.dataModels as dataModels
from app.Calculation.GameBalance import createGame
from app.Calculation.StaticAnalisys import recountModel
from app.DataBase.db import Custom, Games, Profile, WorkspaceProfile
from app.DataBase.permissions import Permissions
from app.Site.loginManager import manager
from app.Site.utils import getWorkspaceProfile

router = APIRouter(
    prefix="/game",
    tags=["game"]
)

templates = Jinja2Templates(directory="templates")

class Static(BaseModel):
    CustomID: int
    TSR: int
    DSR: int
    HSR: int
    Flex: bool
    Roles: str
    Username: str

class Active(BaseModel):
    TeamMask: str
    fMask: str
    sMask: str
    dpFairness: float
    vqUniformity: float
    teamRolePriority: float
    result: float

class GameResult(BaseModel):
    FirstTeamPoints: int
    SecondTeamPoints: int
    active: Active
    static: list[Static]

@router.post("/sendResult")
async def sendResult(game: GameResult, workspaceProfile: WorkspaceProfile | None = Depends(getWorkspaceProfile)):
    if workspaceProfile is None:
        raise HTTPException(HTTP_401_UNAUTHORIZED,
                            "Not found workspace profile")
    fMaskIndex = 0
    sMaskIndex = 0


    if game.SecondTeamPoints != game.FirstTeamPoints:
        if game.FirstTeamPoints > game.SecondTeamPoints:
            diff = 50
        else:
            diff = -50

        for i in range(len(game.active.TeamMask)):
            C = Custom.getInstance(game.static[i].CustomID)
            if C is None:
                print("В пизду")
                return
            if game.active.TeamMask[i] == "0":
                role = int(game.active.fMask[fMaskIndex])
                if C.Creator == workspaceProfile and workspaceProfile.Profile.getUserSettings()["Autoincrement"]:
                    sr = [C.TSR, C.DSR, C.HSR][role]
                    C.changeSR(role, sr + diff)
                fMaskIndex += 1
            else:
                role = int(game.active.sMask[sMaskIndex])
                if C.Creator == workspaceProfile and workspaceProfile.Profile.getUserSettings()["Autoincrement"]:
                    sr = [C.TSR, C.DSR, C.HSR][role]
                    C.changeSR(role, sr - diff)
                sMaskIndex += 1

    jsonModel = json.loads(to_json(game))
    G = Games.create(workspaceProfile, json.dumps(jsonModel["active"]), json.dumps(jsonModel["static"]))
    G.finishGame(game.FirstTeamPoints, game.SecondTeamPoints)
    G.save()
    recalculateWorkspace(workspaceProfile.Workspace.ID)
    return {"message": "OK"}

def getRankIco(sr):
    if sr < 1500:
        return "/img/sr_icons/bronse.png"
    if sr < 2000:
        return "/img/sr_icons/silver.png"
    if sr < 2500:
        return "/img/sr_icons/gold.png"
    if sr < 3000:
        return "/img/sr_icons/plat.png"
    if sr < 3500:
        return "/img/sr_icons/diamond.png"
    if sr < 4000:
        return "/img/sr_icons/masters.png"
    return "/img/sr_icons/gm.png"
    
def getRoleIco(role):
    iconImages = {
        "T": "/img/role_icons/tank.svg",
        "D": "/img/role_icons/dps.svg",
        "H": "/img/role_icons/support.svg",
        "0": "/img/role_icons/tank.svg",
        "1": "/img/role_icons/dps.svg",
        "2": "/img/role_icons/support.svg",
    }
    return iconImages[role]

def getSR(player, role):
    if role == "0":
        return player["TSR"]
    if role == "1":
        return player["DSR"]
    if role == "2":
        return player["HSR"]


@router.get("/{id}/image.svg")
def balance_image(request: Request, id: int):
    game = Games.getInstance(id)
    if game is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Game not found")
    
    gameActive = json.loads(game.GameData)
    gameStatic = json.loads(game.GameStatic)
    
    fMaskIndex = 0
    sMaskIndex = 0
    
    team1 = []
    team2 = []
    
    for i in range(len(gameActive["TeamMask"])):
        if gameActive["TeamMask"][i] == "0":
            role = gameActive["fMask"][fMaskIndex]
            plr = gameStatic[fMaskIndex + sMaskIndex]
            team1.append({"Username": plr["Username"],
                          "RankIco": getRankIco(getSR(plr, role)),
                          "MainRoleIco": getRoleIco(plr["Roles"][0]),
                          "SecondsRoleIcons": [getRoleIco(i) for i in plr["Roles"][1:]],
                          "RoleIco": getRoleIco(role),
                          "sr": getSR(plr, role),
                          "role": role})
            
            fMaskIndex += 1
        else:
            role = gameActive["sMask"][sMaskIndex]
            plr = gameStatic[fMaskIndex + sMaskIndex]
            team2.append({"Username": plr["Username"],
                          "RankIco": getRankIco(getSR(plr, role)),
                          "MainRoleIco": getRoleIco(plr["Roles"][0]),
                          "SecondsRoleIcons": [getRoleIco(i) for i in plr["Roles"][1:]],
                          "RoleIco": getRoleIco(role),
                          "sr": getSR(plr, role),
                          "role": role})
            sMaskIndex += 1
    
    team1 = list(sorted(team1, key=lambda x: int(x["role"])))
    team2 = list(sorted(team2, key=lambda x: int(x["role"])))
    
    response =  templates.TemplateResponse(
        request=request, name="balance.html", context={"gameActive": gameActive, "gameStatic": gameStatic, "team1": team1, "team2": team2}
    )
    response.headers["Content-Type"] = "image/svg+xml"
    return response