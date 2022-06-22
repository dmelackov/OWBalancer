from peewee import *
from app.params import DB_NAME, port, password, user, host, db_type
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
import json
from datetime import datetime as dt
from app.Static.globalClasses import AnswerForm
import secrets


defaultWorkspaceParams = '{"CustomSystem": true}'
defaultLobbyData = '{"Lobby": []}'
defaultWorkspaceSettings = '{"AutoIncrement": false, "generalLobby": false}'


if db_type == "mysql":
    db = MySQLDatabase(DB_NAME, host=host, port=port, user=user, password=password)
else:
    db = SqliteDatabase(DB_NAME + ".db")


class DefaultModel(Model):
    class Meta:
        database = db


class Roles(DefaultModel):
    ID = PrimaryKeyField()
    Name = TextField(unique=True)

    @classmethod
    def create(cls, Name: str) -> AnswerForm:
        R = Roles.select().where(Roles.Name == Name)
        if not R.exists():
            R = super().create(Name=Name)
            return AnswerForm(status=True, error=None, data=R)
        else:
            return AnswerForm(status=False, error="instance_already_exist")

    @classmethod
    def getRole(cls, Name):
        R = Roles.select().where(Roles.Name == Name)
        if R:
            return AnswerForm(status=True, error=None, data=R[0])
        else:
            return AnswerForm(status=False, error="instance_not_exist")


defaultProfileData = '{"Amount": {"T": 2, "D": 2, "H": 2}, "TeamNames": {"1": "Team 1", "2": "Team 2"},' \
                   ' "AutoCustom": true, "ExtendedLobby": false, "Autoincrement": false, "BalanceLimit": 2500,' \
                   '"fColor": "#1e90ff", "sColor": "#ff6347", "ExpandedResult": true, "Math":{"alpha": 3.0, ' \
                   '"beta": 1.0, "gamma": 80.0, "p": 2.0, "q": 2.0, "tWeight": 1.1, "dWeight": 1.0, "hWeight": 0.9}}'


class Profile(DefaultModel, UserMixin):
    ID = PrimaryKeyField()
    Username = TextField()
    Password = TextField(null=True)
    LobbySettings = TextField(default=defaultProfileData)

    @classmethod
    def create(cls, Username: str, Password: str) -> AnswerForm:
        if not Profile.select().where(Profile.Username == Username).exists():
            U = super().create(Username=Username)
            U.set_password(Password)
            U.save()
            return AnswerForm(status=True, error=None, data=U)
        else:
            return AnswerForm(status=True, error="already_exist")

    @classmethod
    def getInstance(cls, ID: int):
        U = Profile.select().where(Profile.ID == ID)
        if U:
            return U[0]
        else:
            return None

    @classmethod
    def getProfile(cls, Username: str):
        U = Profile.select().where(fn.lower(Profile.Username) == Username.lower())
        if U:
            return U[0]
        else:
            return None

    @classmethod
    def check(cls, Username: str, Password: str) -> AnswerForm:
        U = Profile.select().where(Profile.Username == Username)
        if U and U[0].check_password(Password):
            return AnswerForm(status=True, error=None, data=U[0])
        else:
            return AnswerForm(status=False, error="invalid_login")

    @classmethod
    def search(cls, search_query: str) -> list:
        query = []
        for P in Player.select():
            if search_query.lower() in P.Username.lower():
                query.append(P)
        return query

    def set_password(self, Password: str) -> None:
        self.Password = generate_password_hash(Password)
        self.save()

    def check_password(self, Password: str) -> bool:
        return check_password_hash(self.Password, Password)

    def getJson(self) -> dict:
        return {
            'ID': self.ID,
            'username': self.Username
        }

    def getCustom(self, Player_ID: int) -> AnswerForm:
        C = Custom.select().where(Custom.Player == Player_ID, Custom.Creator == self)
        if C.exists():
            return AnswerForm(status=True, error=None, data=C[0])
        else:
            return AnswerForm(status=False, error="instance_not_exist")

    def setUserSettings(self, USettings: dict) -> None:
        self.LobbySettings = json.dumps(USettings)
        self.save()

    def getWorkspaceList(self):
        WUs = WorkspaceProfile.select().where(WorkspaceProfile.Profile == self)
        return AnswerForm(status=True, error=None, data=[WU.Workspace for WU in WUs])


