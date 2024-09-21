
from typing import Optional

from sqlalchemy import and_, select
from DataBase.models.profile import Profile
from sqlalchemy.ext.asyncio import AsyncSession

from DataBase.models.role import Role
from DataBase.models.workspace import Workspace
from DataBase.models.workspace_profile import WorkspaceProfile
from DataBase.repository.lobby_repository import LobbyRepository


class WorkspaceProfileRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: int) -> Optional[WorkspaceProfile]:
        stmt = select(WorkspaceProfile).where(
            WorkspaceProfile.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_bind(self, profile: Profile, workspace: Workspace) -> Optional[WorkspaceProfile]:
        stmt = select(WorkspaceProfile).where(
            WorkspaceProfile.profile_id == profile.id,
            WorkspaceProfile.workspace_id == workspace.id
        ).limit(1)
        return await self.session.scalar(stmt)

    async def set_role(self, workspace_profile: WorkspaceProfile, role: Role):
        workspace_profile.role_id = role.id
        await self.session.flush()

    async def create(self, profile: Profile, workspace: Workspace, role: Role) -> Optional[WorkspaceProfile]:
        lobby_repository = LobbyRepository(self.session)

        lobby = await lobby_repository.create()
        workspace_profile = WorkspaceProfile(role_id=role.id,
                                             workspace_id=workspace.id,
                                             profile_id=profile.id,
                                             lobby_id=lobby.id,
                                             active=True)
        self.session.add(workspace_profile)
        await self.session.flush()
        return await self.get_by_id(workspace_profile.id)

    async def deactivate(self, workspace_profile: WorkspaceProfile):
        workspace_profile.active = False
        await self.session.flush()

    async def activate(self, workspace_profile: WorkspaceProfile):
        workspace_profile.active = True
        await self.session.flush()
