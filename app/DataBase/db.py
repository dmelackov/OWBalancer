from __future__ import annotations

import json
import secrets
from datetime import datetime as dt
from typing import Union

from peewee import *
from werkzeug.security import check_password_hash, generate_password_hash

import app.DataBase.dataModels as dataModels
from app.DataBase.permissions import Permissions
from app.params import (DB_HOST, DB_NAME, DB_PORT, DB_TYPE, DB_USER_LOGIN,
                        DB_USER_PASSWORD)
from app.Static.globalClasses import AnswerForm

defaultWorkspaceParams = '{"CustomSystem": true}'
defaultLobbyData = '{"Lobby": []}'
defaultWorkspaceSettings = '{"AutoIncrement": false, "generalLobby": false}'


if DB_TYPE == "mysql":
    db = MySQLDatabase(DB_NAME, host=DB_HOST, port=DB_PORT,
                       user=DB_USER_LOGIN, password=DB_USER_PASSWORD)
else:
    db = SqliteDatabase(DB_NAME + ".db")


class DefaultModel(Model):
    class Meta:
        database = db


class Roles(DefaultModel):
    ID: int = PrimaryKeyField()
    Name: str = TextField(unique=True)

    @classmethod
    def getInstance(cls, ID: int) -> Union[Roles, None]:
        R = Roles.select().where(Roles.ID == ID)
        if R:
            return R[0]
        else:
            return None

    @classmethod
    def create(cls, Name: str) -> AnswerForm[Union[None, Roles]]:
        R = Roles.select().where(Roles.Name == Name)
        if not R.exists():
            R = super().create(Name=Name)
            return AnswerForm(status=True, error=None, data=R)
        else:
            return AnswerForm(status=False, error="instance_already_exist")

    @classmethod
    def getRole(cls, Name) -> AnswerForm[Union[None, Roles]]:
        R = Roles.select().where(Roles.Name == Name)
        if R:
            return AnswerForm(status=True, error=None, data=R[0])
        else:
            return AnswerForm(status=False, error="instance_not_exist")

    def getJson(self) -> dataModels.Roles:
        return dataModels.Roles(ID=self.ID, Name=self.Name)


defaultProfileData = '{"Amount": {"T": 1, "D": 2, "H": 2}, "TeamNames": {"1": "Team 1", "2": "Team 2"},' \
    ' "AutoCustom": false, "ExtendedLobby": true, "Autoincrement": false, "BalanceLimit": 2500,' \
    '"fColor": "#1e90ff", "sColor": "#ff6347", "ExpandedResult": true, "Math":{"alpha": 3.0, ' \
    '"beta": 1.0, "gamma": 80.0, "p": 2.0, "q": 2.0, "tWeight": 1.1, "dWeight": 1.0, "hWeight": 0.9}}'