class Workspace(DefaultModel):
    ID = PrimaryKeyField()
    Name = TextField()
    Description = TextField(default="")
    Creator = ForeignKeyField(Profile, to_field="ID")
    WorkspaceParams = TextField(default=defaultWorkspaceParams)
    Lobby = TextField(default=defaultLobbyData)

    @classmethod
    def create(cls, U: Profile, Name: str, WorkspaceParams: str) -> AnswerForm:
        W = super().create(Creator=U, Name=Name, WorkspaceParams=WorkspaceParams)
        return AnswerForm(status=True, error=None, data=W)

    @classmethod
    def getInstance(cls, ID: int):
        W = Workspace.select().where(Workspace.ID == ID)
        if W:
            return W[0]
        else:
            return None

    def getJson(self) -> dict:
        return {
            "ID": self.ID,
            "Name": self.Name,
            "Description": self.Description,
            "Creator": self.Creator.getJson()
        }

    def setWorkspaceDescription(self, Desc: str) -> None:
        self.Description = Desc
        self.save()

    def joinWorkspace(self, U: Profile, InviteKey: str) -> AnswerForm:
        KD = KeyData.select().where(KeyData.Key == InviteKey, KeyData.Workspace == self)
        if not KD:
            return AnswerForm(status=False, error="invalid_key")

        WU = WorkspaceProfile.select().where(WorkspaceProfile.Profile == U and WorkspaceProfile.Workspace == self)
        if WU:
            if not WU[0].Active:
                WU[0].Active = 1
                WU[0].save()
                return AnswerForm(status=True, error=None, data=WU[0])
            else:
                return AnswerForm(status=False, error="already_in")

        KD = KD[0]
        if KD.UseLimit > 0:
            KD.UseLimit -= 1
        elif KD.UseLimit == 0:
            return AnswerForm(status=False, error="use_limit")

        WU = WorkspaceProfile.create(U, self)
        return AnswerForm(status=True, error=None, data=WU)

    def getWorkspaceProfile(self, U: Profile) -> AnswerForm:
        WU = WorkspaceProfile.select().where(WorkspaceProfile.Profile == U, WorkspaceProfile.Workspace == self)
        if WU:
            return AnswerForm(status=True, error=None, data=WU[0])
        else:
            return AnswerForm(status=False, error="instance_not_exist")


class KeyData(DefaultModel):
    ID = PrimaryKeyField()
    Key = TextField()
    Workspace = ForeignKeyField(Workspace, to_field="ID")
    UseLimit = IntegerField(default=1)
    Creator = ForeignKeyField(Profile, to_field="ID")

    @classmethod
    def create(cls, U, W, UseLimit=1) -> AnswerForm:
        Key = W.ID + secrets.token_urlsafe(8)
        while KeyData.select().where(KeyData.Key == Key):
            Key = W.ID + secrets.token_urlsafe(8)
        KD = super().create(Key=Key, Workspace=W, Creator=U, UseLimit=UseLimit)
        return AnswerForm(status=True, error=None, data=KD)

    @classmethod
    def getByKey(cls, Key: str) -> AnswerForm:
        KD = KeyData.select().where(KeyData.Key == Key)
        if KD:
            return AnswerForm(status=True, error=None, data=KD[0])
        else:
            return AnswerForm(status=False, error="instance_not_exist")


