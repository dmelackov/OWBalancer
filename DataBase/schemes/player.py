from pydantic import BaseModel

from DataBase.schemes.workspace_profile import WorkspaceProfileScheme


class PlayerBaseScheme(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class PlayerScheme(BaseModel):
    id: int
    username: str
    creator: WorkspaceProfileScheme

    class Config:
        orm_mode = True


class PlayerRoleScheme(BaseModel):
    active: bool
    role: str

class PlayerWithRolesScheme(BaseModel):
    id: int
    username: str
    creator: WorkspaceProfileScheme
    roles: list[PlayerRoleScheme]