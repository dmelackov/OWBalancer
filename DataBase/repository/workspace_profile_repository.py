
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from DataBase.models import Profile, Role, Workspace, WorkspaceProfile, Lobby


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

    async def create(self, profile: Profile, workspace: Workspace, lobby: Lobby, role: Role) -> Optional[WorkspaceProfile]:
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
