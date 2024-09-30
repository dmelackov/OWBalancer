from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Perm(Base):
    __tablename__ = "perm"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
