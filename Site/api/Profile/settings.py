from fastapi import Depends
from fastapi_controllers import Controller, get, post
from sqlalchemy.ext.asyncio import AsyncSession

from DataBase.database import get_db_session
from DataBase.models import Profile
from DataBase.schemes import Settings
from domain.services import ProfileService
from Site.loginManager import manager
from Site.utils import get_ok_response

class SettingsController(Controller):
    prefix = "/settings"
    tags = ["settings"]

    def __init__(self,
                 session: AsyncSession = Depends(get_db_session),
                 profile: Profile = Depends(manager)) -> None:
        self.session = session
        self.profile = profile
        self.profile_service = ProfileService(session)

    @get("/default",
         response_model=Settings,
         summary="Get default settings")
    async def get_default(self):
        """
        Get default settings

        Default settings are the same for all profiles.
        They are used as a starting point for a new profile.
        """
        return self.profile_service.get_default_settings()

    @get("/",
         response_model=Settings,
         summary="Get profile settings")
    async def get_settings(self):
        """
        Get profile settings

        Return the settings of the current profile.
        """
        return self.profile_service.get_settings(self.profile)

    @post("/",
          summary="Set profile settings",
          responses={
              **get_ok_response("Settings updated"),
          })
    async def set_settings(self,
                           settings: Settings):
        """
        Set profile settings

        Replace the current settings of the profile with the given ones.
        """
        await self.profile_service.set_settings(self.profile, settings)
        await self.session.commit()
        return {"message": "OK"}
