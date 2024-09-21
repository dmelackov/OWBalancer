from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from DataBase.database import Base

from DataBase.models.custom import Custom
from DataBase.models.lobby import Lobby

class LobbyPlayer(Base):
    __tablename__ = "lobby_player"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    lobby_id: Mapped[int] = mapped_column(ForeignKey("lobby.id"))
    custom_id: Mapped[int] = mapped_column(ForeignKey("custom.id"))

    lobby: Mapped[Lobby] = relationship()
    custom: Mapped[Custom] = relationship()
