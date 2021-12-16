from app.DataBase.db import *


def createDB():
    db.create_tables([Profile, Custom, Player, Perms, Roles, RolePerms, Games, PlayerRoles])


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


def createPlayer(Profile_ID, Username):
    U = Profile.select().where(Profile.ID == Profile_ID)
    if Username and U.exists():
        P = Player.select().where(Player.Username == Username)
        if not P.exists():
            P = Player.create(Username=Username, Creator=U)
        else:
            P = P[0]
        PR = getPlayerRoles(P, U)
        if not PR:
            PlayerRoles.create(Creator=U, Player=P)
        return P
    return False


def createCustom(U, Player_ID):
    P = Player.select().where(Player.ID == Player_ID)
    if P.exists():
        C = Custom.select().where(Custom.Creator == U, Custom.Player == P)
        if not C.exists():
            C = Custom.create(Creator=U, Player=P[0])
            return C
    return False


def createGame(Profile_ID, GameData):
    U = Profile.select().where(Profile.ID == Profile_ID)
    if U.exists():
        G = Games.create(Creator=U[0], GameData=GameData, Active=False)
        return G
    return False
# -----------------------------------------


# Change custom / roles
# -----------------------------------------
def changeRoles(Profile_ID, Player_ID, NewRoles):
    U = Profile.select().where(Profile.ID == Profile_ID)
    P = Player.select().where(Player.ID == Player_ID)
    PR = getPlayerRoles(P, U)
    if PR is not False:
        PR.Roles = NewRoles
        PR.save()
        return PR
    else:
        return False


def changeFlex(Profile_ID, Player_ID, isFlex):
    U = Profile.select().where(Profile.ID == Profile_ID)
    P = Player.select().where(Player.ID == Player_ID)
    PR = getPlayerRoles(P, U)
    if PR is not False:
        PR.isFlex = isFlex
        PR.save()
        return PR
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
def getPlayerRoles(P, U):
    PR = PlayerRoles.select().where(PlayerRoles.Player == P, PlayerRoles.Creator == U)
    if PR.exists():
        return PR[0]
    else:
        return False


def getCustomID(Profile_ID, Player_ID):
    C = Custom.select().where(Custom.Player == Player_ID, Custom.Creator == Profile_ID)
    if C.exists():
        return C[0].ID
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
    ansm = []
    for P in Player.select():
        if search_query.lower() in P.Username.lower():
            ansm.append(P)
    return ansm


def getProfileID(Profile_Username):
    User = Profile.select().where(Profile.Username == Profile_Username)
    if User.exists():
        return User[0].ID
    else:
        return None


def getRoles(Profile_ID, Player_ID):
    P = Player.select().where(Player.ID == Player_ID)
    U = Profile.select().where(Profile.ID == Profile_ID)
    if P.exists() and U.exists():
        PR = getPlayerRoles(U[0], P[0])
        if PR is not False:
            return [i for i in PR.Roles]
        else:
            PR = PlayerRoles.create(Creator=U, Player=P)
            return []
    else:
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
# print(createProfile("Ivarys", "123"))
# print(getRoles(1, 1))
# createDB()
# print(createPlayer(1, "Ivarys4"))
# print(Profile.select().where(Profile.Username == "Ivarys")[0].getUserSettings())
# ProfileDataConst = {"Amount": {"T": 2, "D": 2, "H": 2},
#                     "TeamNames": {"1": "Team 1", "2": "Team 2"}, "AutoCustom": True,
#                     "ExtendedLobby": False}
# print(Profile.select().where(Profile.Username == "Ivarys")[0].setUserSettings(ProfileDataConst))
