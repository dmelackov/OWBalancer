from pydantic import BaseModel

from . import WorkspaceProfileScheme, PlayerScheme, PlayerRoleScheme

class CustomScheme(BaseModel):
    id: int
    TSR: int
    DSR: int
    HSR: int

    creator: WorkspaceProfileScheme
    player: PlayerScheme

    class Config:
        from_attributes = True

class CustomRoledScheme(BaseModel):
    id: int
    TSR: int
    DSR: int
    HSR: int

    creator: WorkspaceProfileScheme
    player: PlayerRoleScheme

    class Config:
        from_attributes = True