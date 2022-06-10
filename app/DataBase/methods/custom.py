from app.DataBase.db import *
from app.Static.globalClasses import AnswerForm


def createCustom(WU, Player_ID):
    P = Player.select().where(Player.ID == Player_ID)
    if P.exists():
        C = Custom.select().where(Custom.Creator == WU, Custom.Player == P)
        if not C.exists():
            C = Custom.create(Creator=WU, Player=P[0])
            return AnswerForm(status=True, error=None, data=C)
        else:
            return AnswerForm(status=False, error="already_exist")
    else:
        return AnswerForm(status=False, error="player_not_exist")


def changeCustomSR_Tank(Custom_ID, New_SR):
    C = Custom.select().where(Custom.ID == Custom_ID)
    if C.exists():
        C = C[0]
        C.TSR = New_SR
        C.save()
        return AnswerForm(status=True, error=None)
    else:
        return AnswerForm(status=False, error="instance_not_exist")


def changeCustomSR_Dps(Custom_ID, New_SR):
    C = Custom.select().where(Custom.ID == Custom_ID)
    if C.exists():
        C = C[0]
        C.DSR = New_SR
        C.save()
        return AnswerForm(status=True, error=None)
    else:
        return AnswerForm(status=False, error="instance_not_exist")


def changeCustomSR_Heal(Custom_ID, New_SR):
    C = Custom.select().where(Custom.ID == Custom_ID)
    if C.exists():
        C = C[0]
        C.HSR = New_SR
        C.save()
        return AnswerForm(status=True, error=None)
    else:
        return AnswerForm(status=False, error="instance_not_exist")


def getCustom(U, Player_ID):
    C = Custom.select().where(Custom.Player == Player_ID, Custom.Creator == U)
    if C.exists():
        return AnswerForm(status=True, error=None, data=C[0])
    else:
        return AnswerForm(status=False, error="instance_not_exist")


def getCustoms_byPlayer(Player_ID):
    P = Player.select().where(Player.ID == Player_ID)
    if P.exists():
        CList = Custom.select().where(Custom.Player == P[0])
        if CList.exists():
            return AnswerForm(status=True, error=None, data=[C for C in CList])
    return AnswerForm(status=False, error="instance_not_exist")
