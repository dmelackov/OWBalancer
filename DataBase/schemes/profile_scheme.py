from pydantic import BaseModel


class ProfileScheme(BaseModel):
    id: int
    username: str
    active: bool

    class Config:
        orm_mode = True
