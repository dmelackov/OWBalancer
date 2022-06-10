from app.DataBase.db import *
from app.Static.globalClasses import AnswerForm


def createProfile(Username, Password):
    if not Profile.select().where(Profile.Username == Username).exists():
        U = Profile.create(Username=Username)
        U.set_password(Password)
        U.save()
        return AnswerForm(status=True, error=None, data=U)
    else:
        return AnswerForm(status=True, error="already_exist")


def checkProfile(Username, Password):
    User = Profile.select().where(Profile.Username == Username)
    if User.exists() and User[0].check_password(Password):
        return AnswerForm(status=True, error=None)
    else:
        return AnswerForm(status=False, error="invalid_login")


def getPlayerRoles(WU, P):
    PR = PlayerRoles.select().where(PlayerRoles.Player == P, PlayerRoles.Creator == WU)
    if PR.exists():
        return AnswerForm(status=True, error=None, data=PR[0])
    else:
        return AnswerForm(status=False, error="instance_not_exist")


def searchPlayer(search_query):
    query = []
    for P in Player.select():
        if search_query.lower() in P.Username.lower():
            query.append(P)
    return query
