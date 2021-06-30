from peewee import *
from app.params import DB_NAME
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

db = SqliteDatabase(DB_NAME)


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

    class Meta:
        database = db


class Player(Model):
    ID = PrimaryKeyField()
    BattleTag = TextField(null=True)
    Username = TextField(null=True)
    Roles = TextField(null=True, default="")
    PlayedGamesData = TextField(default='')
    TWin = IntegerField(default=0)
    DWin = IntegerField(default=0)
    HWin = IntegerField(default=0)
    TLose = IntegerField(default=0)
    DLose = IntegerField(default=0)
    HLose = IntegerField(default=0)

    def getJsonInfo(self):
        return {"id": self.ID,
                "Username": self.Username,
                "BattleTag": self.BattleTag}
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
        data['CustomID'] = self.ID
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
