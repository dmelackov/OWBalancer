from sqlalchemy.orm import Mapped, mapped_column

from DataBase.database import Base

class Lobby(Base):
    __tablename__ = "lobby"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
