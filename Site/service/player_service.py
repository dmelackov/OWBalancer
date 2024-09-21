from re import A
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from DataBase.models.player import Player
from DataBase.models.workspace import Workspace
from DataBase.models.workspace_profile import WorkspaceProfile
from DataBase.permissions import Permissions
from DataBase.repository.player_repository import PlayerRepository
from Site.service.workspace_profile_service import WorkspaceProfileService


class PlayerService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

        self.workspace_profile_service = WorkspaceProfileService(session)
        self.player_repository = PlayerRepository(session)

    async def is_same_workspace(self, workspace_profile: WorkspaceProfile, player: Player):
        return workspace_profile.workspace_id == player.creator.workspace_id

    async def check_same_workspace(self, workspace_profile: WorkspaceProfile, player: Player):
        if not await self.is_same_workspace(workspace_profile, player):
            raise HTTPException(HTTP_404_NOT_FOUND, "Player not found")

    async def can_edit_player(self, workspace_profile: WorkspaceProfile, player: Player) -> bool:
        if not await self.is_same_workspace(workspace_profile, player):
            return False
        can_other = await self.workspace_profile_service.has_permission(workspace_profile, Permissions.change_player)
        can_self = await self.workspace_profile_service.has_permission(workspace_profile, Permissions.change_your_player) and player.creator_id == workspace_profile.id
        return can_other or can_self

    async def check_edit_player(self, workspace_profile: WorkspaceProfile, player: Player):
        if not self.can_edit_player(workspace_profile, player):
            raise HTTPException(HTTP_403_FORBIDDEN, "Not enough permissions")
        
    async def can_edit_roles(self, workspace_profile: WorkspaceProfile, player: Player) -> bool:
        if not await self.is_same_workspace(workspace_profile, player):
            return False
        return await self.workspace_profile_service.has_permission(workspace_profile, Permissions.change_player_roles)
    
    async def check_edit_roles(self, workspace_profile: WorkspaceProfile, player: Player):
        if not self.can_edit_roles(workspace_profile, player):
            raise HTTPException(HTTP_403_FORBIDDEN, "Not enough permissions")

    async def get_by_id(self, id: int) -> Player:
        player = await self.player_repository.get_by_id(id)
        if player is None:
            raise HTTPException(HTTP_404_NOT_FOUND, "Player not found")
        return player

    async def exist(self, workspace: Workspace, name: str):
        player = await self.player_repository.get_by_username(name, workspace)
        return player is not None

    async def set_roles(self, initiator: WorkspaceProfile, player: Player, roles: str):
        await self.check_edit_roles(initiator, player)
        await self.player_repository.update_roles(player, initiator, roles)

    async def set_flex(self, initiator: WorkspaceProfile, player: Player, is_flex: bool):
        await self.check_edit_roles(initiator, player)
        await self.player_repository.update_flex(player, initiator, is_flex)

    async def set_name(self, initiator: WorkspaceProfile, player: Player, name: str):
        await self.check_edit_player(initiator, player)
        await self.player_repository.update_username(player, name)

    async def create(self, creator: WorkspaceProfile, name: str) -> Player:
        await self.workspace_profile_service.check_permission(creator, Permissions.create_player)
        if self.exist(creator.workspace, name):
            raise HTTPException(HTTP_400_BAD_REQUEST, "Player already exists")
        player = await self.player_repository.create(creator, name)
        if player is None:
            raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, "Unable to create player")
        return player
    
    async def delete(self, initiator: WorkspaceProfile, player: Player):
        await self.check_edit_player(initiator, player)
        await self.player_repository.delete(player)

    async def get_players(self, workspace: Workspace, filter="") -> list[Player]:
        players = await self.player_repository.get_by_workspace(workspace, filter=f"%{filter}%")
        return players