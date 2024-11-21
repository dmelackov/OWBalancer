from fastapi import Depends, Response, responses
from fastapi_controllers import Controller, get, post
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from DataBase.database import get_db_session
from DataBase.models import Profile
from DataBase.permissions import Permissions
from DataBase.roles import Roles
from DataBase.schemes import (InviteInfo, RoleScheme, WorkspaceProfileScheme,
                              WorkspaceScheme)
from Site.exception_mapping import generate_responses_for_endpoint
from Site.utils import get_ok_response
from domain.exceptions.workspace_exceptions import WorkspaceNotFoundException
from domain.exceptions.workspace_profile_exceptions import CantEditOtherWorkspaceProfileException, CantManipulateRoleException, DontHavePermissionException, NotParticipiantException, WorkspaceProfileNotFoundException
from domain.services import WorkspaceProfileService, WorkspaceService
from Site.loginManager import manager


class CreateWorkspaceParams(BaseModel):
    CustomSystem: bool


class CreateWorkspaceRequest(BaseModel):
    name: str
    params: CreateWorkspaceParams


class ChangeWorkspaceUserRoleRequest(BaseModel):
    workspace_profile_id: int
    role_id: int


class InviteCreateRequest(BaseModel):
    use_limit: int = Field(ge=1, le=10)


class InviteCreated(BaseModel):
    key: str


class KickRequest(BaseModel):
    workspace_profile_id: int


