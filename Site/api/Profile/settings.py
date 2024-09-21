from fastapi import APIRouter, Depends
from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession
from DataBase.database import get_db_session
from DataBase.models.profile import DEFAULT_PROFILE_DATA, Profile
from DataBase.repository.profile_repository import ProfileRepository
from Site.loginManager import manager

from fastapi_controllers import Controller, get, post


class RoleAmount(BaseModel):
    tank: int
    damage: int
    support: int


class Team(BaseModel):
    name: str
    color: str


class Teams(BaseModel):
    first: Team
    second: Team


class Math(BaseModel):
    balance_limit: int
    alpha: int | float
    beta: int | float
    gamma: int | float
    p: int | float
    q: int | float
    tank_weight: int | float
    damage_weight: int | float
    support_weight: int | float


class Settings(BaseModel):
    auto_custom: bool
    auto_increment: bool
    extended_lobby: bool
    expanded_result: bool
    amount: RoleAmount
    team: Teams
    math: Math

class SettingsController(Controller):
    prefix = "/settings"
    tags = ["settings"]

    def __init__(self,
                 session: AsyncSession = Depends(get_db_session),
                 profile: Profile = Depends(manager)) -> None:
        self.session = session
        self.profile = profile
        self.profile_repository = ProfileRepository(session)

    @get("/default", response_model=Settings)
    async def get_default(self):
        return DEFAULT_PROFILE_DATA

    @get("/", response_model=Settings)
    async def get_settings(self):
        return self.profile.settings

    @post("/")
    async def set_settings(self, settings: Settings):
        settingsCopy = settings.model_dump()
        await self.profile_repository.set_settings(self.profile, settingsCopy)
        await self.session.commit()
        return {"message": "OK"}