class WorkspaceProfile(DefaultModel):
    ID = PrimaryKeyField()
    Profile = ForeignKeyField(Profile, to_field="ID")
    Customers = TextField(default=defaultLobbyData)
    Role = ForeignKeyField(Roles, to_field="ID", null=True)
    Workspace = ForeignKeyField(Workspace, to_field="ID")
    WorkspaceSettings = TextField(default=defaultWorkspaceSettings)
    Active = BooleanField(default=True)

    @classmethod
    def getInstance(cls, ID: int):
        WU = WorkspaceProfile.select().where(WorkspaceProfile.ID == ID)
        if WU:
            return WU[0]
        else:
            return None

    @classmethod
    def create(cls, U, W) -> AnswerForm:
        WU = WorkspaceProfile.select().where(WorkspaceProfile.Profile == U, WorkspaceProfile.Workspace == W)
        if WU and not WU[0].Active:
            WU[0].Active = True
            WU[0].save()
            return AnswerForm(status=True, error=None, data=WU[0])
        else:
            WU = super().create(Profile=U, Workspace=W)
            return AnswerForm(status=True, error=None, data=WU)

    @classmethod
    def getWU(cls, U, W) -> AnswerForm:
        WU = WorkspaceProfile.select().where(WorkspaceProfile.Profile == U, WorkspaceProfile.Workspace == W)
        if WU:
            return AnswerForm(status=True, error=None, data=WU[0])
        else:
            return AnswerForm(status=False, error="instance_not_exist")

    def getPermissions(self) -> AnswerForm:
        if self.Role is not None:
            RPs = RolePerms.select().where(RolePerms.Role == self.Role)
            mass = []
            for RP in RPs:
                mass.append(RP.Perm)
            return AnswerForm(status=True, error=None, data=mass)
        else:
            return AnswerForm(status=False, error="empty_role")

    def checkPermission(self, Perm: str) -> AnswerForm:
        PRs = self.getPermissions().data
        if PRs:
            if Perm in [i.Name for i in PRs]:
                return AnswerForm(status=True, error=None)
        return AnswerForm(status=False, error=None)

    def getUserSettings(self) -> dict:
        return json.loads(self.LobbySettings)

    def getLobbyInfo(self) -> list:
        LobbyData = json.loads(self.Customers)
        return LobbyData["Lobby"]

    def updateLobbyInfo(self, mass: list) -> None:
        d = {"Lobby": mass}
        self.Customers = json.dumps(d)
        self.save()

    def setRole(self, Role: Roles) -> AnswerForm:
        if self.Role != Role:
            self.Role = Role
            self.save()
            return AnswerForm(status=True, error=None)
        else:
            return AnswerForm(status=False, error="role_already_given")


class Player(DefaultModel):
    ID = PrimaryKeyField()
    Username = TextField(null=True)
    Creator = ForeignKeyField(WorkspaceProfile, to_field="ID")

    @classmethod
    def create(cls, WU: WorkspaceProfile, Username: str) -> AnswerForm:
        if Username:
            P = Player.select().where(Player.Username == Username)
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
    def getInstance(cls, ID: int):
        P = Player.select().where(Player.ID == ID)
        if P:
            return P[0]
        else:
            return None

    # return {
    #             "id": self.ID,
    #             "Username": self.Username,
    #             "Creator": self.Creator.getJsonInfo(),
    #             "Roles": {"Tank": ("T" in self.Roles or self.isFlex),
    #                       "Damage": ("D" in self.Roles or self.isFlex),
    #                       "Heal": ("H" in self.Roles or self.isFlex)},
    #             "RolesPriority": priority,
    #             "isFlex": self.isFlex
    #         }
    def getJson(self) -> dict:
        return {"ID": self.ID,
                "Creator": self.Creator.getJson(),
                "Username": self.Username}


class PlayerRoles(DefaultModel):
    ID = PrimaryKeyField()
    Creator = ForeignKeyField(WorkspaceProfile, to_field="ID")
    Player = ForeignKeyField(Player, to_field="ID")
    Roles = TextField(default="")
    isFlex = BooleanField(default=False)

    @classmethod
    def getInstance(cls, ID: int):
        PR = PlayerRoles.select().where(PlayerRoles.ID == ID)
        if PR:
            return PR[0]
        else:
            return None

    @classmethod
    def getPR(cls, WU: WorkspaceProfile, P: Player) -> AnswerForm:
        PR = PlayerRoles.select().where(PlayerRoles.Player == P, PlayerRoles.Creator == WU)
        if PR.exists():
            return AnswerForm(status=True, error=None, data=PR[0])
        else:
            return AnswerForm(status=False, error="instance_not_exist")

    def getJsonRoles(self) -> list:
        if self.isFlex:
            return [{"role": i, "active": True} for i in "TDH"]
        else:
            priority = [{"role": i, "active": True} for i in self.Roles] + \
                       [{"role": i, "active": False} for i in "TDH" if i not in self.Roles]
        return priority

    def setRoles(self, newRoles: str) -> AnswerForm:
        if all(i in "TDH" for i in newRoles):
            self.Roles = newRoles
            self.save()
            return AnswerForm(status=True, error=None)
        else:
            return AnswerForm(status=False, error="role_presentation_error")

    def setFlex(self, Flex: bool) -> AnswerForm:
        self.isFlex = bool(Flex)
        self.save()
        return AnswerForm(status=True, error=None)


