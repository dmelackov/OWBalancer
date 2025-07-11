from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .player import Player
from .workspace_profile import WorkspaceProfile


class Custom(Base):
    __tablename__ = "custom"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    TSR: Mapped[int] = mapped_column(default=0)
    DSR: Mapped[int] = mapped_column(default=0)
    HSR: Mapped[int] = mapped_column(default=0)
    creator_id: Mapped[int] = mapped_column(ForeignKey("workspace_profile.id"))
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"))

    creator: Mapped[WorkspaceProfile] = relationship()
    player: Mapped[Player] = relationship()
