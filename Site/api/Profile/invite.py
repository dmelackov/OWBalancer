from fastapi import Depends
from fastapi_controllers import Controller, delete, get, post
from sqlalchemy.ext.asyncio import AsyncSession

from DataBase.database import get_db_session
from DataBase.models.profile import Profile
from DataBase.schemes.invite import TruncInviteInfo
from Site.loginManager import manager
from Site.service.invite_service import InviteService
from Site.service.workspace_profile_service import WorkspaceProfileService
from Site.service.workspace_service import WorkspaceService


class InviteController(Controller):
    prefix = "/invite"
    tags = ["invite"]

    def __init__(self,
                 session: AsyncSession = Depends(get_db_session),
                 profile: Profile = Depends(manager)) -> None:
        self.session = session
        self.profile = profile

        self.workspace_service = WorkspaceService(session)
        self.workspace_profile_service = WorkspaceProfileService(session)
        self.invite_service = InviteService(session)

    @get("/{token}", response_model=TruncInviteInfo)
    async def get_invite_data(self, token: str):
        return await self.invite_service.get_by_key(token)

    @post("/{token}")
    async def activate_invite(self, token: str):
        invite = await self.invite_service.get_by_key(token)
        await self.invite_service.activate_invite(invite, self.profile)
        await self.session.commit()
        return {"message": "ok"}

    @delete("/{id}")
    async def deactivate_invite(self, id: int):
        invite = await self.invite_service.get_by_id(id)
        workspace_profile = await self.workspace_profile_service.get_by_bind(self.profile, invite.creator.workspace)
        await self.invite_service.deactivate_invite(workspace_profile, invite)
        await self.session.commit()
        return {"message": "ok"}
