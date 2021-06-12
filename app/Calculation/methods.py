from app.DataBase.db import *


def UserPrediction(GameRate, UserRate, WinRate, GamesPlayed):
    if GamesPlayed > 10:
        return (UserRate / GameRate) * ((WinRate + AVGEP) / 2)  # + AVGEP
    else:
        return 0.5


def GamesPlayedCounter(Player_ID, Role):
    P = Player.select().where(Player.ID == Player_ID)
    if P.exists():
        P = P[0]
        if Role == "T":
            return P.TWin + P.TLose
        if Role == "D":
            return P.DWin + P.DLose
        if Role == "H":
            return P.HWin + P.HLose
    return 0


def WinRateCounter(Player_ID, Role):
    P = Player.select().where(Player.ID == Player_ID)
    if P.exists():
        P = P[0]
        if Role == "T" and P.TWin + P.TLose > 0:
            return P.TWin / (P.TWin + P.TLose)
        if Role == "D" and P.DWin + P.DLose > 0:
            return P.DWin / (P.DWin + P.DLose)
        if Role == "H" and P.HWin + P.HLose > 0:
            return P.HWin / (P.HWin + P.HLose)
    return 0.5
