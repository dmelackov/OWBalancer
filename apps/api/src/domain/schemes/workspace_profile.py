from pydantic import BaseModel

from .profile_scheme import ProfileScheme
from .role_scheme import RoleScheme
from .workspace_scheme import WorkspaceScheme


class WorkspaceProfileScheme(BaseModel):
    id: int
    profile: ProfileScheme
    workspace: WorkspaceScheme
    role: RoleScheme
    active: bool

    class Config:
        from_attributes = True