class Custom(DefaultModel):
    ID = PrimaryKeyField()
    Creator = ForeignKeyField(WorkspaceProfile, to_field="ID")
    Player = ForeignKeyField(Player, to_field="ID")
    TSR = IntegerField(default=0)
    DSR = IntegerField(default=0)
    HSR = IntegerField(default=0)

    @classmethod
    def create(cls, WU, P) -> AnswerForm:
        C = Custom.select().where(Custom.Creator == WU, Custom.Player == P)
        if not C.exists():
            C = super().create(Creator=WU, Player=P[0])
            return AnswerForm(status=True, error=None, data=C)
        else:
            return AnswerForm(status=False, error="already_exist")

    @classmethod
    def getInstance(cls, ID: int):
        C = Custom.select().where(Custom.ID == ID)
        if C:
            return C[0]
        else:
            return None

    @classmethod
    def get_byPlayer(cls, Player_ID: int) -> AnswerForm:
        P = Player.select().where(Player.ID == Player_ID)
        if P.exists():
            CList = Custom.select().where(Custom.Player == P[0])
            if CList.exists():
                return AnswerForm(status=True, error=None, data=[C for C in CList])
        return AnswerForm(status=False, error="instance_not_exist")

    def changeSR(self, Role: str, New_SR: int) -> AnswerForm:
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
    def getJson(self, U: Profile) -> dict:
        P = self.Player
        PR = PlayerRoles.select().where(PlayerRoles.Player == P, PlayerRoles.Creator == U)
        if not PR.exists():
            PR = PlayerRoles.create(Creator=U, Player=P)
        else:
            PR = PR[0]
        data = {
            "Player": P.getJson(),
            "Roles": PR.getJsonRoles(),
            "isFlex": PR.isFlex,
            "ID": self.ID,
            "Creator": self.Creator.getJson()}

        for i in range(3):
            if data["Roles"][i]["role"] == "T":
                data["Roles"][i]["sr"] = self.TSR
            elif data["Roles"][i]["role"] == "D":
                data["Roles"][i]["sr"] = self.DSR
            elif data["Roles"][i]["role"] == "H":
                data["Roles"][i]["sr"] = self.HSR
        return data


class Perms(DefaultModel):
    ID = PrimaryKeyField()
    Name = TextField()

    @classmethod
    def create(cls, Name: str) -> AnswerForm:
        Perm = Perms.select().where(Perms.Name == Name)
        if not Perm.exists():
            Perm = super().create(Name=Name)
            return AnswerForm(status=True, error=None, data=Perm)
        else:
            return AnswerForm(status=False, error="instance_already_exists")


class RolePerms(DefaultModel):
    ID = PrimaryKeyField()
    Role = ForeignKeyField(Roles, to_field="ID")
    Perm = ForeignKeyField(Perms, to_field="ID")

    @classmethod
    def create(cls, Role: Roles, Perm: Perms) -> AnswerForm:
        RP = RolePerms.select().where(RolePerms.Perm == Perm, RolePerms.Role == Role)
        if not RP.exists():
            RP = super().create(Perm=Perm, Role=Role)
            return AnswerForm(status=True, error=None, data=RP)
        else:
            return AnswerForm(status=False, error="instance_already_exist")


class Games(DefaultModel):
    ID = PrimaryKeyField()
    Creator = ForeignKeyField(Profile, to_field="ID")
    Timestamp = DateTimeField(null=True)
    Winner = IntegerField(null=True)
    GameStatic = TextField()
    GameData = TextField()
    Active = BooleanField()

    @classmethod
    def create(cls, Profile_ID, GameData):
        U = Profile.select().where(Profile.ID == Profile_ID)
        if U.exists():
            G = super().create(Creator=U[0], GameData=GameData, Active=False)
            return G
        return False

    def activate(self):
        self.Active = True
        self.save()
        return True

    def deactivate(self):
        self.Active = False
        self.save()
        return True

    def finishGame(self, winner):
        self.Timestamp = dt.now()
        self.Winner = winner
        self.Active = False
        self.save()
        return True

