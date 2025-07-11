from sqlalchemy.ext.asyncio import AsyncSession

from balancer_models.models import KeyData, Profile, Role, Workspace, WorkspaceProfile
from balancer_models.repository import (InviteRepository, LobbyRepository,
                                 RoleRepository, WorkspaceProfileRepository,
                                 WorkspaceRepository)
from balancer_models.roles import Roles
from domain.exceptions import (InviteCreateException, RoleNotFoundException,
                               RoleNotGeneratedException,
                               WorkspaceCreateException,
                               WorkspaceNotFoundException)


class WorkspaceService:
    def __init__(self, role_repository: RoleRepository, workspace_repository: WorkspaceRepository, workspace_profile_repository: WorkspaceProfileRepository, invite_repository: InviteRepository, lobby_repository: LobbyRepository) -> None:
        self.role_repository = role_repository
        self.workspace_repository = workspace_repository
        self.workspace_profile_repository = workspace_profile_repository
        self.invite_repository = invite_repository
        self.lobby_repository = lobby_repository

    async def get_by_id(self, id: int) -> Workspace:
        workspace = await self.workspace_repository.get_by_id(id)
        if workspace is None:
            raise WorkspaceNotFoundException
        return workspace

    async def create(self, creator: Profile, name: str, params: dict):
        lobby = await self.lobby_repository.create()
        workspace = await self.workspace_repository.create(creator, name, lobby, params)
        if workspace is None:
            raise WorkspaceCreateException
        return workspace

    async def get_by_profile(self, profile: Profile) -> list[Workspace]:
        return await self.workspace_repository.get_by_user(profile)

    async def get_roles(self) -> list[Role]:
        return await self.role_repository.get_all()

    async def get_role(self, role_enum: Roles) -> Role:
        role = await self.role_repository.get_by_name(role_enum.value)
        if role is None:
            raise RoleNotGeneratedException
        return role

    async def get_role_by_id(self, id: int) -> Role:
        role = await self.role_repository.get_by_id(id)
        if role is None:
            raise RoleNotFoundException
        return role

    async def get_members(self, workspace: Workspace) -> list[WorkspaceProfile]:
        return await self.workspace_repository.get_members(workspace)

    async def get_invites(self, workspace: Workspace) -> list[KeyData]:
        return await self.workspace_repository.get_invites(workspace)

    async def create_invite(self, initiator: WorkspaceProfile, use_limit: int) -> KeyData:
        keydata = await self.invite_repository.create(initiator, use_limit=use_limit)
        if keydata is None:
            raise InviteCreateException
        return keydata
