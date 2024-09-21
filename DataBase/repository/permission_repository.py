from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from DataBase.models.perm import Perm

class PermissionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: int) -> Optional[Perm]:
        stmt = select(Perm).where(Perm.id == id).limit(1)
        return await self.session.scalar(stmt)
    
    async def get_by_name(self, name: str) -> Optional[Perm]:
        stmt = select(Perm).where(Perm.name == name).limit(1)
        return await self.session.scalar(stmt)
    
    async def create(self, name: str):
        perm = Perm(name=name)
        self.session.add(perm)
        await self.session.flush()
        return await self.get_by_id(perm.id)