class WorkspaceController(Controller):
    prefix = "/workspace"
    tags = ["workspace"]

    def __init__(self,
                 session: AsyncSession = Depends(get_db_session),
                 profile: Profile = Depends(manager)) -> None:
        self.session = session
        self.profile = profile

        self.workspace_service = WorkspaceService(session)
        self.workspace_profile_service = WorkspaceProfileService(session)

    @get("/roles",
         response_model=list[RoleScheme],
         summary="Get available roles")
    async def get_roles(self):
        """
        Retrieves a list of roles available in the system.

        Returns:
            A list of RoleScheme objects representing the available roles.
        """
        return await self.workspace_service.get_roles()

    @post("/{workspace_id}/select",
          summary="Select workspace",
          responses={
              **get_ok_response("Workspace successfully selected"),
              **generate_responses_for_endpoint([
                  NotParticipiantException,
                  WorkspaceNotFoundException
              ])
          })
    async def select_workspace(self,
                               response: Response,
                               workspace_id: int):
        """
        Select a workspace to interact with.

        Selects a workspace to interact with. If the workspace doesn't exist, or the user is not a participant of the workspace, an error is returned.

        Args:
            workspace_id (int): The ID of the workspace to select.

        Returns:
            A dictionary containing a message indicating that the workspace has been successfully selected.
        """
        workspace = await self.workspace_service.get_by_id(workspace_id)
        await self.workspace_profile_service.check_participant(self.profile, workspace)

        response.set_cookie("workspace", str(workspace.id),
                            max_age=60*60*24*30)  # 1 month
        return {"message": "OK"}

    @get("/",
         response_model=list[WorkspaceScheme],
         summary="Get workspaces")
    async def get_workspaces(self):
        """
        Returns a list of workspaces that the user is a participant of.

        Returns:
            A list of WorkspaceScheme objects representing the user's workspaces.
        """
        return await self.workspace_service.get_by_profile(self.profile)

    @get("/{workspace_id}",
         response_model=WorkspaceScheme,
         summary="Get workspace by id",
         responses={
             **generate_responses_for_endpoint([
                 WorkspaceNotFoundException,
                 NotParticipiantException
             ])
         })
    async def get_workspace(self,
                            workspace_id: int):
        """
        Retrieves a workspace by its ID.

        Args:
            workspace_id (int): The ID of the workspace to retrieve.

        Returns:
            A WorkspaceScheme object representing the retrieved workspace.

        Raises:
            WorkspaceNotFoundException: If the workspace doesn't exist.
            NotParticipiantException: If the user is not a participant of the workspace.
        """
        workspace = await self.workspace_service.get_by_id(workspace_id)
        await self.workspace_profile_service.check_participant(self.profile, workspace)

        return workspace

    @post("/",
          response_model=WorkspaceScheme,
          summary="Create a new workspace")
    async def create_workspace(self,
                               request: CreateWorkspaceRequest):
        """
        Creates a new workspace with the given name and parameters.

        Args:
            request: A CreateWorkspaceRequest object containing the name and parameters of the workspace to create.

        Returns:
            A WorkspaceScheme object representing the newly created workspace.
        """
        workspace = await self.workspace_service.create(self.profile, request.name, request.params.model_dump())
        role = await self.workspace_service.get_role(Roles.ADMINISTRATOR)

        await self.workspace_profile_service.join(self.profile, workspace, role)

        await self.session.commit()
        return workspace

    @post("/{workspace_id}/change_role",
          summary="Change workspace user role",
          responses={
              **get_ok_response("Role successfully changed"),
              **generate_responses_for_endpoint([
                  WorkspaceNotFoundException,
                  WorkspaceProfileNotFoundException,
                  CantManipulateRoleException,
                  CantEditOtherWorkspaceProfileException
              ])
          })
    async def changeWorkspaceUserRole(self,
                                      request: ChangeWorkspaceUserRoleRequest,
                                      workspace_id: int,):
        """
        Changes the role of a user within a workspace.

        This endpoint allows the authenticated user to change the role of another
        user in a specified workspace. The user must have the necessary permissions
        to modify roles.

        Args:
            request: A ChangeWorkspaceUserRoleRequest object containing the target
                    workspace_profile_id and the new role_id.
            workspace_id (int): The ID of the workspace where the role change will occur.

        Returns:
            A dictionary containing a message indicating that the role has been
            successfully changed.

        Raises:
            NotParticipiantException: If the user is not a participant of the workspace.
            WorkspaceProfileNotFoundException: If the target workspace profile is not found.
            CantManipulateRoleException: If the user doesn't have permission to change the role.
            CantEditOtherWorkspaceProfileException: If the user can't edit the target workspace profile.
        """
        workspace = await self.workspace_service.get_by_id(workspace_id)
        workspace_profile = await self.workspace_profile_service.get_by_bind(self.profile, workspace)
        role = await self.workspace_service.get_role_by_id(request.role_id)

        target_workspace_profile = await self.workspace_profile_service.get_by_id(request.workspace_profile_id)
        await self.workspace_profile_service.change_role(workspace_profile, target_workspace_profile, role)
        await self.session.commit()
        return {"message": "OK"}

    @post("/{workspace_id}/kick",
          summary="Kick user from workspace",
          responses={
              **get_ok_response("User successfully kicked"),
              **generate_responses_for_endpoint([
                  WorkspaceNotFoundException,
                  WorkspaceProfileNotFoundException,
                  CantEditOtherWorkspaceProfileException
              ])
          })
    async def kick(self,
                   request: KickRequest,
                   workspace_id: int):
        """
        This endpoint allows the authenticated user to kick a user from a specified
        workspace. The user must have the necessary permissions to kick users.

        Args:
            request: A KickRequest object containing the target workspace_profile_id.
            workspace_id (int): The ID of the workspace where the kicking will occur.

        Returns:
            A dictionary containing a message indicating that the user has been
            successfully kicked.

        Raises:
            WorkspaceProfileNotFoundException: If the target workspace profile is not found.
            CantEditOtherWorkspaceProfileException: If the user can't kick the target workspace profile.
        """
        workspace = await self.workspace_service.get_by_id(workspace_id)
        workspace_profile = await self.workspace_profile_service.get_by_bind(self.profile, workspace)

        target_workspace_profile = await self.workspace_profile_service.get_by_id(request.workspace_profile_id)
        await self.workspace_profile_service.kick(workspace_profile, target_workspace_profile)

        await self.session.commit()
        return {"message": "OK"}

    @post("/{workspace_id}/leave",
          summary="Leave workspace",
          responses={
              **get_ok_response("Leave successful"),
              **generate_responses_for_endpoint([
                  WorkspaceNotFoundException,
                  WorkspaceProfileNotFoundException
              ])
          })
    async def workspace_leave(self,
                              res: Response,
                              workspace_id: int):
        """
        This endpoint allows the authenticated user to leave a workspace.

        Args:
            workspace_id (int): The ID of the workspace to leave.

        Returns:
            A dictionary containing a message indicating that the user has been
            successfully kicked.

        Raises:
            WorkspaceNotFoundException: If the workspace doesn't exist.
            WorkspaceProfileNotFoundException: If the authenticated user's workspace profile is not found.
        """
        workspace = await self.workspace_service.get_by_id(workspace_id)
        workspace_profile = await self.workspace_profile_service.get_by_bind(self.profile, workspace)

        await self.workspace_profile_service.leave(workspace_profile)

        await self.session.commit()
        res.set_cookie("access-token", "", max_age=0, httponly=True)
        return {"message": "OK"}

    @get("/{workspace_id}/members",
         response_model=list[WorkspaceProfileScheme],
         summary="Get workspace members",
         responses={
             **generate_responses_for_endpoint([
                 WorkspaceNotFoundException,
                 NotParticipiantException
             ])
         })
    async def get_workspace_members(self,
                                    workspace_id: int):
        """
        This endpoint returns a list of the members of the specified workspace.

        Args:
            workspace_id (int): The ID of the workspace.

        Returns:
            A list of WorkspaceProfileScheme objects representing the members of the workspace.

        Raises:
            WorkspaceNotFoundException: If the workspace doesn't exist.
            NotParticipiantException: If the user is not a participant of the workspace.
        """
        workspace = await self.workspace_service.get_by_id(workspace_id)
        await self.workspace_profile_service.check_participant(self.profile, workspace)

        return await self.workspace_service.get_members(workspace)

    @get("/{workspace_id}/invite",
         response_model=list[InviteInfo],
         summary="Get workspace invites",
         responses={
             **generate_responses_for_endpoint([
                 WorkspaceNotFoundException,
                 WorkspaceProfileNotFoundException,
                 DontHavePermissionException
             ])
         })
    async def get_workspace_invites(self,
                                    workspace_id: int):
        """
        This endpoint returns a list of the invites of the specified workspace.

        Args:
            workspace_id (int): The ID of the workspace.

        Returns:
            A list of InviteInfo objects representing the invites of the workspace.

        Raises:
            WorkspaceNotFoundException: If the workspace doesn't exist.
            WorkspaceProfileNotFoundException: If the authenticated user's workspace profile is not found.
            DontHavePermissionException: If the user doesn't have permission to get the invites.
        """
        workspace = await self.workspace_service.get_by_id(workspace_id)
        workspace_profile = await self.workspace_profile_service.get_by_bind(self.profile, workspace)
        await self.workspace_profile_service.check_permission(workspace_profile, Permissions.moderate_workspace)

        return await self.workspace_service.get_invites(workspace)

    @post("/{workspace_id}/invite",
          response_model=InviteCreated,
          summary="Create workspace invite",
          responses={
              **generate_responses_for_endpoint([
                  WorkspaceNotFoundException,
                  WorkspaceProfileNotFoundException,
                  DontHavePermissionException
              ])
          })
    async def create_workspace_invite(self,
                                      workspace_id: int,
                                      request: InviteCreateRequest):
        """
        This endpoint creates a new invite for the specified workspace.

        Args:
            workspace_id (int): The ID of the workspace.
            request (InviteCreateRequest): A request object containing the use_limit for the invite.

        Returns:
            An InviteCreated object containing the created invite key.

        Raises:
            WorkspaceNotFoundException: If the workspace doesn't exist.
            WorkspaceProfileNotFoundException: If the authenticated user's workspace profile is not found.
            DontHavePermissionException: If the user doesn't have permission to create the invite.
        """
        workspace = await self.workspace_service.get_by_id(workspace_id)
        workspace_profile = await self.workspace_profile_service.get_by_bind(self.profile, workspace)
        await self.workspace_profile_service.check_permission(workspace_profile, Permissions.moderate_workspace)

        invite = await self.workspace_service.create_invite(workspace_profile, request.use_limit)
        await self.session.commit()
        return InviteCreated(key=invite.key)
