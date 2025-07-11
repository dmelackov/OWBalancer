from typing import Annotated, Any, Dict
from fastapi import Cookie, Depends, HTTPException, Response
from starlette.status import HTTP_404_NOT_FOUND

from backend.dependency import DB_SESSION, WorkspaceServiceDepends
from balancer_models.models.profile import Profile
from balancer_models.models.workspace import Workspace
from balancer_models.models.workspace_profile import WorkspaceProfile
from balancer_models.repository.workspace_profile_repository import \
    WorkspaceProfileRepository
from balancer_models.repository.workspace_repository import WorkspaceRepository


def get_ok_response(description) -> Dict[int | str, Dict[str, Any]]:
    OK_RESPONSE = {
        200: {
            "description": description,
            "content": {
                "application/json": {
                    "example": {"message": "OK"}
                }
            }
        }}
    return OK_RESPONSE  # type: ignore


async def get_optional_profile() -> Profile | None:
    ...


async def get_profile() -> Profile:
    ...

ProfileOptionalDepends = Annotated[Profile |
                                   None, Depends(get_optional_profile)]
ProfileDepends = Annotated[Profile, Depends(get_profile)]


async def get_workspace(response: Response,
                        workspace_repository: WorkspaceServiceDepends,
                        workspace: str | None = Cookie(default=None)) -> Workspace | None:
    if workspace is None:
        return None
    if not workspace.isdigit():
        response.set_cookie("workspace",  "", max_age=0)
        return None
    workspace_id = int(workspace)
    workspace_inst = await workspace_repository.get_by_id(workspace_id)
    if workspace_inst is None:
        response.set_cookie("workspace",  "", max_age=0)
        return None
    return workspace_inst


async def get_workspace_profile(self, response: Response,
                                session: DB_SESSION,
                                profile: ProfileOptionalDepends,
                                workspace: Workspace | None = Depends(
                                    get_workspace),
                                ) -> WorkspaceProfile:
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


async def get_workspace_profile_optional(self, response: Response,
                                         session: DB_SESSION,
                                         profile: ProfileOptionalDepends,
                                         workspace: Workspace | None = Depends(
                                             get_workspace)
                                         ) -> WorkspaceProfile | None:
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


WorkspaceProfileDepends = Annotated[WorkspaceProfile, Depends(
    get_workspace_profile)]
WorkspaceProfileOptionalDepends = Annotated[WorkspaceProfile | None, Depends(
    get_workspace_profile_optional)]
