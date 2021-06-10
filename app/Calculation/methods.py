from app.DataBase.db import *


def UserPrediction(GameRate, UserRate, WinRate, GamesPlayed):
    if GamesPlayed > 10:
        return (UserRate / GameRate) * WinRate
    else:
        return 0.5


# def TTCount(P, PlayerMass, i):
#     WinWithP = 0
#     LoseWithP = 0
#     G = Games.select().where((Games.T1Tank1 == P & Games.T1Tank2 == PlayerMass[i]) | (Games.T1Tank2 == P & Games.T1Tank1 == PlayerMass[i]))
#     for k in G:
#         if G.Win == 1:
#             WinWithP += 1
#         elif G.Win == 2:
#             LoseWithP += 1
#     G = Games.select().where((Games.T2Tank1 == P & Games.T2Tank2 == PlayerMass[i]) | (Games.T2Tank2 == P & Games.T2Tank1 == PlayerMass[i]))
#     for k in G:
#         if k.Win == 2:
#             WinWithP += 1
#         elif k.Win == 1:
#             LoseWithP += 1
#     return WinWithP, LoseWithP
#
#
# def AvgEP(Player_ID, Role, PlayerMass):
#     P = Player.select().where(Player.ID == Player_ID)
#     if P.exists():
#         P = P[0]
#         if Role == "T":
#             WinWithP = 0
#             LoseWithP = 0
#             for i in range(6):
#                 if 0 <= i <= 1:
#                     WinWithP, LoseWithP = TTCount(P, PlayerMass, i)
#
#         if Role == "D":
#             return P.DWin + P.DLose
#         if Role == "H":
#             return P.HWin + P.HLose


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
