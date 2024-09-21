from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette.status import HTTP_404_NOT_FOUND

from DataBase.database import get_db_session
from DataBase.repository.role_repository import RoleRepository
from DataBase.repository.workspace_profile_repository import WorkspaceProfileRepository
from DataBase.schemes.profile_scheme import ProfileScheme
from DataBase.schemes.workspace_profile import WorkspaceProfileScheme
from DataBase.schemes.workspace_scheme import WorkspaceScheme
from Site.loginManager import manager
from Site.utils import get_workspace_profile

from DataBase.models.workspace import Workspace
from DataBase.models.profile import Profile
from DataBase.models.workspace_profile import WorkspaceProfile

from fastapi_controllers import Controller, get


class InfoResponse(BaseModel):
    auth: bool
    profile: Optional[ProfileScheme]
    workspace_profile: Optional[WorkspaceProfileScheme]

    class Config:
        orm_mode = True


class ProfileController(Controller):
    prefix = "/profile"
    tags = ["profile"]

    def __init__(self):
        pass

    @get("/", response_model=InfoResponse)
    async def getInfo(self,
                      profile: Profile | None = Depends(manager.optional),
                      workspace_profile: WorkspaceProfile | None = Depends(get_workspace_profile.optional)):
        response = {"auth": profile is not None,
                    "profile": profile,
                    "workspace_profile": workspace_profile}
        return response

    @get("/permissions", response_model=list[str])
    async def getPermissions(self,
                             workspace_profile: WorkspaceProfile = Depends(
                                 get_workspace_profile),
                             session=Depends(get_db_session)):
        role_repository = RoleRepository(session)
        permissions = await role_repository.get_permissions(workspace_profile.role)
        return list(map(lambda x: x.name, permissions))