class Profile(DefaultModel):
    ID: int = PrimaryKeyField()
    Username: str = TextField()
    Password: str = TextField(null=True)
    LobbySettings: str = TextField(default=defaultProfileData)
    Secret: str = TextField()

    @classmethod
    def create(cls, Username: str, Password: str) -> AnswerForm[Union[None, Profile]]:
        if not Profile.select().where(Profile.Username == Username).exists():
            U = super().create(Username=Username)
            U.set_password(Password)
            U.save()
            return AnswerForm(status=True, error=None, data=U)
        else:
            return AnswerForm(status=True, error="already_exist")

    @classmethod
    def getInstance(cls, ID: int) -> Union[Profile, None]:
        U = Profile.select().where(Profile.ID == ID)
        if U:
            return U[0]
        else:
            return None

    @classmethod
    def getProfile(cls, Username: str) -> Union[Profile, None]:
        U = Profile.select().where(fn.lower(Profile.Username) == Username.lower())
        if U:
            return U[0]
        else:
            return None

    @classmethod
    def check(cls, Username: str, Password: str) -> AnswerForm[Union[None, Profile]]:
        U = Profile.select().where(fn.lower(Profile.Username) == Username.lower())
        if U and U[0].check_password(Password):
            return AnswerForm(status=True, error=None, data=U[0])
        else:
            return AnswerForm(status=False, error="invalid_login")

    def set_password(self, Password: str) -> None:
        self.Password = generate_password_hash(Password)
        self.Secret = secrets.token_urlsafe(8)
        self.save()

    def check_password(self, Password: str) -> bool:
        return check_password_hash(self.Password, Password)

    def getJson(self) -> dataModels.Profile:
        return dataModels.Profile(ID=self.ID, Username=self.Username)

    def getCustom(self, Player_ID: int) -> AnswerForm[Union[None, Custom]]:
        C = Custom.select().where(Custom.Player == Player_ID, Custom.Creator == self)
        if C.exists():
            return AnswerForm(status=True, error=None, data=C[0])
        else:
            return AnswerForm(status=False, error="instance_not_exist")

    def setUserSettings(self, USettings: dict) -> None:
        self.LobbySettings = json.dumps(USettings)
        self.save()

    def getUserSettings(self) -> dict:
        return json.loads(self.LobbySettings)

    def getWorkspaceList(self):
        WUs = WorkspaceProfile.select().where(WorkspaceProfile.Profile == self)
        return AnswerForm(status=True, error=None, data=[WU.Workspace for WU in WUs])


class Workspace(DefaultModel):
    ID: int = PrimaryKeyField()
    Name: str = TextField()
    Description: str = TextField(default="")
    Creator: Profile = ForeignKeyField(Profile, to_field="ID")
    WorkspaceParams: str = TextField(default=defaultWorkspaceParams)
    Lobby: str = TextField(default=defaultLobbyData)

    @classmethod
    def create(cls, U: Profile, Name: str, WorkspaceParams: str) -> AnswerForm[Workspace]:
        W = super().create(Creator=U, Name=Name, WorkspaceParams=WorkspaceParams)
        return AnswerForm(status=True, error=None, data=W)

    @classmethod
    def getInstance(cls, ID: int) -> Union[Workspace, None]:
        W = Workspace.select().where(Workspace.ID == ID)
        if W:
            return W[0]
        else:
            return None

    def searchPlayers(self, search_query: str) -> list[Player]:
        query = []
        WUs = WorkspaceProfile.select().where(WorkspaceProfile.Workspace == self)
        for P in Player.select().where(Player.Creator << WUs):
            if search_query.lower() in P.Username.lower():
                query.append(P)
        return query

    def getJson(self) -> dataModels.Workspace:
        return dataModels.Workspace(ID=self.ID, Name=self.Name, Description=self.Description, Creator=self.Creator.getJson())

    def setWorkspaceDescription(self, Desc: str) -> None:
        self.Description = Desc
        self.save()

    def joinWorkspace(self, U: Profile, InviteKey: KeyData) -> AnswerForm[Union[None, WorkspaceProfile]]:
        WU = WorkspaceProfile.select().where(WorkspaceProfile.Profile ==
                                             U and WorkspaceProfile.Workspace == self)
        if WU:
            if not WU[0].Active:
                WU[0].Active = 1
                WU[0].save()
                return AnswerForm(status=True, error=None, data=WU[0])
            else:
                return AnswerForm(status=False, error="already_in")

        if InviteKey.UseLimit > 0:
            InviteKey.UseLimit -= 1
        elif InviteKey.UseLimit == 0:
            return AnswerForm(status=False, error="use_limit")

        WU = WorkspaceProfile.create(U, self).data
        return AnswerForm(status=True, error=None, data=WU)

    def getWorkspaceProfile(self, U: Profile) -> AnswerForm[Union[None, WorkspaceProfile]]:
        WU = WorkspaceProfile.select().where(WorkspaceProfile.Profile ==
                                             U, WorkspaceProfile.Workspace == self)
        if WU:
            return AnswerForm(status=True, error=None, data=WU[0])
        else:
            return AnswerForm(status=False, error="instance_not_exist")

    def getWorkspaceParams(self):
        return json.loads(self.WorkspaceParams)
    
    def getWorkspaceMembers(self) -> list[WorkspaceProfile]:
        return WorkspaceProfile.select().where(WorkspaceProfile.Workspace == self)


