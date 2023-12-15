from datetime import datetime
from enum import Enum
from typing import Any, List, Union

from pydantic import BaseModel


class Roles(BaseModel):
    ID: int
    Name: str


class Profile(BaseModel):
    ID: int
    Username: str


class Workspace(BaseModel):
    ID: int
    Name: str
    Description: str
    Creator: Profile


class KeyData(BaseModel):
    ID: int
    Key: str
    Workspace: Workspace
    UseLimit: int
    Creator: Profile


class WorkspaceProfile(BaseModel):
    ID: int
    Profile: Profile
    Role: Roles
    Workspace: Workspace
    Active: bool


class Player(BaseModel):
    ID: int
    Username: str
    Creator: WorkspaceProfile


class GameRole(Enum):
    tank = "T"
    heal = "H"
    damage = "D"


class PlayerRole(BaseModel):
    active: bool
    role: GameRole
    sr: int


class Custom(BaseModel):
    ID: int
    Creator: WorkspaceProfile
    Player: Player
    Roles: list[PlayerRole]
    isFlex: bool


class Perms(BaseModel):
    ID: int
    Name: str


class RolePerms(BaseModel):
    ID: int
    Role: Roles
    Perm: Perms


class Games(BaseModel):
    ID: int
    Creator: Profile
    Timestamp: datetime
    Winner: int
