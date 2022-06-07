from peewee import *
from app.params import DB_NAME, port, password, user, host, db_type
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
import json
from datetime import datetime as dt

if db_type == "mysql":
    db = MySQLDatabase(DB_NAME, host=host, port=port, user=user, password=password)
else:
    db = SqliteDatabase(DB_NAME + ".db")


class DefaultModel(Model):
    class Meta:
        database = db


class Roles(DefaultModel):
    ID = PrimaryKeyField()
    Name = TextField()


defaultProfileData = '{"Amount": {"T": 2, "D": 2, "H": 2}, "TeamNames": {"1": "Team 1", "2": "Team 2"},' \
                   ' "AutoCustom": true, "ExtendedLobby": false, "Autoincrement": false, "BalanceLimit": 2500,' \
                   '"fColor": "#1e90ff", "sColor": "#ff6347", "ExpandedResult": true, "Math":{"alpha": 3.0, ' \
                   '"beta": 1.0, "gamma": 80.0, "p": 2.0, "q": 2.0, "tWeight": 1.1, "dWeight": 1.0, "hWeight": 0.9}}'


class Profile(DefaultModel, UserMixin):
    ID = PrimaryKeyField()
    Username = TextField()
    Password = TextField(null=True)
    LobbySettings = TextField(default=defaultProfileData)

    # login methods
    # -------------------
    def set_password(self, password):
        self.Password = generate_password_hash(password)
        self.save()

    def check_password(self, password):
        return check_password_hash(self.Password, password)

    def getJson(self):
        return {
            'ID': self.ID,
            'username': self.Username
        }

    # -------------------
    # Settings methods
    # -------------------
    def setUserSettings(self, USettings):
        self.LobbySettings = json.dumps(USettings)
        self.save()
    # -------------------


defaultWorkspaceSettings = '{"AutoIncrement": false}'
defaultWorkspaceParams = '{"CustomSystem": true}'


class Workspace(DefaultModel):
    ID = PrimaryKeyField()
    Name = TextField(unique=True)
    Description = TextField(default="")
    Creator = ForeignKeyField(Profile, to_field="ID")
    WorkspaceParams = TextField(default=defaultWorkspaceParams)
    WorkspaceSettings = TextField(default=defaultWorkspaceSettings)

    # Settings methods
    # -------------------
    def setWorkspaceSettings(self, WSettings):
        self.WorkspaceSettings = json.dumps(WSettings)
        self.save()

    def setWorkspaceDescription(self, Desc):
        self.Description = Desc
        self.save()
    # -------------------0


class KeyData(DefaultModel):
    ID = PrimaryKeyField()
    Key = TextField()
    Workspace = ForeignKeyField(Workspace, to_field="ID")
    UseLimit = IntegerField(default=1)
    Creator = ForeignKeyField(Profile, to_field="ID")


defaultLobbyData = '{"Lobby": []}'


class WorkspaceProfile(DefaultModel):
    ID = PrimaryKeyField()
    Profile = ForeignKeyField(Profile, to_field="ID")
    Customers = TextField(default=defaultLobbyData)
    Role = ForeignKeyField(Roles, to_field="ID", null=True)
    Workspace = ForeignKeyField(Workspace, to_field="ID")

    # Lobby methods
    # -------------------
    def getUserSettings(self):
        return json.loads(self.LobbySettings)

    def getLobbyInfo(self):
        LobbyData = json.loads(self.Customers)
        return LobbyData["Lobby"]

    def updateLobbyInfo(self, mass):
        d = {"Lobby": mass}
        self.Customers = json.dumps(d)
        self.save()


class Player(DefaultModel):
    ID = PrimaryKeyField()
    Username = TextField(null=True)
    Creator = ForeignKeyField(WorkspaceProfile, to_field="ID")

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

    def getJson(self):
        return {"ID": self.ID,
                "Creator": self.Creator.getJson(),
                "Username": self.Username}


class PlayerRoles(DefaultModel):
    ID = PrimaryKeyField()
    Creator = ForeignKeyField(WorkspaceProfile, to_field="ID")
    Player = ForeignKeyField(Player, to_field="ID")
    Roles = TextField(default="")
    isFlex = BooleanField(default=False)

    def getJsonRoles(self):
        if self.isFlex:
            return [{"role": i, "active": True} for i in "TDH"]
        else:
            priority = [{"role": i, "active": True} for i in self.Roles] + \
                       [{"role": i, "active": False} for i in "TDH" if i not in self.Roles]
        return priority


class Custom(DefaultModel):
    ID = PrimaryKeyField()
    Creator = ForeignKeyField(WorkspaceProfile, to_field="ID")
    Player = ForeignKeyField(Player, to_field="ID")
    TSR = IntegerField(default=0)
    DSR = IntegerField(default=0)
    HSR = IntegerField(default=0)

    # returning json data with whole information about this custom
    # {
    #     "RolesPriority":
    #         [
    #             {"role": SR, "active": True}, {"role": SR, "active": True}, {"role": SR, "active": False}
    #          ],
    #     "CustomID": ID
    # }
    def getJson(self, U):
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


class RolePerms(DefaultModel):
    ID = PrimaryKeyField()
    Role = ForeignKeyField(Roles, to_field="ID")
    Perm = ForeignKeyField(Perms, to_field="ID")


class Games(DefaultModel):
    ID = PrimaryKeyField()
    Creator = ForeignKeyField(Profile, to_field="ID")
    Timestamp = DateTimeField(null=True)
    Winner = IntegerField(null=True)
    GameStatic = TextField()
    GameData = TextField()
    Active = BooleanField()

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

