from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from DataBase.models.player import Player
from DataBase.models.player_roles import PlayerRoles
from DataBase.models.workspace import Workspace
from DataBase.models.workspace_profile import WorkspaceProfile


class PlayerRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: int) -> Optional[Player]:
        stmt = select(Player).where(Player.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_username(self, username: str, workspace: Workspace) -> Optional[Player]:
        stmt = select(Player).join(WorkspaceProfile).where(
            Player.username == username, WorkspaceProfile.workspace_id == workspace.id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_workspace(self, workspace: Workspace, filter: Optional[str] = None) -> list[Player]:
        stmt = select(Player).join(Player.creator).where(
            WorkspaceProfile.workspace_id == workspace.id)
        if filter is not None:
            stmt = stmt.filter(Player.username.ilike(filter))
        return list((await self.session.scalars(stmt)).all())

    async def create(self, creator: WorkspaceProfile, username: str) -> Optional[Player]:
        player = Player(creator_id=creator.id, username=username)
        self.session.add(player)
        await self.session.flush()
        new_player = await self.get_by_id(player.id)
        return new_player

    async def update_username(self, player: Player, username: str):
        player.username = username
        await self.session.flush()

    async def get_or_create_roles(self, player: Player, workspace_profile: WorkspaceProfile) -> PlayerRoles:
        get_stmt = select(PlayerRoles).where(PlayerRoles.creator_id ==
                                             workspace_profile.id, PlayerRoles.player_id == player.id).limit(1)
        player_roles = await self.session.scalar(get_stmt)
        if player_roles is not None:
            return player_roles
        new_player_roles = PlayerRoles(
            creator_id=workspace_profile.id, player_id=player.id)
        self.session.add(new_player_roles)
        await self.session.flush()
        getted_player_roles = await self.session.scalar(get_stmt)
        if getted_player_roles is None:
            raise
        return getted_player_roles

    async def update_roles(self, player: Player, workspace_profile: WorkspaceProfile, roles: str):
        player_roles = await self.get_or_create_roles(player, workspace_profile)
        player_roles.roles = roles
        await self.session.flush()

    async def update_flex(self, player: Player, workspace_profile: WorkspaceProfile, flex: bool):
        player_roles = await self.get_or_create_roles(player, workspace_profile)
        player_roles.is_flex = flex
        await self.session.flush()

    async def delete(self, player: Player):
        await self.session.delete(player)
        await self.session.flush()
