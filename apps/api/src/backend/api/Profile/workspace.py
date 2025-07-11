from fastapi import APIRouter, Depends, Response, responses
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from backend.dependency import ProfileServiceDepends, WorkspaceProfileServiceDepends, WorkspaceServiceDepends
from balancer_models.models import Profile
from balancer_models.permissions import Permissions
from balancer_models.roles import Roles
from domain.schemes import (InviteInfo, RoleScheme, WorkspaceProfileScheme,
                              WorkspaceScheme)
from backend.exception_mapping import generate_responses_for_endpoint
from backend.utils import ProfileDepends, get_ok_response
from domain.exceptions.workspace_exceptions import WorkspaceNotFoundException
from domain.exceptions.workspace_profile_exceptions import CantEditOtherWorkspaceProfileException, CantManipulateRoleException, DontHavePermissionException, NotParticipiantException, WorkspaceProfileNotFoundException
from domain.services import WorkspaceProfileService, WorkspaceService

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


router = APIRouter(
    prefix="/workspace",
    tags=["workspace"]
)


@router.get("/roles", response_model=list[RoleScheme], summary="Get available roles")
async def get_roles(workspace_service: WorkspaceServiceDepends):
    return await workspace_service.get_roles()


@router.post("/{workspace_id}/select", summary="Select workspace",
             responses={**get_ok_response("Workspace successfully selected"),
                        **generate_responses_for_endpoint([NotParticipiantException, WorkspaceNotFoundException])})
async def select_workspace(response: Response, workspace_id: int,
                           workspace_service: WorkspaceServiceDepends,
                           workspace_profile_service: WorkspaceProfileServiceDepends,
                           profile: ProfileDepends):
    workspace = await workspace_service.get_by_id(workspace_id)
    await workspace_profile_service.check_participant(profile, workspace)
    response.set_cookie("workspace", str(workspace.id), max_age=60*60*24*30)
    return {"message": "OK"}


@router.get("/", response_model=list[WorkspaceScheme], summary="Get workspaces")
async def get_workspaces(workspace_service: WorkspaceServiceDepends,
                         profile: ProfileDepends):
    return await workspace_service.get_by_profile(profile)


@router.get("/{workspace_id}", response_model=WorkspaceScheme, summary="Get workspace by id",
            responses=generate_responses_for_endpoint([WorkspaceNotFoundException, NotParticipiantException]))
async def get_workspace(workspace_id: int,
                        workspace_service: WorkspaceServiceDepends,
                        workspace_profile_service: WorkspaceProfileServiceDepends,
                        profile: ProfileDepends):
    workspace = await workspace_service.get_by_id(workspace_id)
    await workspace_profile_service.check_participant(profile, workspace)
    return workspace


@router.post("/", response_model=WorkspaceScheme, summary="Create a new workspace")
async def create_workspace(request: CreateWorkspaceRequest,
                           workspace_service: WorkspaceServiceDepends,
                           workspace_profile_service: WorkspaceProfileServiceDepends,
                           profile: ProfileDepends):
    workspace = await workspace_service.create(profile, request.name, request.params.model_dump())
    role = await workspace_service.get_role(Roles.ADMINISTRATOR)
    await workspace_profile_service.join(profile, workspace, role)
    return workspace


@router.post("/{workspace_id}/change_role", summary="Change workspace user role",
             responses={**get_ok_response("Role successfully changed"),
                        **generate_responses_for_endpoint([
                            WorkspaceNotFoundException,
                            WorkspaceProfileNotFoundException,
                            CantManipulateRoleException,
                            CantEditOtherWorkspaceProfileException
                        ])})
async def change_workspace_user_role(request: ChangeWorkspaceUserRoleRequest, workspace_id: int,
                                     workspace_service: WorkspaceServiceDepends,
                                     workspace_profile_service: WorkspaceProfileServiceDepends,
                                     profile: ProfileDepends):
    workspace = await workspace_service.get_by_id(workspace_id)
    source_wp = await workspace_profile_service.get_by_bind(profile, workspace)
    role = await workspace_service.get_role_by_id(request.role_id)
    target_wp = await workspace_profile_service.get_by_id(request.workspace_profile_id)
    await workspace_profile_service.change_role(source_wp, target_wp, role)
    return {"message": "OK"}


