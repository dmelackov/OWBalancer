from fastapi import Depends
from fastapi_controllers import Controller, get, post
from sqlalchemy.ext.asyncio import AsyncSession

from DataBase.database import get_db_session
from DataBase.models import Profile
from DataBase.schemes import Settings
from Site.loginManager import manager
from domain.services import ProfileService


class SettingsController(Controller):
    prefix = "/settings"
    tags = ["settings"]

    def __init__(self,
                 session: AsyncSession = Depends(get_db_session),
                 profile: Profile = Depends(manager)) -> None:
        self.session = session
        self.profile = profile
        self.profile_service = ProfileService(session)

    @get("/default", response_model=Settings)
    async def get_default(self):
        return self.profile_service.get_default_settings()

    @get("/", response_model=Settings)
    async def get_settings(self):
        return self.profile_service.get_settings(self.profile)

    @post("/")
    async def set_settings(self, settings: Settings):
        await self.profile_service.set_settings(self.profile, settings)
        await self.session.commit()
        return {"message": "OK"}
