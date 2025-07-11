from enum import Enum

from pydantic import BaseModel

from .workspace_profile import WorkspaceProfileScheme


class PlayerBaseScheme(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class PlayerScheme(BaseModel):
    id: int
    username: str
    creator: WorkspaceProfileScheme

    class Config:
        from_attributes = True


class Role(Enum):
    TANK = "t"
    DAMAGE = "d"
    SUPPORT = "s"


class PlayerRoleScheme(BaseModel):
    active: bool
    role: Role


class PlayerWithRolesScheme(BaseModel):
    id: int
    username: str
    creator: WorkspaceProfileScheme
    roles: list[PlayerRoleScheme]
