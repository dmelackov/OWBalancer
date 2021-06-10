from app.DataBase.db import *


def createDB():
    db.create_tables([Profile, Games, Custom, Player])


# create things
# -----------------------------------------
def createProfile(Username, Password):
    if not Profile.select().where(Profile.Username == Username).exists():
        User = Profile(Username=Username)
        User.set_password(Password)
        User.save()
        return True
    else:
        return False


def checkProfile(Username, Password):
    User = Profile.select().where(Profile.Username == Username)
    if User.exists() and User[0].check_password(Password):
        return True
    else:
        return False


def createPlayer(BattleTag, Username):  # можно что-то одно (тоже работает)
    if BattleTag or Username:
        if not Player.select().where((Player.BattleTag == BattleTag) | (Player.Username == Username)).exists():
            Player.create(BattleTag=BattleTag, Username=Username)
            return True
    return False


def createCustom(Creator_Username, Player_Username):
    P = Player.select().where(Player.Username == Player_Username)
    User = Profile.select().where(Profile.Username == Creator_Username)
    if P.exists() and User.exists():
        Custom.create(Creator=User[0], Player=P[0])
        return True
    else:
        return False
# -----------------------------------------


# Change custom / roles
# -----------------------------------------
def changeRoles(Custom_ID, NewRoles):
    C = Custom.select().where(Custom.ID == Custom_ID)
    if C.exists():
        C = C[0]
        C.Roles = NewRoles
        C.save()
        return True
    else:
        return False


def changeCustomSR_Tank(Custom_ID, New_SR):
    C = Custom.select().where(Custom.ID == Custom_ID)
    if C.exists():
        C = C[0]
        C.TSR = New_SR
        C.save()
        return True
    else:
        return False


def changeCustomSR_Dps(Custom_ID, New_SR):
    C = Custom.select().where(Custom.ID == Custom_ID)
    if C.exists():
        C = C[0]
        C.DSR = New_SR
        C.save()
        return True
    else:
        return False


def changeCustomSR_Heal(Custom_ID, New_SR):
    C = Custom.select().where(Custom.ID == Custom_ID)
    if C.exists():
        C = C[0]
        C.HSR = New_SR
        C.save()
        return True
    else:
        return False
# -----------------------------------------


# get some things
# -----------------------------------------
def getCustoms_byPlayer(Player_ID):
    P = Player.select().where(Player.ID == Player_ID)
    if P.exists():
        CList = Custom.select().where(Custom.Player == P[0])
        if CList.exists():
            return [C for C in CList]
    return False


def searchPlayer(search_query):
    AllP = Player.select()
    ansm = []
    for P in AllP:
        if search_query.lower() in P.Username.lower() or search_query.lower() in P.BattleTag.lower():
            ansm.append(P)
    return ansm


def getProfileID(Profile_Username):
    User = Profile.select().where(Profile.Username == Profile_Username)
    if User.exists():
        return User[0].ID
    else:
        return None

# print(getCustoms_byPlayer(1))
# print(changeRoles(1, "TD"))
# print(searchPlayer(""))
# print(changeCustomSR_Tank(1, 3200))
# print(changeCustomSR_Heal(1, 3000))
# print(changeCustomSR_Dps(1, 3200))
# print(createCustom("Ivar", "Ivaryss"))
# print(createPlayer("Ivarys#256", "Ivaryss"))
# print(checkProfile("Ivar", "Ivar"))
# print(createProfile("Ivar", "Ivar"))
# createDB()
