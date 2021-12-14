from peewee import *
from app.params import DB_NAME, port, password, user, host
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
import json

# db = MySQLDatabase(DB_NAME, host=host, port=port, user=user, password=password)
db = SqliteDatabase(DB_NAME + ".db")
ProfileDataConst = '{"Amount": {"T": 2, "D": 2, "H": 2}, "TeamNames": {"1": "Team 1", "2": "Team 2"},' \
                   ' "AutoCustom": true, "ExtendedLobby": false, "Autoincrement": false, "BalanceLimit": 1000,' \
                   ' "Network": true}'
LobbyDataConst = '{"Lobby": []}'


class DefaultModel(Model):
    class Meta:
        database = db


class Roles(DefaultModel):
    ID = PrimaryKeyField()
    Name = TextField()


class Profile(DefaultModel, UserMixin):
    ID = PrimaryKeyField()
    Username = TextField()
    Password = TextField(null=True)
    Customers = TextField(default=LobbyDataConst)
    LobbySettings = TextField(default=ProfileDataConst)
    Role = ForeignKeyField(Roles, to_field="ID", null=True)

    # login methods
    # -------------------
    def set_password(self, password):
        self.Password = generate_password_hash(password)
        self.save()

    def check_password(self, password):
        return check_password_hash(self.Password, password)

    def getJsonInfo(self):
        return {
            'id': self.ID,
            'username': self.Username
        }

    # -------------------
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

    # -------------------
    # Settings methods
    # -------------------
    def setUserSettings(self, USettings):
        self.LobbySettings = json.dumps(USettings)
        self.save()

    def settingsChangeTanks(self, TanksCount):
        USettings = json.loads(self.LobbySettings)
        USettings["Amount"]["T"] = TanksCount
        self.LobbySettings = json.dumps(USettings)
        self.save()

    def settingsChangeDps(self, DpsCount):
        USettings = json.loads(self.LobbySettings)
        USettings["Amount"]["D"] = DpsCount
        self.LobbySettings = json.dumps(USettings)
        self.save()

    def settingsChangeHeal(self, HealCount):
        USettings = json.loads(self.LobbySettings)
        USettings["Amount"]["H"] = HealCount
        self.LobbySettings = json.dumps(USettings)
        self.save()

    def settingsTeamOne(self, TeamName):
        USettings = json.loads(self.LobbySettings)
        USettings["TeamNames"]["1"] = TeamName
        self.LobbySettings = json.dumps(USettings)
        self.save()

    def settingsTeamTwo(self, TeamName):
        USettings = json.loads(self.LobbySettings)
        USettings["TeamNames"]["2"] = TeamName
        self.LobbySettings = json.dumps(USettings)
        self.save()

    def settingsAutoCustom(self, AutoCustom):
        USettings = json.loads(self.LobbySettings)
        USettings["AutoCustom"] = AutoCustom
        self.LobbySettings = json.dumps(USettings)
        self.save()

    def settingsExtendedLobby(self, ExtendedLobby):
        USettings = json.loads(self.LobbySettings)
        USettings["ExtendedLobby"] = ExtendedLobby
        self.LobbySettings = json.dumps(USettings)
        self.save()
    # -------------------


class Player(DefaultModel):
    ID = PrimaryKeyField()
    Username = TextField(null=True)
    Creator = ForeignKeyField(Profile, to_field="ID")


class PlayerRoles(DefaultModel):
    ID = PrimaryKeyField()
    Creator = ForeignKeyField(Profile, to_field="ID")
    Player = ForeignKeyField(Player, to_field="ID")
    Roles = TextField(default="")
    isFlex = BooleanField(default=False)

    def getJsonInfo(self):
        priority = list(map(lambda x: {"role": x, "active": True}, list(self.Roles)))
        if "T" not in self.Roles:
            priority.append({"role": "T", "active": False})
        if "D" not in self.Roles:
            priority.append({"role": "D", "active": False})
        if "H" not in self.Roles:
            priority.append({"role": "H", "active": False})
        if self.isFlex:
            for i in priority:
                i["active"] = True

        return {
            "id": self.ID,
            "Username": self.Username,
            "Creator": self.Creator.getJsonInfo(),
            "Roles": {"Tank": ("T" in self.Roles or self.isFlex),
                      "Damage": ("D" in self.Roles or self.isFlex),
                      "Heal": ("H" in self.Roles or self.isFlex)},
            "RolesPriority": priority,
            "isFlex": self.isFlex
            }


class Custom(DefaultModel):
    ID = PrimaryKeyField()
    Creator = ForeignKeyField(Profile, to_field="ID")
    Player = ForeignKeyField(Player, to_field="ID")
    TSR = IntegerField(default=0)
    DSR = IntegerField(default=0)
    HSR = IntegerField(default=0)

    def getJsonInfo(self):
        data = self.Player.getJsonInfo()
        for i in range(3):
            if data["RolesPriority"][i]["role"] == "T":
                data["RolesPriority"][i]["sr"] = self.TSR
            elif data["RolesPriority"][i]["role"] == "D":
                data["RolesPriority"][i]["sr"] = self.DSR
            elif data["RolesPriority"][i]["role"] == "H":
                data["RolesPriority"][i]["sr"] = self.HSR
        data['CustomID'] = self.ID
        data['SR'] = {"Tank": self.TSR,
                      "Damage": self.DSR,
                      "Heal": self.HSR}
        data['Author'] = self.Creator.getJsonInfo()
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
    Timestamp = DateTimeField()
    Winner = IntegerField(null=True)
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
        self.Winner = winner
        self.Active = False
        self.save()
        return True
