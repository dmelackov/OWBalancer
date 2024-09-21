from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
from starlette.status import (HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN,
                              HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR)

from DataBase.database import get_db_session
from DataBase.models.profile import Profile
from DataBase.permissions import Permissions
from DataBase.repository.invite_repository import InviteRepository
from DataBase.repository.role_repository import RoleRepository
from DataBase.repository.workspace_profile_repository import WorkspaceProfileRepository
from DataBase.repository.workspace_repository import WorkspaceRepository
from DataBase.schemes.invite import TruncInviteInfo
from DataBase.schemes.role_scheme import RoleScheme
from DataBase.schemes.workspace_profile import WorkspaceProfileScheme
from DataBase.schemes.workspace_scheme import WorkspaceScheme
from Site.loginManager import manager
from Site.service.invite_service import InviteService
from Site.service.workspace_profile_service import WorkspaceProfileService
from Site.service.workspace_service import WorkspaceService
from Site.utils import get_workspace_profile
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_controllers import Controller, post, get, delete


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
