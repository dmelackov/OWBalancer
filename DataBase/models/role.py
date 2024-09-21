from sqlalchemy.orm import Mapped, mapped_column
from DataBase.database import Base

class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)