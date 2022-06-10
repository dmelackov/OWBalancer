from app.DataBase.db import *


def createDB():
    db.create_tables([Profile, Custom, Player, Perms, Roles, RolePerms, Games, PlayerRoles])


def createGame(Profile_ID, GameData):
    U = Profile.select().where(Profile.ID == Profile_ID)
    if U.exists():
        G = Games.create(Creator=U[0], GameData=GameData, Active=False)
        return G
    return False


# def getGames(Profile_ID):
#     U = Profile.select().where(Pro)
# -----------------------------------------

# print(getCustoms_byPlayer(1))
# print(changeRoles(2, "TH"))
# print()
# print(changeCustomSR_Tank(1, 3200))
# print(changeCustomSR_Heal(1, 3000))
# print(changeCustomSR_Dps(1, 3200))
# print(createCustom(1, i))
# print(checkProfile("Ivar", "Ivar"))
# print(createProfile("Ivarysss", "123"))
# print(getRoles(1, 1))
# createDB()
# print(createPlayer(1, "Ivarys4"))
# print(Custom.get(Custom.ID == 1).getJson(Profile.select().where(Profile.Username == "Ivarys")[0]))
# print(Profile.select().where(Profile.Username == "Ivarys")[0].getUserSettings())
# ProfileDataConst = {"Amount": {"T": 2, "D": 2, "H": 2},
#                     "TeamNames": {"1": "Team 1", "2": "Team 2"}, "AutoCustom": True,
#                     "ExtendedLobby": False}
# print(Profile.select().where(Profile.Username == "Ivarys")[0].setUserSettings(ProfileDataConst))
