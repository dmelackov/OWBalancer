from typing import Optional

from fastapi import Depends
from fastapi_controllers import Controller, get
from pydantic import BaseModel

from DataBase.database import get_db_session
from DataBase.models.profile import Profile
from DataBase.models.workspace_profile import WorkspaceProfile
from DataBase.schemes.profile_scheme import ProfileScheme
from DataBase.schemes.workspace_profile import WorkspaceProfileScheme
from Site.loginManager import manager
from Site.service.workspace_profile_service import WorkspaceProfileService
from Site.utils import get_workspace_profile


class InfoResponse(BaseModel):
    auth: bool
    profile: Optional[ProfileScheme]
    workspace_profile: Optional[WorkspaceProfileScheme]

    class Config:
        orm_mode = True


class ProfileController(Controller):
    prefix = "/profile"
    tags = ["profile"]

    def __init__(self,
                 session=Depends(get_db_session)):
        self.workspace_profile_service = WorkspaceProfileService(session)

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
                                 get_workspace_profile)):
        return self.workspace_profile_service.get_permissions(workspace_profile)
