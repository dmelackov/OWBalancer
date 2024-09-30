from pydantic import BaseModel

from .workspace_profile import WorkspaceProfileScheme


class TruncInviteInfo(BaseModel):
    creator: WorkspaceProfileScheme

    class Config:
        from_attributes = True


class InviteInfo(BaseModel):
    id: int
    use_limit: int
    key: str
    creator: WorkspaceProfileScheme

    class Config:
        from_attributes = True
