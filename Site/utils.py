from typing import Any
from fastapi import Cookie, Depends, HTTPException, Response
from DataBase.database import get_db_session
from DataBase.models.profile import Profile
from DataBase.models.workspace import Workspace
from DataBase.models.workspace_profile import WorkspaceProfile
from DataBase.repository.workspace_profile_repository import WorkspaceProfileRepository
from DataBase.repository.workspace_repository import WorkspaceRepository
from Site.loginManager import manager
from starlette.status import HTTP_404_NOT_FOUND


async def get_workspace(response: Response,
                        workspace: str | None = Cookie(default=None),
                        session=Depends(get_db_session)) -> Workspace | None:
    if workspace is None:
        return None
    if not workspace.isdigit():
        response.set_cookie("workspace",  "", max_age=0)
        return None
    workspace_repository = WorkspaceRepository(session)
    workspace_id = int(workspace)
    workspace_inst = await workspace_repository.get_by_id(workspace_id)
    if workspace_inst is None:
        response.set_cookie("workspace",  "", max_age=0)
        return None
    return workspace_inst


class WorkspaceProfileGetter:
    def __init__(self) -> None:
        pass

    async def __call__(self, response: Response,
                       profile: Profile | None = Depends(manager.optional),
                       workspace: Workspace | None = Depends(get_workspace),
                       session=Depends(get_db_session)) -> WorkspaceProfile:
        if profile is None:
            raise HTTPException(HTTP_404_NOT_FOUND, "Invalid workspace/user")
        if workspace is None:
            raise HTTPException(HTTP_404_NOT_FOUND, "Invalid workspace/user")
        workspace_profile_repository = WorkspaceProfileRepository(session)
        workspaceProfile = await workspace_profile_repository.get_by_bind(profile, workspace)
        if workspaceProfile is None or not workspaceProfile.active:
            response.set_cookie("workspace",  "", max_age=0)
            raise HTTPException(HTTP_404_NOT_FOUND, "Invalid workspace/user")
        return workspaceProfile

    async def optional(self, response: Response,
                       profile: Profile | None = Depends(manager.optional),
                       workspace: Workspace | None = Depends(get_workspace),
                       session=Depends(get_db_session)) -> WorkspaceProfile | None:
        if profile is None:
            return None
        if workspace is None:
            return None
        workspace_profile_repository = WorkspaceProfileRepository(session)
        workspaceProfile = await workspace_profile_repository.get_by_bind(profile, workspace)
        if workspaceProfile is None or not workspaceProfile.active:
            response.set_cookie("workspace",  "", max_age=0)
            return None
        return workspaceProfile


get_workspace_profile = WorkspaceProfileGetter()
