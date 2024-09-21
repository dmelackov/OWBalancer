from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from DataBase.database import Base

from DataBase.models.workspace_profile import WorkspaceProfile

class KeyData(Base):
    __tablename__ = "key_data"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    key: Mapped[str]
    use_limit: Mapped[int] = mapped_column(default=1)
    creator_id: Mapped[int] = mapped_column(ForeignKey("workspace_profile.id"))

    creator: Mapped[WorkspaceProfile] = relationship(lazy="selectin")