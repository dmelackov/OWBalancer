from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from pydantic import BaseModel

from app.DataBase.db import Profile, WorkspaceProfile
from app.Site.loginManager import manager
from app.Site.utils import getWorkspaceProfile
from app.DataBase.permissions import Permissions

from app.Calculation.StaticAnalisys import recountModel
from app.Calculation.GameBalance import createGame

import app.DataBase.dataModels as dataModels
router = APIRouter(
    prefix="/balance",
    tags=["balance"]
)


class CalcBalanceRequest(BaseModel):
    static: list
    active: dict

@router.post("/calcBalance/")
async def calcBalance(req: CalcBalanceRequest, workspaceProfile: WorkspaceProfile | None = Depends(getWorkspaceProfile)):
    if workspaceProfile is None:
        raise HTTPException(HTTP_401_UNAUTHORIZED,
                            "Not found workspace profile")
    if not workspaceProfile.checkPermission(Permissions.do_balance):
        raise HTTPException(HTTP_403_FORBIDDEN, "Not enough permissions")
    return recountModel(req.static, req.active, workspaceProfile.Profile)

@router.get("/getBalances/")
async def getBalances(workspaceProfile: WorkspaceProfile | None = Depends(getWorkspaceProfile)):
    if workspaceProfile is None:
        raise HTTPException(HTTP_401_UNAUTHORIZED,
                            "Not found workspace profile")
    if not workspaceProfile.checkPermission(Permissions.do_balance):
        raise HTTPException(HTTP_403_FORBIDDEN, "Not enough permissions")
    return createGame(workspaceProfile)