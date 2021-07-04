from app.DataBase.db import *
import json


def GetLobby(Profile_ID):
    User = Profile.select().where(Profile.ID == Profile_ID)
    if User.exists():
        CMass = User[0].Customers.split(".")
        if "" in CMass:
            CMass.remove("")
        return [int(i) for i in CMass]


def GetRolesAmount(Profile_ID):
    User = Profile.select().where(Profile.ID == Profile_ID)
    if User.exists():
        CMass = json.loads(User[0].LobbySettings)
        return CMass


def AddToLobby(Profile_ID, Custom_ID):
    User = Profile.select().where(Profile.ID == Profile_ID)
    C = Custom.select().where(Custom.ID == Custom_ID)
    if User.exists() and C.exists():
        User, C = User[0], C[0]

        CMass = User.Customers.split(".")

        if "" in CMass:
            CMass.remove("")

        cacheToChange = -1
        for C_ID in CMass:
            if Custom.get(Custom.ID == C_ID).Player == C.Player:
                cacheToChange = C_ID
        if cacheToChange != -1:
            CMass.remove(cacheToChange)

        if not str(C.ID) in CMass:
            CMass.append(str(C.ID))
        User.Customers = ".".join(CMass)
        User.save()
        return True
    return False


def DeleteFromLobby(Profile_ID, Custom_ID):
    User = Profile.select().where(Profile.ID == Profile_ID)
    C = Custom.select().where(Custom.ID == Custom_ID)
    if User.exists() and C.exists():
        User, C = User[0], C[0]

        CMass = User.Customers.split(".")
        if "" in CMass:
            CMass.remove("")
        if str(C.ID) in CMass:
            CMass.remove(str(C.ID))
        User.Customers = ".".join(CMass)
        User.save()
        return True
    return False


def ClearLobby(Profile_ID):
    User = Profile.select().where(Profile.ID == Profile_ID)
    if User.exists():
        User = User[0]
        User.Customers = ""
        User.save()
        return True
    return False


# print(GetRolesAmount(1))
# print(DeleteFromLobby(1, 16))
# for i in range(1, 13):
#     print(AddToLobby(1, i))
# print(GetLobby(1))
# AddToLobby(1, 16)
