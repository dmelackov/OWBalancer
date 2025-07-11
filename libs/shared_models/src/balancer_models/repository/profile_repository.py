import secrets
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import bcrypt
from ..models import Profile


class ProfileRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: int) -> Optional[Profile]:
        stmt = select(Profile).where(Profile.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_username(self, username: str) -> Optional[Profile]:
        stmt = select(Profile).where(Profile.username == username).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_auth(self, username: str, password: str) -> Optional[Profile]:
        profile = await self.get_by_username(username)
        if profile is None:
            return None
        if not self.compare_password(profile, password):
            return None
        return profile

    async def registration(self, username: str, password: str) -> Optional[Profile]:
        profile = Profile(username=username)
        self.session.add(profile)
        await self.set_password(profile, password)
        return await self.get_by_id(profile.id)

    async def set_password(self, profile: Profile, new_password: str) -> None:
        profile.password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        profile.secret = secrets.token_urlsafe(8)
        await self.session.flush()

    def compare_password(self, profile: Profile, password: str) -> bool:
        old_password = profile.password
        if old_password is None:
            old_password = ""
        return bcrypt.checkpw(password.encode(), old_password.encode())

    async def set_settings(self, profile: Profile, new_settings: dict) -> None:
        profile.settings = new_settings
        await self.session.flush()
