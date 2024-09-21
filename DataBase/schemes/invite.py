from pydantic import BaseModel

from DataBase.schemes.workspace_profile import WorkspaceProfileScheme


class TruncInviteInfo(BaseModel):
    creator: WorkspaceProfileScheme

    class Config:
        orm_mode = True

class InviteInfo(BaseModel):
    id: int
    use_limit: int
    key: str
    creator: WorkspaceProfileScheme

    class Config:
        orm_mode = True