class KeyData(DefaultModel):
    ID: int = PrimaryKeyField()
    Key: str = TextField()
    Workspace: Workspace = ForeignKeyField(Workspace, to_field="ID")
    UseLimit: int = IntegerField(default=1)
    Creator: Profile = ForeignKeyField(Profile, to_field="ID")

    @classmethod
    def create(cls, U, W, UseLimit=1) -> AnswerForm[KeyData]:
        Key = W.ID + secrets.token_urlsafe(8)
        while KeyData.select().where(KeyData.Key == Key):
            Key = W.ID + secrets.token_urlsafe(8)
        KD = super().create(Key=Key, Workspace=W, Creator=U, UseLimit=UseLimit)
        return AnswerForm(status=True, error=None, data=KD)

    @classmethod
    def getByKey(cls, Key: str) -> AnswerForm[Union[None, KeyData]]:
        KD = KeyData.select().where(KeyData.Key == Key)
        if KD:
            return AnswerForm(status=True, error=None, data=KD[0])
        else:
            return AnswerForm(status=False, error="instance_not_exist")

    def getJson(self):
        return {
            "workspace": self.Workspace.getJson(),
            "creator": self.Creator.getJson()
        }


class WorkspaceProfile(DefaultModel):
    ID: int = PrimaryKeyField()
    Profile: Profile = ForeignKeyField(Profile, to_field="ID")
    Customers: str = TextField(default=defaultLobbyData)
    Role: Roles = ForeignKeyField(Roles, to_field="ID", null=True)
    Workspace: Workspace = ForeignKeyField(Workspace, to_field="ID")
    WorkspaceSettings: str = TextField(default=defaultWorkspaceSettings)
    Active: bool = BooleanField(default=True)

    @classmethod
    def getInstance(cls, ID: int) -> Union[WorkspaceProfile, None]:
        WU = WorkspaceProfile.select().where(WorkspaceProfile.ID == ID)
        if WU:
            return WU[0]
        else:
            return None

    @classmethod
    def create(cls, U, W) -> AnswerForm[WorkspaceProfile]:
        WU = WorkspaceProfile.select().where(WorkspaceProfile.Profile ==
                                             U, WorkspaceProfile.Workspace == W)
        if WU and not WU[0].Active:
            WU[0].Active = True
            WU[0].save()
            return AnswerForm(status=True, error=None, data=WU[0])
        else:
            WU = super().create(Profile=U, Workspace=W)
            return AnswerForm(status=True, error=None, data=WU)

    @classmethod
    def getWU(cls, U: Profile, W: Workspace) -> AnswerForm[Union[None, WorkspaceProfile]]:
        WU = WorkspaceProfile.select().where(WorkspaceProfile.Profile ==
                                             U, WorkspaceProfile.Workspace == W)
        if WU:
            return AnswerForm(status=True, error=None, data=WU[0])
        else:
            return AnswerForm(status=False, error="instance_not_exist")

    def getPermissions(self) -> AnswerForm[Union[None, list[Perms]]]:
        if self.Role is not None:
            RPs = RolePerms.select().where(RolePerms.Role == self.Role)
            mass = []
            for RP in RPs:
                mass.append(RP.Perm)
            return AnswerForm(status=True, error=None, data=mass)
        else:
            return AnswerForm(status=False, error="empty_role")

    def checkPermission(self, Perm: Permissions) -> bool:
        PRs = self.getPermissions().data
        if PRs:
            if Perm.value in [i.Name for i in PRs]:
                return True
        return False

    def getLobbyInfo(self) -> list:
        WSettings = json.loads(self.WorkspaceSettings)
        if WSettings["generalLobby"]:
            LobbyData = json.loads(self.Workspace.Lobby)
        else:
            LobbyData = json.loads(self.Customers)
        CustomChecker = [C.ID for C in Custom.select().where(
            Custom.ID << LobbyData["Lobby"])]
        if len(CustomChecker) != len(LobbyData["Lobby"]):
            self.updateLobbyInfo(CustomChecker)
        return CustomChecker

    def updateLobbyInfo(self, mass: list) -> None:
        WSettings = json.loads(self.WorkspaceSettings)
        d = {"Lobby": mass}
        if WSettings["generalLobby"]:
            self.Workspace.Lobby = json.dumps(d)
            self.Workspace.save()
        else:
            self.Customers = json.dumps(d)
            self.save()

    def setRole(self, Role: Roles) -> AnswerForm[None]:
        if self.Role != Role:
            self.Role = Role
            self.save()
            return AnswerForm(status=True, error=None)
        else:
            return AnswerForm(status=False, error="role_already_given")

    def addToLobby(self, C: Custom) -> AnswerForm[None]:
        CMass = self.getLobbyInfo()
        USettings = self.Profile.getUserSettings()
        TeamPlayers = USettings["Amount"]["T"] + \
            USettings["Amount"]["D"] + USettings["Amount"]["H"]
        if len(CMass) < TeamPlayers * 2 or USettings["ExtendedLobby"]:
            cacheToChange = -1
            for C_ID in CMass:
                LobbyC = Custom.getInstance(C_ID)
                if not LobbyC:
                    return AnswerForm(status=False, error="broken_lobby")
                if LobbyC and LobbyC.Player == C.Player:
                    cacheToChange = C_ID
            if cacheToChange != -1:
                CMass.remove(cacheToChange)

            if C.ID not in CMass:
                CMass.append(C.ID)
            self.updateLobbyInfo(CMass)
            return AnswerForm(status=True, error=None)
        return AnswerForm(status=False, error="lobby_is_overflowing")

    def DeleteFromLobby(self, Custom_ID):
        C = Custom.getInstance(Custom_ID)
        if C:
            CMass = self.getLobbyInfo()

            if C.ID in CMass:
                CMass.remove(C.ID)
            self.updateLobbyInfo(CMass)
            return AnswerForm(status=True, error=None)
        return AnswerForm(status=True, error="instance_not_exist")

    def ClearLobby(self):
        self.updateLobbyInfo([])
        return AnswerForm(status=True, error=None)

    def getJson(self) -> dataModels.WorkspaceProfile:
        return dataModels.WorkspaceProfile(ID=self.ID, Profile=self.Profile.getJson(), Role=self.Role.getJson(), Workspace=self.Workspace.getJson(), Active=self.Active)


