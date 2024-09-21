from typing import Optional

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from DataBase.database import Base
from DataBase.models.lobby import Lobby
from DataBase.models.profile import Profile

DEFAULT_WORKSPACE_PARAMS = {"CustomSystem": True}


class Workspace(Base):
    __tablename__ = "workspace"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    workspace_params: Mapped[Optional[dict | list]] = mapped_column(type_=JSON,
                                                                    default=DEFAULT_WORKSPACE_PARAMS)
    creator_id: Mapped[int] = mapped_column(ForeignKey("profile.id"))
    lobby_id: Mapped[int] = mapped_column(ForeignKey("lobby.id"))

    creator: Mapped[Profile] = relationship(lazy="selectin")
    lobby: Mapped[Lobby] = relationship()
