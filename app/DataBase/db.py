from peewee import *
from app.params import DB_NAME
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

db = MySQLDatabase(DB_NAME, host="blackserver.sytes.net", port=3306, user="Ivarys", password="c44vwi")


class Profile(Model, UserMixin):
    ID = PrimaryKeyField()
    Username = TextField()
    Password = TextField(null=True)
    Customers = TextField(default="")
    LobbySettings = TextField(default='{"Amount": {"T": 2, "D": 2, "H": 2}}')

    def set_password(self, password):
        self.Password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.Password, password)

    def getJsonInfo(self):
        return {
            'id': self.ID,
            'username': self.Username
        }

    class Meta:
        database = db


class Player(Model):
    ID = PrimaryKeyField()
    BattleTag = TextField(null=True)
    Username = TextField(null=True)
    Roles = TextField(null=True, default="")
    isFlex = BooleanField(default=False)
    PlayedGamesData = TextField(
        default='{"Win": {"T": {}, "D": {}, "H": {}}, "Lose": {"T": {}, "D": {}, "H": {}}}')
    TWin = IntegerField(default=0)
    DWin = IntegerField(default=0)
    HWin = IntegerField(default=0)
    TLose = IntegerField(default=0)
    DLose = IntegerField(default=0)
    HLose = IntegerField(default=0)

    def getJsonInfo(self):
        priority = list(map(lambda x: {"role": x, "active": True}, list(self.Roles)))
        if "T" not in self.Roles:
            priority.append({"role": "T", "active": False})
        if "D" not in self.Roles:
            priority.append({"role": "D", "active": False})
        if "H" not in self.Roles:
            priority.append({"role": "H", "active": False})
        return {"id": self.ID,
                "Username": self.Username,
                "BattleTag": self.BattleTag,
                "Roles": {"Tank": ("T" in self.Roles),
                          "Damage": ("D" in self.Roles),
                          "Heal": ("H" in self.Roles)},
                "RolesPriority": priority
                }

    class Meta:
        database = db


class Custom(Model):
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

    class Meta:
        database = db


class Games(Model):
    ID = PrimaryKeyField()
    Creator = ForeignKeyField(Profile, to_field="ID")
    T1Tank1 = ForeignKeyField(Player, to_field="ID")
    T1Tank2 = ForeignKeyField(Player, to_field="ID")
    T1Dps1 = ForeignKeyField(Player, to_field="ID")
    T1Dps2 = ForeignKeyField(Player, to_field="ID")
    T1Heal1 = ForeignKeyField(Player, to_field="ID")
    T1Heal2 = ForeignKeyField(Player, to_field="ID")
    T2Tank1 = ForeignKeyField(Player, to_field="ID")
    T2Tank2 = ForeignKeyField(Player, to_field="ID")
    T2Dps1 = ForeignKeyField(Player, to_field="ID")
    T2Dps2 = ForeignKeyField(Player, to_field="ID")
    T2Heal1 = ForeignKeyField(Player, to_field="ID")
    T2Heal2 = ForeignKeyField(Player, to_field="ID")
    Win = IntegerField()

    class Meta:
        database = db
