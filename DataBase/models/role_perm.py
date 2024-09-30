from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .perm import Perm
from .role import Role


class RolePerm(Base):
    __tablename__ = "role_perm"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))
    perm_id: Mapped[int] = mapped_column(ForeignKey("perm.id"))

    role: Mapped[Role] = relationship(lazy="selectin")
    perm: Mapped[Perm] = relationship(lazy="selectin")
