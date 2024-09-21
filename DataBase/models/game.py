import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, JSON, func, DateTime
from typing import Optional
from DataBase.database import Base

from DataBase.models.workspace_profile import WorkspaceProfile

class Game(Base):
    __tablename__ = "game"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    first_team_points: Mapped[int]
    second_team_points: Mapped[int]
    game_static: Mapped[Optional[dict | list]] = mapped_column(type_=JSON)
    game_data: Mapped[Optional[dict | list]] = mapped_column(type_=JSON)
    active: Mapped[bool]
    creator_id: Mapped[int] = mapped_column(ForeignKey("workspace_profile.id"))

    creator: Mapped[WorkspaceProfile] = relationship()
