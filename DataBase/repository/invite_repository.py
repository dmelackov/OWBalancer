import secrets
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from DataBase.models import KeyData, WorkspaceProfile


class InviteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: int) -> KeyData | None:
        stmt = select(KeyData).where(KeyData.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_key(self, key: str) -> KeyData | None:
        stmt = select(KeyData).where(KeyData.key == key).limit(1)
        return await self.session.scalar(stmt)

    async def create(self, workspace_profile: WorkspaceProfile, use_limit=-1) -> Optional[KeyData]:
        key = secrets.token_urlsafe(8)
        key_data = KeyData(creator_id=workspace_profile.id,
                           key=key, use_limit=use_limit)
        self.session.add(key_data)
        await self.session.flush()
        new_key_data = await self.get_by_id(key_data.id)
        return new_key_data

    async def decrease_uselimit(self, key_data: KeyData):
        key_data.use_limit -= 1
        await self.session.flush()

    async def deactivate(self, key_data: KeyData):
        key_data.use_limit = 0
        await self.session.flush()