class Player(DefaultModel):
    ID: int = PrimaryKeyField()
    Username: str = TextField(null=True)
    Creator: WorkspaceProfile = ForeignKeyField(
        WorkspaceProfile, to_field="ID")

    @classmethod
    def create(cls, WU: WorkspaceProfile, Username: str) -> AnswerForm[Union[None, Player]]:
        if Username:
            P = Player.select().join(WorkspaceProfile).where(Player.Username == Username, WorkspaceProfile.Workspace == WU.Workspace)
            if not P.exists():
                P = super().create(Username=Username, Creator=WU)
            else:
                P = P[0]
            PR = PlayerRoles.getPR(WU, P)
            if not PR:
                PlayerRoles.create(Creator=WU, Player=P)
            return AnswerForm(status=True, error=None, data=P)
        return AnswerForm(status=False, error="username_is_empty")

    @classmethod
    def getInstance(cls, ID: int) -> Union[Player, None]:
        P = Player.select().where(Player.ID == ID)
        if P:
            return P[0]
        else:
            return None

    def getJson(self) -> dataModels.Player:
        return dataModels.Player(ID=self.ID, Username=self.Username, Creator=self.Creator.getJson())


class PlayerRoles(DefaultModel):
    ID: int = PrimaryKeyField()
    Creator: WorkspaceProfile = ForeignKeyField(
        WorkspaceProfile, to_field="ID")
    Player: Player = ForeignKeyField(Player, to_field="ID")
    Roles: str = TextField(default="")
    isFlex: bool = BooleanField(default=False)

    @classmethod
    def getInstance(cls, ID: int) -> Union[PlayerRoles, None]:
        PR = PlayerRoles.select().where(PlayerRoles.ID == ID)
        if PR:
            return PR[0]
        else:
            return None

    @classmethod
    def getPR(cls, WU: WorkspaceProfile, P) -> AnswerForm[Union[None, PlayerRoles]]:
        PR = PlayerRoles.select().where(PlayerRoles.Player == P, PlayerRoles.Creator == WU)
        if PR.exists():
            return AnswerForm(status=True, error=None, data=PR[0])
        else:
            return AnswerForm(status=False, error="instance_not_exist")

    def getJsonRoles(self) -> list[dataModels.PlayerRole]:
        if self.isFlex:
            return [dataModels.PlayerRole(active=True, role=i, sr=0) for i in "TDH"]
        else:
            priority = [dataModels.PlayerRole(active=True, role=i, sr=0) for i in self.Roles] + \
                       [dataModels.PlayerRole(active=False, role=i, sr=0)
                           for i in "TDH" if i not in self.Roles]
        return priority

    def setRoles(self, newRoles: str) -> AnswerForm[None]:
        if all(i in "TDH" for i in newRoles):
            self.Roles = newRoles
            self.save()
            return AnswerForm(status=True, error=None)
        else:
            return AnswerForm(status=False, error="role_presentation_error")

    def setFlex(self, Flex: bool) -> AnswerForm[None]:
        self.isFlex = bool(Flex)
        self.save()
        return AnswerForm(status=True, error=None)


