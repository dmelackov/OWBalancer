from pydantic import BaseModel

from DataBase.schemes.profile_scheme import ProfileScheme


class WorkspaceScheme(BaseModel):
    id: int
    name: str
    description: str
    creator: ProfileScheme

    class Config:
        orm_mode = True