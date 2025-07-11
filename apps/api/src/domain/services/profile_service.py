from sqlalchemy.ext.asyncio import AsyncSession

from balancer_models.models import DEFAULT_PROFILE_DATA, Profile
from balancer_models.repository import ProfileRepository
from ..schemes import Settings
from domain.exceptions import (InvalidCredentialsException,
                               PasswordDontMatchException,
                               ProfileAlreadyExists)


class ProfileService:
    def __init__(self, profile_repository: ProfileRepository) -> None:
        self.profile_repository = profile_repository

    async def login(self, login: str, password: str) -> Profile:
        profile = await self.profile_repository.get_by_auth(login, password)
        if profile is None:
            raise InvalidCredentialsException
        return profile

    async def registration(self, login, password, repeat_password):
        if password != repeat_password:
            raise PasswordDontMatchException
        if await self.profile_repository.get_by_username(login) is not None:
            raise ProfileAlreadyExists
        await self.profile_repository.registration(login, password)

    async def get_default_settings(self) -> Settings:
        return Settings.model_validate(DEFAULT_PROFILE_DATA)

    async def get_settings(self, profile: Profile) -> Settings:
        return Settings.model_validate(profile.settings)

    async def set_settings(self, profile: Profile, settings: Settings):
        await self.profile_repository.set_settings(profile, settings.model_dump())