class Custom(DefaultModel):
    ID: int = PrimaryKeyField()
    Creator: WorkspaceProfile = ForeignKeyField(
        WorkspaceProfile, to_field="ID")
    Player: Player = ForeignKeyField(Player, to_field="ID")
    TSR: int = IntegerField(default=0)
    DSR: int = IntegerField(default=0)
    HSR: int = IntegerField(default=0)

    @classmethod
    def create(cls, WU, P) -> AnswerForm[Union[None, Custom]]:
        if WU.Workspace.getWorkspaceParams()["CustomSystem"]:
            C = Custom.select().where(Custom.Creator == WU, Custom.Player == P)
        else:
            WUs = WorkspaceProfile.select().where(WorkspaceProfile.Workspace == WU.Workspace)
            if not WUs:
                return AnswerForm(status=False, error="instance_not_exist")
            C = Custom.select().where(Custom.Creator << WUs, Custom.Player == P)
        if not C.exists():
            C = super().create(Creator=WU, Player=P)
            return AnswerForm(status=True, error=None, data=C)
        else:
            return AnswerForm(status=False, error="already_exist")

    @classmethod
    def getInstance(cls, ID: int) -> Union[Custom, None]:
        C = Custom.select().where(Custom.ID == ID)
        if C:
            return C[0]
        else:
            return None

    @classmethod
    def get_byPlayer(cls, Player_ID: int) -> AnswerForm[Union[None, list[Custom]]]:
        P = Player.select().where(Player.ID == Player_ID)
        if P.exists():
            CList = Custom.select().where(Custom.Player == P[0])
            return AnswerForm(status=True, error=None, data=[C for C in CList])
        return AnswerForm(status=False, error="instance_not_exist")

    def changeSR(self, Role: str | int, New_SR: int) -> AnswerForm[None]:
        if Role == "T" or Role == 0:
            self.TSR = New_SR
            self.save()
        elif Role == "D" or Role == 1:
            self.DSR = New_SR
            self.save()
        elif Role == "H" or Role == 2:
            self.HSR = New_SR
            self.save()
        else:
            return AnswerForm(status=False, error="incorrect_role")
        return AnswerForm(status=True, error=None)

    # returning json data with whole information about this custom
    # {
    #     "RolesPriority":
    #         [
    #             {"role": SR, "active": True}, {"role": SR, "active": True}, {"role": SR, "active": False}
    #          ],
    #     "CustomID": ID
    # }
    def getJson(self, WU: WorkspaceProfile) -> dataModels.Custom:
        P = self.Player
        PR: PlayerRoles = PlayerRoles.select().where(
            PlayerRoles.Player == P, PlayerRoles.Creator == WU)
        if not PR.exists():
            PR = PlayerRoles.create(Creator=WU, Player=P)
        else:
            PR = PR[0]

        roles = PR.getJsonRoles()

        for i in range(3):
            if roles[i].role == dataModels.GameRole.tank:
                roles[i].sr = self.TSR
            elif roles[i].role == dataModels.GameRole.damage:
                roles[i].sr = self.DSR
            elif roles[i].role == dataModels.GameRole.heal:
                roles[i].sr = self.HSR
        return dataModels.Custom(ID=self.ID,
                                 Creator=self.Creator.getJson(),
                                 Player=self.Player.getJson(),
                                 isFlex=PR.isFlex,
                                 Roles=roles)


