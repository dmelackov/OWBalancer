from sqlalchemy.ext.asyncio import AsyncSession

from balancer_models.models import KeyData, Profile, WorkspaceProfile
from balancer_models.permissions import Permissions
from balancer_models.repository import InviteRepository
from balancer_models.roles import Roles
from domain.exceptions import InviteExpiredException, InviteNotFoundException

from .workspace_profile_service import WorkspaceProfileService
from .workspace_service import WorkspaceService


class InviteService:
    def __init__(self, workspace_service: WorkspaceService, workspace_profile_service: WorkspaceProfileService,
                 invite_repository: InviteRepository) -> None:
        self.workspace_service = workspace_service
        self.workspace_profile_service = workspace_profile_service
        self.invite_repository = invite_repository

    async def activate_invite(self, invite: KeyData, profile: Profile):
        if invite.use_limit <= 0:
            raise InviteExpiredException
        await self.workspace_profile_service.check_not_participant(profile, invite.creator.workspace)
        role = await self.workspace_service.get_role(Roles.GUEST)
        await self.workspace_profile_service.join(profile, invite.creator.workspace, role)
        await self.invite_repository.decrease_uselimit(invite)

    async def get_by_key(self, token: str):
        invite = await self.invite_repository.get_by_key(token)
        if invite is None:
            raise InviteNotFoundException
        if invite.use_limit <= 0:
            raise InviteExpiredException
        return invite

    async def get_by_id(self, id: int):
        invite = await self.invite_repository.get_by_id(id)
        if invite is None or invite.use_limit <= 0:
            raise InviteNotFoundException
        return invite

    async def deactivate_invite(self, initiator: WorkspaceProfile, invite: KeyData):
        await self.workspace_profile_service.check_permission(initiator, Permissions.moderate_workspace)
        await self.invite_repository.deactivate(invite)
