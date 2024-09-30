from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .player import Player
from .workspace_profile import WorkspaceProfile


class PlayerRoles(Base):
    __tablename__ = "player_roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    roles: Mapped[str] = mapped_column(default="")
    is_flex: Mapped[bool] = mapped_column(default=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey("workspace_profile.id"))
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"))

    creator: Mapped[WorkspaceProfile] = relationship()
    player: Mapped[Player] = relationship()