@router.post("/{workspace_id}/kick", summary="Kick user from workspace",
             responses={**get_ok_response("User successfully kicked"),
                        **generate_responses_for_endpoint([
                            WorkspaceNotFoundException,
                            WorkspaceProfileNotFoundException,
                            CantEditOtherWorkspaceProfileException
                        ])})
async def kick_user(request: KickRequest, workspace_id: int,
                    workspace_service: WorkspaceServiceDepends,
                    workspace_profile_service: WorkspaceProfileServiceDepends,
                    profile: ProfileDepends):
    workspace = await workspace_service.get_by_id(workspace_id)
    source_wp = await workspace_profile_service.get_by_bind(profile, workspace)
    target_wp = await workspace_profile_service.get_by_id(request.workspace_profile_id)
    await workspace_profile_service.kick(source_wp, target_wp)
    return {"message": "OK"}


@router.post("/{workspace_id}/leave", summary="Leave workspace",
             responses={**get_ok_response("Leave successful"),
                        **generate_responses_for_endpoint([
                            WorkspaceNotFoundException,
                            WorkspaceProfileNotFoundException
                        ])})
async def leave_workspace(workspace_id: int, res: Response,
                          workspace_service: WorkspaceServiceDepends,
                          workspace_profile_service: WorkspaceProfileServiceDepends,
                          profile: ProfileDepends):
    workspace = await workspace_service.get_by_id(workspace_id)
    wp = await workspace_profile_service.get_by_bind(profile, workspace)
    await workspace_profile_service.leave(wp)
    res.set_cookie("access-token", "", max_age=0, httponly=True)
    return {"message": "OK"}


@router.get("/{workspace_id}/members", response_model=list[WorkspaceProfileScheme], summary="Get workspace members",
            responses=generate_responses_for_endpoint([WorkspaceNotFoundException, NotParticipiantException]))
async def get_workspace_members(workspace_id: int,
                                workspace_service: WorkspaceServiceDepends,
                                workspace_profile_service: WorkspaceProfileServiceDepends,
                                profile: ProfileDepends):
    workspace = await workspace_service.get_by_id(workspace_id)
    await workspace_profile_service.check_participant(profile, workspace)
    return await workspace_service.get_members(workspace)


@router.get("/{workspace_id}/invite", response_model=list[InviteInfo], summary="Get workspace invites",
            responses=generate_responses_for_endpoint([
                WorkspaceNotFoundException,
                WorkspaceProfileNotFoundException,
                DontHavePermissionException
            ]))
async def get_workspace_invites(workspace_id: int,
                                workspace_service: WorkspaceServiceDepends,
                                workspace_profile_service: WorkspaceProfileServiceDepends,
                                profile: ProfileDepends):
    workspace = await workspace_service.get_by_id(workspace_id)
    wp = await workspace_profile_service.get_by_bind(profile, workspace)
    await workspace_profile_service.check_permission(wp, Permissions.moderate_workspace)
    return await workspace_service.get_invites(workspace)


@router.post("/{workspace_id}/invite", response_model=InviteCreated, summary="Create workspace invite",
             responses=generate_responses_for_endpoint([
                 WorkspaceNotFoundException,
                 WorkspaceProfileNotFoundException,
                 DontHavePermissionException
             ]))
async def create_workspace_invite(workspace_id: int, request: InviteCreateRequest,
                                  workspace_service: WorkspaceServiceDepends,
                                  workspace_profile_service: WorkspaceProfileServiceDepends,
                                  profile: ProfileDepends):
    workspace = await workspace_service.get_by_id(workspace_id)
    wp = await workspace_profile_service.get_by_bind(profile, workspace)
    await workspace_profile_service.check_permission(wp, Permissions.moderate_workspace)
    invite = await workspace_service.create_invite(wp, request.use_limit)
    return InviteCreated(key=invite.key)
