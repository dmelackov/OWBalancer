from pydantic import BaseModel

from DataBase.schemes.profile_scheme import ProfileScheme
from DataBase.schemes.role_scheme import RoleScheme
from DataBase.schemes.workspace_scheme import WorkspaceScheme


class WorkspaceProfileScheme(BaseModel):
    id: int
    profile: ProfileScheme
    workspace: WorkspaceScheme
    role: RoleScheme
    active: bool

    class Config:
        orm_mode = True