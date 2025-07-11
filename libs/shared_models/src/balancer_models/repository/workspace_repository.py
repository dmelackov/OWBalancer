from typing import Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models import (KeyData, Lobby, Profile, Workspace,
                             WorkspaceProfile)


class WorkspaceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: int) -> Optional[Workspace]:
        stmt = select(Workspace).where(Workspace.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_user(self, profile: Profile) -> list[Workspace]:
        stmt = select(WorkspaceProfile).options(selectinload(WorkspaceProfile.workspace)).where(
            and_(
                WorkspaceProfile.profile_id == profile.id,
                WorkspaceProfile.active == True
            )
        )
        workspaces = []
        for workspace_profile in (await self.session.scalars(stmt)).all():
            workspace_profile.workspace.creator
            workspaces.append(workspace_profile.workspace)
        return workspaces

    async def create(self, creator: Profile, name: str, lobby: Lobby, workspace_params: Optional[dict] = None) -> Optional[Workspace]:
        if workspace_params is None:
            workspace = Workspace(
                lobby_id=lobby.id, creator_id=creator.id, name=name, description="")
        else:
            workspace = Workspace(lobby_id=lobby.id, creator_id=creator.id,
                                  name=name, description="", workspace_params=workspace_params)
        self.session.add(workspace)
        await self.session.flush()
        return await self.get_by_id(workspace.id)

    async def set_description(self, workspace: Workspace, description: str):
        workspace.description = description
        await self.session.flush()

    async def get_members(self, workspace: Workspace) -> list[WorkspaceProfile]:
        stmt = select(WorkspaceProfile).where(
            WorkspaceProfile.workspace_id == workspace.id, WorkspaceProfile.active == True)
        return list((await self.session.scalars(stmt)).all())

    async def get_invites(self, workspace: Workspace) -> list[KeyData]:
        stmt = select(KeyData).join(WorkspaceProfile).where(
            WorkspaceProfile.workspace_id == workspace.id, KeyData.use_limit > 0)
        return list((await self.session.scalars(stmt)).all())
