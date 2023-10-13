from fastapi import APIRouter, Depends, HTTPException, Response
from starlette.status import HTTP_404_NOT_FOUND
from pydantic import BaseModel

from app.DataBase.db import Profile, WorkspaceProfile, Workspace
from app.Site.loginManager import manager


class RoleAmount(BaseModel):
    T: int
    D: int
    H: int


class TeamNames(BaseModel):
    t1: str
    t2: str


class Math(BaseModel):
    alpha: int | float
    beta: int | float
    gamma: int | float
    p: int | float
    q: int | float
    tWeight: int | float
    dWeight: int | float
    hWeight: int | float


class Settings(BaseModel):
    AutoCustom: bool
    Autoincrement: bool
    BalanceLimit: int
    ExtendedLobby: bool
    ExpandedResult: bool
    Amount: RoleAmount
    TeamNames: TeamNames
    fColor: str
    sColor: str
    Math: Math


router = APIRouter(
    prefix="/settings",
    tags=["settings"]
)


@router.get("/getSettings/")
async def getSettings(user: Profile = Depends(manager)) -> Settings:
    settings = user.getUserSettings()
    settings["TeamNames"]['t1'] = settings["TeamNames"]["1"]
    settings["TeamNames"]['t2'] = settings["TeamNames"]["2"]
    del settings["TeamNames"]["1"]
    del settings["TeamNames"]["2"]
    return settings


@router.post("/setSettings/")
async def setSettings(settings: Settings, user: Profile = Depends(manager)):
    settingsCopy = settings.model_dump()
    settingsCopy["TeamNames"]['1'] = settingsCopy["TeamNames"]["t1"]
    settingsCopy["TeamNames"]['2'] = settingsCopy["TeamNames"]["t2"]
    del settingsCopy["TeamNames"]["t1"]
    del settingsCopy["TeamNames"]["t2"]
    user.setUserSettings(settingsCopy)
    return {"message": "OK"}
