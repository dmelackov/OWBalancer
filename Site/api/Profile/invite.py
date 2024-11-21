from fastapi import Depends
from fastapi_controllers import Controller, delete, get, post
from sqlalchemy.ext.asyncio import AsyncSession

from DataBase.database import get_db_session
from DataBase.models import Profile
from DataBase.schemes import TruncInviteInfo
from Site.exception_mapping import generate_responses_for_endpoint
from Site.utils import get_ok_response
from domain.exceptions.invite_exceptions import InviteExpiredException, InviteNotFoundException
from domain.exceptions.workspace_profile_exceptions import AlreadyParticipiantException, DontHavePermissionException, WorkspaceProfileNotFoundException
from domain.services import (InviteService, WorkspaceProfileService,
                             WorkspaceService)
from Site.loginManager import manager


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

    @get("/{token}",
         response_model=TruncInviteInfo,
         summary="Get invite data")
    async def get_invite_data(self, token: str):
        """
        Get invite data.

        Args:
            token: Invite token.

        Returns:
            Invite data.

        Raises:
            InviteNotFoundException: If invite with given token doesn't exist.
            InviteExpiredException: If invite with given token has expired.
        """
        return await self.invite_service.get_by_key(token)

    @post("/{token}",
          summary="Activate invite",
          responses={
              **get_ok_response("Invite sucessfully activated"),
              **generate_responses_for_endpoint(
                    allowed_exceptions=[
                        InviteNotFoundException,
                        InviteExpiredException,
                        AlreadyParticipiantException
                    ]
                )
          })
    async def activate_invite(self, token: str):
        """
        Activate invite.

        Args:
            token: Invite token.

        Raises:
            InviteNotFoundException: If invite with given token doesn't exist.
            InviteExpiredException: If invite is expired.
            AlreadyParticipiantException: If user is already in workspace.
        """
        invite = await self.invite_service.get_by_key(token)
        await self.invite_service.activate_invite(invite, self.profile)
        await self.session.commit()
        return {"message": "ok"}

    @delete("/{id}",
            summary="Deactivate invite",
            responses={
                **get_ok_response("Invite sucessfully deactivated"),
                **generate_responses_for_endpoint(
                    allowed_exceptions=[
                        InviteNotFoundException,
                        WorkspaceProfileNotFoundException,
                        DontHavePermissionException
                    ]
                )
            })
    async def deactivate_invite(self, id: int):
        """
        Deactivate invite.

        Args:
            id: Invite id.

        Raises:
            InviteNotFoundException: If invite with given id doesn't exist.
            WorkspaceProfileNotFoundException: If user is not in workspace.
            DontHavePermissionException: If user doesn't have permission to deactivate invite.
        """
        invite = await self.invite_service.get_by_id(id)
        workspace_profile = await self.workspace_profile_service.get_by_bind(self.profile, invite.creator.workspace)
        await self.invite_service.deactivate_invite(workspace_profile, invite)
        await self.session.commit()
        return {"message": "ok"}
