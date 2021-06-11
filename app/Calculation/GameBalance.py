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


# def formPlayersData(Lobby):

preGenerate()