class Perms(DefaultModel):
    ID: int = PrimaryKeyField()
    Name: str = TextField()

    @classmethod
    def create(cls, Name: str) -> AnswerForm[Union[None, Perms]]:
        Perm = Perms.select().where(Perms.Name == Name)
        if not Perm.exists():
            Perm = super().create(Name=Name)
            return AnswerForm(status=True, error=None, data=Perm)
        else:
            return AnswerForm(status=False, error="instance_already_exists")


class RolePerms(DefaultModel):
    ID: int = PrimaryKeyField()
    Role: Roles = ForeignKeyField(Roles, to_field="ID")
    Perm: Perms = ForeignKeyField(Perms, to_field="ID")

    @classmethod
    def create(cls, Role: Roles, Perm: Perms) -> AnswerForm[Union[None, RolePerms]]:
        RP = RolePerms.select().where(RolePerms.Perm == Perm, RolePerms.Role == Role)
        if not RP.exists():
            RP = super().create(Perm=Perm, Role=Role)
            return AnswerForm(status=True, error=None, data=RP)
        else:
            return AnswerForm(status=False, error="instance_already_exist")


class Games(DefaultModel):
    ID: int = PrimaryKeyField()
    Creator: WorkspaceProfile = ForeignKeyField(WorkspaceProfile, to_field="ID")
    Timestamp: dt = DateTimeField(null=True)
    FirstTeamPoints: int = IntegerField(null=True)
    SecondTeamPoints: int = IntegerField(null=True)
    GameStatic: str = TextField()
    GameData: str = TextField()
    Active: bool = BooleanField()

    @classmethod
    def create(cls, WU: WorkspaceProfile, GameData, GameStatic) -> "Games":
        G = super().create(Creator=WU, GameData=GameData, GameStatic=GameStatic, Active=False)
        return G

    def activate(self):
        self.Active = True
        self.save()
        return True

    def deactivate(self):
        self.Active = False
        self.save()
        return True

    def finishGame(self, FirstTeamPoints: int, SecondTeamPoints: int):
        self.Timestamp = dt.now()
        self.FirstTeamPoints = FirstTeamPoints
        self.SecondTeamPoints = SecondTeamPoints
        self.Active = False
        self.save()
        return True
