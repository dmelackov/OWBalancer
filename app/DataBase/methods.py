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
        if not Player.select().where(((Player.BattleTag == BattleTag) & (BattleTag != "")) | (Player.Username == Username)).exists():
            Player.create(BattleTag=BattleTag, Username=Username)
            return True
    return False


def createCustom(Creator_Username, Player_Username):
    P = Player.select().where(Player.Username == Player_Username)
    User = Profile.select().where(Profile.Username == Creator_Username)
    if P.exists() and User.exists():
        C = Custom.select().where(Custom.Creator == User, Custom.Player == P)
        if not C.exists():
            Custom.create(Creator=User[0], Player=P[0])
            return True
    return False
# -----------------------------------------


# Change custom / roles
# -----------------------------------------
def changeRoles(Player_ID, NewRoles):
    P = Player.select().where(Player.ID == Player_ID)
    if P.exists():
        P = P[0]
        P.Roles = NewRoles
        P.save()
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


# get SR
# -----------------------------------------
def getCustomSR(Custom_ID):
    C = Custom.select().where(Custom.ID == Custom_ID)
    if C.exists():
        C = C[0]
        return [C.TSR, C.DSR, C.HSR]
    return False
# -----------------------------------------


# get some things
# -----------------------------------------
def getCustomID(Profile_ID, Player_ID):
    C = Custom.select().where(Custom.Player.ID == Player_ID, Custom.Creator.ID == Profile_ID)
    if C.exists():
        return C.ID
    else:
        return False


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


def getRoles(Player_ID):
    P = Player.select().where(Player.ID == Player_ID)
    if P.exists():
        P = P[0]
        return [i for i in P.Roles]
    else:
        return []


# print(getCustoms_byPlayer(1))
# print(changeRoles(2, "TH"))
# print()
# print(changeCustomSR_Tank(1, 3200))
# print(changeCustomSR_Heal(1, 3000))
# print(changeCustomSR_Dps(1, 3200))
# print(createCustom("Ivar", "Ivarys"))
# print(createPlayer("Ivarys#2564", "Ivarys"))
# print(checkProfile("Ivar", "Ivar"))
# print(createProfile("Ivarys", "123"))
# print(getRoles(1))
# createDB()

# name = "Artmagic"
# print(createPlayer("", name))
# print(createCustom("Ivarys", name))
# print(changeCustomSR_Tank(searchPlayer(name)[0].ID, 2900))
# print(changeCustomSR_Dps(searchPlayer(name)[0].ID, 3100))
# print(changeCustomSR_Heal(searchPlayer(name)[0].ID, 2600))
# print(changeRoles(searchPlayer(name)[0].ID, "TD"))
