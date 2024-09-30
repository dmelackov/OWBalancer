from pydantic import BaseModel

from .profile_scheme import ProfileScheme


class WorkspaceScheme(BaseModel):
    id: int
    name: str
    description: str
    creator: ProfileScheme

    class Config:
        from_attributes = True
