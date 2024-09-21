from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from DataBase.database import Base

from DataBase.models.workspace_profile import WorkspaceProfile

class Player(Base):
    __tablename__ = "player"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str]
    creator_id: Mapped[int] = mapped_column(ForeignKey("workspace_profile.id"))

    creator: Mapped[WorkspaceProfile] = relationship(lazy="selectin")