from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel, Field
from starlette.status import (HTTP_403_FORBIDDEN,
                              HTTP_404_NOT_FOUND,
                              HTTP_500_INTERNAL_SERVER_ERROR)

from DataBase.database import get_db_session
from DataBase.models.profile import Profile
from DataBase.models.workspace import Workspace
from DataBase.models.workspace_profile import WorkspaceProfile
from DataBase.permissions import Permissions
from DataBase.repository.invite_repository import InviteRepository
from DataBase.repository.role_repository import RoleRepository
from DataBase.repository.workspace_profile_repository import WorkspaceProfileRepository
from DataBase.repository.workspace_repository import WorkspaceRepository
from DataBase.roles import Roles
from DataBase.schemes.invite import InviteInfo
from DataBase.schemes.role_scheme import RoleScheme
from DataBase.schemes.workspace_profile import WorkspaceProfileScheme
from DataBase.schemes.workspace_scheme import WorkspaceScheme
from Site.service.workspace_profile_service import WorkspaceProfileService
from Site.service.workspace_service import WorkspaceService
from Site.loginManager import manager
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_controllers import Controller, post, get, delete


class CreateWorkspaceParams(BaseModel):
    CustomSystem: bool


class CreateWorkspaceRequest(BaseModel):
    name: str
    params: CreateWorkspaceParams


class ChangeWorkspaceUserRoleRequest(BaseModel):
    workspace_profile_id: int
    role_id: int


class InviteCreateRequest(BaseModel):
    use_limit: int = Field(ge=0, le=11)


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

    @get("/roles", response_model=list[RoleScheme])
    async def get_roles(self):
        return await self.workspace_service.get_roles()

    @post("/{workspace_id}/select")
    async def select_workspace(self,
                               response: Response,
                               workspace_id: int):
        workspace = await self.workspace_service.get_by_id(workspace_id)
        await self.workspace_profile_service.check_participant(self.profile, workspace)

        response.set_cookie("workspace", str(workspace.id),
                            max_age=60*60*24*30)  # 1 month
        return {"message": "OK"}

    @get("/", response_model=list[WorkspaceScheme])
    async def get_workspaces(self):
        return await self.workspace_service.get_by_profile(self.profile)

    @get("/{workspace_id}", response_model=WorkspaceScheme)
    async def get_workspace(self,
                            workspace_id: int):
        workspace = await self.workspace_service.get_by_id(workspace_id)
        await self.workspace_profile_service.check_participant(self.profile, workspace)

        return workspace

    @post("/", response_model=WorkspaceScheme)
    async def create_workspace(self,
                               request: CreateWorkspaceRequest):
        workspace = await self.workspace_service.create(self.profile, request.name, request.params.model_dump())
        role = await self.workspace_service.get_role(Roles.ADMINISTRATOR)

        await self.workspace_profile_service.join(self.profile, workspace, role)

        await self.session.commit()
        return workspace

    @post("/{workspace_id}/change_role")
    async def changeWorkspaceUserRole(self,
                                      request: ChangeWorkspaceUserRoleRequest,
                                      workspace_id: int,):
        workspace = await self.workspace_service.get_by_id(workspace_id)
        workspace_profile = await self.workspace_profile_service.get_by_bind(self.profile, workspace)
        role = await self.workspace_service.get_role_by_id(request.role_id)

        target_workspace_profile = await self.workspace_profile_service.get_by_id(request.workspace_profile_id)
        await self.workspace_profile_service.change_role(workspace_profile, target_workspace_profile, role)
        await self.session.commit()
        return {"message": "OK"}

    @post("/{workspace_id}/kick")
    async def kick(self,
                   request: KickRequest,
                   workspace_id: int):
        workspace = await self.workspace_service.get_by_id(workspace_id)
        workspace_profile = await self.workspace_profile_service.get_by_bind(self.profile, workspace)

        target_workspace_profile = await self.workspace_profile_service.get_by_id(request.workspace_profile_id)
        await self.workspace_profile_service.kick(workspace_profile, target_workspace_profile)

        await self.session.commit()
        return {"message": "OK"}

    @post("/{workspace_id}/leave")
    async def workspace_leave(self,
                              res: Response,
                              workspace_id: int):
        workspace = await self.workspace_service.get_by_id(workspace_id)
        workspace_profile = await self.workspace_profile_service.get_by_bind(self.profile, workspace)

        await self.workspace_profile_service.leave(workspace_profile)

        await self.session.commit()
        res.set_cookie("access-token", "", max_age=0, httponly=True)
        return {"message": "OK"}

    @get("/{workspace_id}/members", response_model=list[WorkspaceProfileScheme])
    async def get_workspace_members(self,
                                    workspace_id: int):
        workspace = await self.workspace_service.get_by_id(workspace_id)
        await self.workspace_profile_service.check_participant(self.profile, workspace)

        return await self.workspace_service.get_members(workspace)

    @get("/{workspace_id}/invite", response_model=list[InviteInfo])
    async def get_workspace_invites(self,
                                    workspace_id: int):
        workspace = await self.workspace_service.get_by_id(workspace_id)
        workspace_profile = await self.workspace_profile_service.get_by_bind(self.profile, workspace)
        await self.workspace_profile_service.check_permission(workspace_profile, Permissions.moderate_workspace)

        return self.workspace_service.get_invites(workspace)

    @post("/{workspace_id}/invite", response_model=InviteCreated)
    async def create_workspace_invite(self,
                                      workspace_id: int,
                                      request: InviteCreateRequest):
        workspace = await self.workspace_service.get_by_id(workspace_id)
        workspace_profile = await self.workspace_profile_service.get_by_bind(self.profile, workspace)
        await self.workspace_profile_service.check_permission(workspace_profile, Permissions.moderate_workspace)

        invite = await self.workspace_service.create_invite(workspace_profile, request.use_limit)
        await self.session.commit()
        return InviteCreated(key=invite.key)
