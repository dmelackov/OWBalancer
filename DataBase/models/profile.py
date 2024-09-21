from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from DataBase.database import Base
from sqlalchemy import JSON

DEFAULT_PROFILE_DATA = {
    "amount": {
        "tank": 1,
        "damage": 2,
        "support": 2
    },
    "team": {
        "first": {
            "name": "Team 1",
            "color": "#1e90ff"
        },
        "second": {
            "name": "Team 2",
            "color": "#ff6347"
        }
    },
    "auto_custom": False,
    "extended_lobby": True,
    "auto_increment": False,
    "expanded_result": True,
    "math": {
        "balance_limit": 2500,
        "alpha": 3.0,
        "beta": 1.0,
        "gamma": 80.0,
        "p": 2.0,
        "q": 2.0,
        "tank_weight": 1.1,
        "damage_weight": 1.0,
        "support_weight": 1.1
    }
}


class Profile(Base):
    __tablename__ = "profile"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[Optional[str]]
    settings: Mapped[Optional[dict | list]] = mapped_column(
        type_=JSON, default=DEFAULT_PROFILE_DATA)
    active: Mapped[bool] = mapped_column(default=True)
    secret: Mapped[Optional[str]]
