from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from backend.dependency import WorkspaceProfileServiceDepends
from backend.utils import ProfileDepends, WorkspaceProfileDepends, WorkspaceProfileOptionalDepends
from balancer_models.models import Profile
from domain.schemes import ProfileScheme, WorkspaceProfileScheme


class InfoResponse(BaseModel):
    permissions: list[str]
    profile: ProfileScheme
    workspace_profile: Optional[WorkspaceProfileScheme]

    class Config:
        from_attributes = True


router = APIRouter(
    prefix="/profile",
    tags=["profile"]
)


@router.get("/",
            response_model=InfoResponse,
            summary="Get profile info")
async def getInfo(workspace_profile_service: WorkspaceProfileServiceDepends,
                  workspace_profile: WorkspaceProfileOptionalDepends,
                  profile: ProfileDepends,
                  ):
    """
    Returns information about current profile.
    """
    response = {
        "profile": profile,
        "workspace_profile": workspace_profile,
        "permissions": await workspace_profile_service.get_permissions(workspace_profile) if workspace_profile else [],
    }
    return response
