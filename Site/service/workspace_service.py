from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from starlette.status import (HTTP_403_FORBIDDEN,
                              HTTP_404_NOT_FOUND,
                              HTTP_500_INTERNAL_SERVER_ERROR,
                              HTTP_400_BAD_REQUEST)

from DataBase.models.key_data import KeyData
from DataBase.repository.invite_repository import InviteRepository
from DataBase.repository.workspace_profile_repository import WorkspaceProfileRepository
from DataBase.repository.workspace_repository import WorkspaceRepository
from DataBase.repository.role_repository import RoleRepository

from DataBase.models.workspace_profile import WorkspaceProfile
from DataBase.models.workspace import Workspace
from DataBase.models.profile import Profile
from DataBase.models.role import Role
from DataBase.roles import Roles


class WorkspaceService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

        self.role_repository = RoleRepository(session)
        self.workspace_repository = WorkspaceRepository(session)
        self.workspace_profile_repository = WorkspaceProfileRepository(session)
        self.invite_repository = InviteRepository(session)

    async def get_by_id(self, id: int) -> Workspace:
        workspace = await self.workspace_repository.get_by_id(id)
        if workspace is None:
            raise HTTPException(HTTP_404_NOT_FOUND, "Workspace not found")
        return workspace

    async def create(self, creator: Profile, name: str, params: dict):
        workspace = await self.workspace_repository.create(creator, name, params)
        if workspace is None:
            raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR,
                                "Unable to create workspace")
        return workspace

    async def get_by_profile(self, profile: Profile) -> list[Workspace]:
        return await self.workspace_repository.get_by_user(profile)

    async def get_roles(self) -> list[Role]:
        return await self.role_repository.get_all()

    async def get_role(self, role_enum: Roles) -> Role:
        role = await self.role_repository.get_by_name(role_enum.value)
        if role is None:
            raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR,
                                "Roles not generated. Contact site admin")
        return role

    async def get_role_by_id(self, id: int) -> Role:
        role = await self.role_repository.get_by_id(id)
        if role is None:
            raise HTTPException(HTTP_404_NOT_FOUND, "Role not found")
        return role

    async def get_members(self, workspace: Workspace) -> list[WorkspaceProfile]:
        return await self.workspace_repository.get_members(workspace)

    async def get_invites(self, workspace: Workspace) -> list[KeyData]:
        return await self.workspace_repository.get_invites(workspace)

    async def create_invite(self, initiator: WorkspaceProfile, use_limit: int) -> KeyData:
        keydata = await self.invite_repository.create(initiator, use_limit=use_limit)
        if keydata is None:
            raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR,
                                "Unable to create invite")
        return keydata
