import datetime
import json
from typing import Optional
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from sqlalchemy import (JSON, DateTime, ForeignKey, String, TypeDecorator,
                        func, types)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

DEFAULT_WORKSPACE_PARAMS = {"CustomSystem": True}
DEFAULT_LOBBY_DATA = {"Lobby": []}
DEFAULT_WORKSPACE_SETTIGNS = {"AutoIncrement": False, "generalLobby": False}
DEFAULT_PROFILE_DATA = {"Amount": {"T": 1, "D": 2, "H": 2}, "TeamNames": {"1": "Team 1", "2": "Team 2"},
                        "AutoCustom": False, "ExtendedLobby": True, "Autoincrement": False, "BalanceLimit": 2500,
                        "fColor": "#1e90ff", "sColor": "#ff6347", "ExpandedResult": True, "Math": {"alpha": 3.0,
                                                                                                   "beta": 1.0, "gamma": 80.0, "p": 2.0, "q": 2.0, "tWeight": 1.1, "dWeight": 1.0, "hWeight": 0.9}}


class Base(DeclarativeBase):
    pass


class Profile(Base):
    __tablename__ = "profile"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str]
    password: Mapped[str]
    settings: Mapped[Optional[dict | list]] = mapped_column(
        type_=JSON, default=DEFAULT_PROFILE_DATA)
    active: Mapped[bool] = mapped_column(default=True)
    secret: Mapped[str]


class Workspace(Base):
    __tablename__ = "workspace"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    workspace_params: Mapped[Optional[dict | list]] = mapped_column(type_=JSON,
                                                                    default=DEFAULT_WORKSPACE_PARAMS)
    lobby: Mapped[Optional[dict | list]] = mapped_column(
        type_=JSON, default=DEFAULT_LOBBY_DATA)


class KeyData(Base):
    __tablename__ = "key_data"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    key: Mapped[str]
    use_limit: Mapped[int] = mapped_column(default=1)
    creator_id: Mapped[int] = mapped_column(ForeignKey("workspace_profile.id"))

    creator: Mapped["WorkspaceProfile"] = relationship()


class WorkspaceProfile(Base):
    __tablename__ = "workspace_profile"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customers: Mapped[Optional[dict | list]] = mapped_column(type_=JSON,
                                                             default=DEFAULT_LOBBY_DATA)
    workspace_settings: Mapped[Optional[dict | list]] = mapped_column(type_=JSON,
                                                                      default=DEFAULT_WORKSPACE_SETTIGNS)
    active: Mapped[bool] = mapped_column(default=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspace.id"))
    profile_id: Mapped[int] = mapped_column(ForeignKey("profile.id"))

    profile: Mapped["Profile"] = relationship()
    role: Mapped["Role"] = relationship()
    workspace: Mapped["Workspace"] = relationship()


class Player(Base):
    __tablename__ = "player"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str]
    creator_id: Mapped[int] = mapped_column(ForeignKey("workspace_profile.id"))

    creator: Mapped["WorkspaceProfile"] = relationship()


class PlayerRoles(Base):
    __tablename__ = "player_roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    roles: Mapped[str] = mapped_column(default="")
    is_flex: Mapped[bool] = mapped_column(default=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey("workspace_profile.id"))
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"))

    creator: Mapped["WorkspaceProfile"] = relationship()
    player: Mapped["Player"] = relationship()


class Custom(Base):
    __tablename__ = "custom"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    TSR: Mapped[int] = mapped_column(default=0)
    DSR: Mapped[int] = mapped_column(default=0)
    HSR: Mapped[int] = mapped_column(default=0)
    creator_id: Mapped[int] = mapped_column(ForeignKey("workspace_profile.id"))
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"))

    creator: Mapped["WorkspaceProfile"] = relationship()
    player: Mapped["Player"] = relationship()


class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)


class Perm(Base):
    __tablename__ = "perm"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]


class RolePerm(Base):
    __tablename__ = "role_perm"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


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

    creator: Mapped["WorkspaceProfile"] = relationship()
