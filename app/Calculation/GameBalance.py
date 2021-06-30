from app.DataBase.db import *
from app.DataBase.LobbyСollector import GetLobby, GetRolesAmount
import random
import datetime


def preGenerate(RolesAmount, PlayersInTeam):
    teamMask = [0 for i in range(PlayersInTeam * 2)]
    teamMaskfilled = []
    for i in range(2 ** (PlayersInTeam * 2) - 1):
        teamMask[0] += 1
        for j in range(PlayersInTeam * 2 - 1):
            if teamMask[j] > 1:
                teamMask[j + 1] += 1
                teamMask[j] -= 2
        if teamMask.count(0) == teamMask.count(1) == PlayersInTeam and \
                not [0 if i else 1 for i in teamMask] in teamMaskfilled:
            teamMaskfilled.append(teamMask.copy())

    roleMask = [0 for i in range(PlayersInTeam)]
    roleMaskFilled = []
    for i in range(3 ** PlayersInTeam - 1):
        roleMask[0] += 1
        for j in range(PlayersInTeam - 1):
            if roleMask[j] > 2:
                roleMask[j + 1] += 1
                roleMask[j] -= 3
        if roleMask.count(0) == RolesAmount["Amount"]["T"] and \
                roleMask.count(1) == RolesAmount["Amount"]["D"] and \
                roleMask.count(2) == RolesAmount["Amount"]["H"]:
            roleMaskFilled.append(roleMask.copy())
    return teamMaskfilled, roleMaskFilled


def formPlayersData(Lobby):
    Ps = []
    for Custom_Iterator in Lobby:
        C = Custom.select().where(Custom.ID == Custom_Iterator)
        if C.exists():
            C = C[0]
            Ps.append(C)
    return Ps


# def formGoodBal(first, second, fMask, sMask, fAVG, sAVG):
#     data = {"first": {}, "second": {}}
#     data["first"]["AVG"] = fAVG
#     data["second"]["AVG"] = sAVG
#     for i in range(len(fMask)):
#         data["first"][]


def tryRoleMask(team, roleMask, PlayersInTeam):
    goodMask = []
    for RM in roleMask:
        tr = True
        AVG = 0
        for i in range(len(RM)):
            if not RM[i] in [0 if i == "T" else 1 if i == "D" else 2 if i == "H" else -1
                             for i in team[i].Player.Roles]:
                tr = False
            else:
                if RM[i] == 0:
                    AVG += team[i].TSR
                elif RM[i] == 1:
                    AVG += team[i].DSR
                elif RM[i] == 2:
                    AVG += team[i].HSR
        if tr:
            goodMask.append([AVG // PlayersInTeam, RM])
    return goodMask


def tryTeamMask(TM, roleMask, Ps, PlayersInTeam):
    first_team = []
    second_team = []
    for i in range(len(TM)):
        if TM[i]:
            second_team.append(Ps[i])
        else:
            first_team.append(Ps[i])

    ft_gm = tryRoleMask(first_team, roleMask, PlayersInTeam)
    st_gm = tryRoleMask(second_team, roleMask, PlayersInTeam)

    good_balance = []
    for f in ft_gm:
        for s in st_gm:
            if s[0] - 10 <= f[0] <= s[0] + 10:
                good_balance.append([f, s])
    return len(good_balance)


def randLobby(Lobby, PlayersInTeam):
    ExtendedLobby = False
    if PlayersInTeam * 2 < len(Lobby):
        PlayersLobby = random.sample(Lobby, PlayersInTeam * 2)
        ExtendedLobby = True
    else:
        PlayersLobby = Lobby
    return PlayersLobby, ExtendedLobby


def createGame(Profile_ID):

    RolesAmount = GetRolesAmount(Profile_ID)
    PlayersInTeam = RolesAmount["Amount"]["T"] + RolesAmount["Amount"]["D"] + RolesAmount["Amount"]["H"]

    teamMask, roleMask = preGenerate(RolesAmount, PlayersInTeam)
    Lobby = GetLobby(Profile_ID)
    Lobby, ExtendedLobby = randLobby(Lobby, PlayersInTeam)

    FullLobby = False
    if len(Lobby) == PlayersInTeam * 2:
        FullLobby = True
        Ps = formPlayersData(Lobby)
        s = 0
        for TM in teamMask:
            s += tryTeamMask(TM, roleMask, Ps, PlayersInTeam)
        print(s)


d1 = datetime.datetime.now()
createGame(1)
d2 = datetime.datetime.now()
print(str(d2 - d1))
