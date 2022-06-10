from app.DataBase.db import *


def createPlayer(U, Username):
    if Username:
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


def changeRoles(U, Player_ID, NewRoles):
    P = Player.select().where(Player.ID == Player_ID)
    if P.exists():
        PR = getPlayerRoles(P[0], U)
        if PR is not False:
            PR.Roles = NewRoles
            PR.save()
            return PR
    return False


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


def changeFlex(U, Player_ID, isFlex):
    P = Player.select().where(Player.ID == Player_ID)
    if P.exists():
        PR = getPlayerRoles(P[0], U)
        if PR is not False:
            PR.isFlex = isFlex
            PR.save()
            return PR
    return False



