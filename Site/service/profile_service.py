from fastapi import HTTPException
from DataBase.models.profile import DEFAULT_PROFILE_DATA, Profile
from DataBase.repository.profile_repository import ProfileRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_login.exceptions import InvalidCredentialsException
from starlette.status import HTTP_400_BAD_REQUEST

from DataBase.schemes.settings import Settings

class ProfileService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

        self.profile_repository = ProfileRepository(session)

    async def login(self, login: str, password: str) -> Profile:
        profile = await self.profile_repository.get_by_auth(login, password)
        if profile is None:
            raise InvalidCredentialsException
        return profile
    
    async def registration(self, login, password, repeat_password):
        if password != repeat_password:
            raise HTTPException(HTTP_400_BAD_REQUEST, "Passwords don't match")
        if await self.profile_repository.get_by_username(login) is not None:
            raise HTTPException(HTTP_400_BAD_REQUEST, "User already exist")
        await self.profile_repository.registration(login, password)

    async def get_default_settings(self) -> Settings:
        return Settings.model_validate(DEFAULT_PROFILE_DATA)
    
    async def get_settings(self, profile: Profile) -> Settings:
        return Settings.model_validate(profile.settings)
    
    async def set_settings(self, profile: Profile, settings: Settings):
        await self.profile_repository.set_settings(profile, settings.model_dump())