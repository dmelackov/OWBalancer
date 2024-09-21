from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from DataBase.models.lobby import Lobby


class LobbyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: int) -> Optional[Lobby]:
        stmt = select(Lobby).where(Lobby.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def create(self) -> Lobby:
        lobby = Lobby()
        self.session.add(lobby)
        await self.session.flush()
        new_lobby = await self.get_by_id(lobby.id)
        if new_lobby is None:
            raise
        return new_lobby
