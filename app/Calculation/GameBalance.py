from app.DataBase.db import *
from app.DataBase.LobbyСollector import GetLobby
import itertools
import copy


def preGenerate():
    teamMask = [0 for i in range(12)]
    teamMaskfilled = []
    for i in range(2 ** 12 - 1):
        teamMask[0] += 1
        for j in range(11):
            if teamMask[j] > 1:
                teamMask[j + 1] += 1
                teamMask[j] -= 2
        if teamMask.count(0) == teamMask.count(1) == 6:
            teamMaskfilled.append(teamMask.copy())

    roleMask = [0 for i in range(6)]
    roleMaskFilled = []
    for i in range(728):
        roleMask[0] += 1
        for j in range(5):
            if roleMask[j] > 2:
                roleMask[j + 1] += 1
                roleMask[j] -= 3
        if roleMask.count(0) == roleMask.count(1) == roleMask.count(2) == 2:
            roleMaskFilled.append(roleMask.copy())
    return teamMaskfilled, roleMaskFilled


def formPlayersData(Lobby):
    Ps = []
    for Custom_Iterator in range(len(Lobby)):
        C = Custom.select().where(Custom.ID == Lobby[Custom_Iterator])
        if C.exists():
            C = C[0]
            Ps.append({"Custom": C})
            if "T" in C.Player.Roles:
                Ps[Custom_Iterator][0] = C.TSR
            if "D" in C.Player.Roles:
                Ps[Custom_Iterator][1] = C.DSR
            if "H" in C.Player.Roles:
                Ps[Custom_Iterator][2] = C.HSR
    return Ps


# print(formPlayersData(GetLobby(1)))
def countByMask(teamMask, roleMaskFilled, Ps):
    first_team = []
    second_team = []
    for pointer in range(len(teamMask)):
        if teamMask[pointer]:
            second_team.append(Ps[pointer])
        else:
            first_team.append(Ps[pointer])
    corrected_fb = []
    for Mask in roleMaskFilled:
        tr = 1
        for k in range(len(Mask)):
            if not Mask[k] in list(first_team[k].keys()):
                tr = 0
        if tr:
            print(Mask)

    # print(first_team)
    # print(second_team)


def createGame(Profile_ID):
    teamMask, roleMask = preGenerate()
    Lobby = GetLobby(Profile_ID)
    Ps = formPlayersData(Lobby)
    # for Mask in roleMask:

    print(countByMask(teamMask[0], roleMask, formPlayersData(GetLobby(1))))


createGame(1)
