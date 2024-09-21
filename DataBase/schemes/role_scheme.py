from pydantic import BaseModel


class RoleScheme(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True