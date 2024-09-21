from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from DataBase.database import Base
from sqlalchemy import ForeignKey, JSON

from DataBase.models.profile import Profile
from DataBase.models.role import Role 
from DataBase.models.workspace import Workspace
from DataBase.models.lobby import Lobby

DEFAULT_WORKSPACE_SETTIGNS = {"AutoIncrement": False, "generalLobby": False}


class WorkspaceProfile(Base):
    __tablename__ = "workspace_profile"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    workspace_settings: Mapped[Optional[dict | list]] = mapped_column(type_=JSON,
                                                                      default=DEFAULT_WORKSPACE_SETTIGNS)
    active: Mapped[bool] = mapped_column(default=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspace.id"))
    profile_id: Mapped[int] = mapped_column(ForeignKey("profile.id"))
    lobby_id: Mapped[int] = mapped_column(ForeignKey("lobby.id"))

    profile: Mapped[Profile] = relationship(lazy="selectin")
    role: Mapped[Role] = relationship(lazy="selectin")
    workspace: Mapped[Workspace] = relationship(lazy="selectin")
    lobby: Mapped[Lobby] = relationship()
