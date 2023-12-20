from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from pydantic_core import to_json
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
import json

import app.DataBase.dataModels as dataModels
from app.Calculation.GameBalance import createGame
from app.Calculation.StaticAnalisys import recountModel
from app.DataBase.db import Custom, Profile, WorkspaceProfile, Games
from app.DataBase.permissions import Permissions
from app.Site.loginManager import manager
from app.Site.utils import getWorkspaceProfile

router = APIRouter(
    prefix="/game",
    tags=["game"]
)


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
async def getCustoms(game: GameResult, workspaceProfile: WorkspaceProfile | None = Depends(getWorkspaceProfile)):
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
    return {"message": "OK"}
    