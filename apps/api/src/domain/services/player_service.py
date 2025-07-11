from sqlalchemy.ext.asyncio import AsyncSession

from balancer_models.models import Player, Workspace, WorkspaceProfile
from balancer_models.permissions import Permissions
from balancer_models.repository import PlayerRepository
from domain.exceptions import (CantEditPlayerException,
                               CantEditPlayerRolesException,
                               PlayerAlreadyExistException,
                               PlayerCreateException, PlayerNotFoundException)

from .workspace_profile_service import WorkspaceProfileService


class PlayerService:
    def __init__(self, workspace_profile_service: WorkspaceProfileService, player_repository: PlayerRepository) -> None:
        self.workspace_profile_service = workspace_profile_service
        self.player_repository = player_repository

    async def is_same_workspace(self, workspace_profile: WorkspaceProfile, player: Player):
        return workspace_profile.workspace_id == player.creator.workspace_id

    async def check_same_workspace(self, workspace_profile: WorkspaceProfile, player: Player):
        if not await self.is_same_workspace(workspace_profile, player):
            raise PlayerNotFoundException

    async def can_edit_player(self, workspace_profile: WorkspaceProfile, player: Player) -> bool:
        if not await self.is_same_workspace(workspace_profile, player):
            return False
        can_other = await self.workspace_profile_service.has_permission(workspace_profile, Permissions.change_player)
        can_self = await self.workspace_profile_service.has_permission(workspace_profile, Permissions.change_your_player) and player.creator_id == workspace_profile.id
        return can_other or can_self

    async def check_edit_player(self, workspace_profile: WorkspaceProfile, player: Player):
        if not self.can_edit_player(workspace_profile, player):
            raise CantEditPlayerException

    async def can_edit_roles(self, workspace_profile: WorkspaceProfile, player: Player) -> bool:
        if not await self.is_same_workspace(workspace_profile, player):
            return False
        return await self.workspace_profile_service.has_permission(workspace_profile, Permissions.change_player_roles)

    async def check_edit_roles(self, workspace_profile: WorkspaceProfile, player: Player):
        if not self.can_edit_roles(workspace_profile, player):
            raise CantEditPlayerRolesException

    async def get_by_id(self, id: int) -> Player:
        player = await self.player_repository.get_by_id(id)
        if player is None:
            raise PlayerNotFoundException
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
            raise PlayerAlreadyExistException
        player = await self.player_repository.create(creator, name)
        if player is None:
            raise PlayerCreateException
        return player

    async def delete(self, initiator: WorkspaceProfile, player: Player):
        await self.check_edit_player(initiator, player)
        await self.player_repository.delete(player)

    async def get_players(self, workspace: Workspace, filter="") -> list[Player]:
        players = await self.player_repository.get_by_workspace(workspace, filter=f"%{filter}%")
        return players
