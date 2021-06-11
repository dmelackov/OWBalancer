from app.DataBase.db import *


def GetLobby(Profile_ID):
    User = Profile.select().where(Profile.ID == Profile_ID)
    if User.exists():
        CMass = User[0].Customers.split(".")
        if "" in CMass:
            CMass.remove("")
        return CMass


def AddToLobby(Profile_ID, Custom_ID):
    User = Profile.select().where(Profile.ID == Profile_ID)
    C = Custom.select().where(Custom.ID == Custom_ID)
    if User.exists() and C.exists():
        User, C = User[0], C[0]

        CMass = User.Customers.split(".")
        if "" in CMass:
            CMass.remove("")
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


# for i in range(1, 13):
#     AddToLobby(1, i)
