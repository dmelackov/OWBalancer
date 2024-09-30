from sqlalchemy.ext.asyncio import AsyncSession

from DataBase.models import Profile, Role, Workspace, WorkspaceProfile
from DataBase.repository import RoleRepository, WorkspaceProfileRepository, LobbyRepository, WorkspaceRepository

from DataBase.permissions import Permissions

from domain.exceptions import AlreadyParticipiantException, NotParticipiantException, CantEditOtherWorkspaceProfileException, CantManipulateRoleException, DontHavePermissionException, WorkspaceProfileCreateException, WorkspaceProfileNotFoundException

class WorkspaceProfileService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

        self.role_repository = RoleRepository(session)
        self.workspace_repository = WorkspaceRepository(session)
        self.workspace_profile_repository = WorkspaceProfileRepository(session)
        self.lobby_repostiory = LobbyRepository(session)

    async def has_permission(self, workspace_profile: WorkspaceProfile, permission: Permissions) -> bool:
        if workspace_profile.id == workspace_profile.workspace.creator.id:
            return True
        return await self.role_repository.check_permission(workspace_profile.role, Permissions.moderate_workspace.value)

    async def check_permission(self, workspace_profile: WorkspaceProfile, permission: Permissions):
        if not await self.has_permission(workspace_profile, permission):
            raise DontHavePermissionException(permission.value)

    async def can_manipulate_role(self, workspace_profile: WorkspaceProfile, role: Role) -> bool:
        if workspace_profile.id == workspace_profile.workspace.creator.id:
            return True
        return workspace_profile.role.id > role.id

    async def check_manipulate_role(self, workspace_profile: WorkspaceProfile, role: Role):
        if not await self.can_manipulate_role(workspace_profile, role):
            raise CantManipulateRoleException

    async def is_participant(self, profile: Profile, workspace: Workspace) -> bool:
        workspace_profile = await self.workspace_profile_repository.get_by_bind(profile, workspace)
        return workspace_profile is not None and workspace_profile.active

    async def check_participant(self, profile: Profile, workspace: Workspace):
        if not await self.is_participant(profile, workspace):
            raise NotParticipiantException

    async def check_not_participant(self, profile: Profile, workspace: Workspace):
        if await self.is_participant(profile, workspace):
            raise AlreadyParticipiantException

    async def can_edit_other(self, initiator: WorkspaceProfile, target: WorkspaceProfile) -> bool:
        if target.workspace_id != initiator.workspace_id:
            return False
        if not await self.has_permission(initiator, Permissions.moderate_workspace):
            return False
        if not await self.can_manipulate_role(initiator, target.role):
            return False
        return True

    async def check_edit_other(self, initiator: WorkspaceProfile, target: WorkspaceProfile):
        if not self.can_edit_other(initiator, target):
            raise CantEditOtherWorkspaceProfileException

    async def get_by_id(self, id: int) -> WorkspaceProfile:
        workspace_profile = await self.workspace_profile_repository.get_by_id(id)
        if workspace_profile is None:
            raise WorkspaceProfileNotFoundException
        return workspace_profile

    async def get_by_bind(self, profile: Profile, workspace: Workspace) -> WorkspaceProfile:
        workspace_profile = await self.workspace_profile_repository.get_by_bind(profile, workspace)
        if workspace_profile is None:
            raise WorkspaceProfileNotFoundException
        return workspace_profile

    async def change_role(self, initiator: WorkspaceProfile, target: WorkspaceProfile, role: Role):
        await self.check_edit_other(initiator, target)
        await self.check_manipulate_role(initiator, role)
        await self.workspace_profile_repository.set_role(target, role)

    async def kick(self, initiator: WorkspaceProfile, target: WorkspaceProfile):
        await self.check_edit_other(initiator, target)
        await self.workspace_profile_repository.deactivate(target)

    async def leave(self, workspace_profile: WorkspaceProfile):
        await self.workspace_profile_repository.deactivate(workspace_profile)

    async def join(self, profile: Profile, workspace: Workspace, role: Role):
        old_workspace_profile = await self.workspace_profile_repository.get_by_bind(profile, workspace)
        if old_workspace_profile is not None:
            await self.workspace_profile_repository.activate(old_workspace_profile)
            return old_workspace_profile
        lobby = await self.lobby_repostiory.create()
        workspace_profile = await self.workspace_profile_repository.create(profile, workspace, lobby, role)
        if workspace_profile is None:
            raise WorkspaceProfileCreateException
        return workspace_profile

    async def get_permissions(self, workspace_profile: WorkspaceProfile) -> list[str]:
        perms = await self.role_repository.get_permissions(workspace_profile.role)
        return list(map(lambda x: x.name, perms))