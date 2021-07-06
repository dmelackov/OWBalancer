from app.DataBase.db import *
from app.DataBase.LobbyСollector import GetLobby, GetRolesAmount
import random
import datetime
from functools import cmp_to_key


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


def formGoodBal(first, second, fMask, sMask, fAVG, sAVG, fTeamRolePrior, sTeamRolePrior):
    data = {"pareTeamAVG": 0,
            "first": {"AVG": fAVG, "RolePoints": fTeamRolePrior, 0: [], 1: [], 2: []},
            "second": {"AVG": sAVG, "RolePoints": sTeamRolePrior, 0: [], 1: [], 2: []}}
    T_Range = 0
    D_Range = 0
    H_Range = 0
    for i in range(len(fMask)):
        data["first"][fMask[i]].append(first[i].ID)
        if fMask[i] == 0:
            T_Range += first[i].TSR
        elif fMask[i] == 1:
            D_Range += first[i].DSR
        elif fMask[i] == 2:
            H_Range += first[i].HSR
    for i in range(len(sMask)):
        data["second"][sMask[i]].append(second[i].ID)
        if sMask[i] == 0:
            T_Range -= second[i].TSR
        elif sMask[i] == 1:
            D_Range -= second[i].DSR
        elif sMask[i] == 2:
            H_Range -= second[i].HSR
    data["pareTeamAVG"] = abs(T_Range) + abs(D_Range) + abs(H_Range)
    return data


def sort_comparator(left, right):
    left_arg = left["pareTeamAVG"]
    right_arg = right["pareTeamAVG"]
    if left["first"]["RolePoints"] + left["second"]["RolePoints"] > \
            right["first"]["RolePoints"] + right["second"]["RolePoints"]:
        return -1
    elif left["first"]["RolePoints"] + left["second"]["RolePoints"] < \
            right["first"]["RolePoints"] + right["second"]["RolePoints"]:
        return 1
    elif left_arg < right_arg:
        return -1
    elif left_arg > right_arg:
        return 1
    else:
        return 0


def tryRoleMask(team, roleMask, PlayersInTeam):
    goodMask = []
    for RM in roleMask:
        tr = True
        AVG = 0
        TeamRolePrior = 0
        for i in range(len(RM)):
            if not RM[i] in [0 if j == "T" else 1 if j == "D" else 2 if j == "H" else -1
                             for j in team[i].Player.Roles]:
                tr = False
            else:
                if RM[i] == 0:
                    AVG += team[i].TSR
                    TeamRolePrior += (3 - team[i].Player.Roles.index("T"))
                elif RM[i] == 1:
                    AVG += team[i].DSR
                    TeamRolePrior += (3 - team[i].Player.Roles.index("D"))
                elif RM[i] == 2:
                    AVG += team[i].HSR
                    TeamRolePrior += (3 - team[i].Player.Roles.index("H"))
        if tr:
            goodMask.append([AVG // PlayersInTeam, RM, TeamRolePrior])
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
            if s[0] - 25 <= f[0] <= s[0] + 25:
                gd_bl = formGoodBal(first_team, second_team, f[1], s[1], f[0], s[0], f[2], s[2])
                if gd_bl["pareTeamAVG"] <= 1500:
                    good_balance.append(gd_bl)
    return good_balance


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

    if len(Lobby) == PlayersInTeam * 2:
        Ps = formPlayersData(Lobby)
        s = []
        for TM in teamMask:
            tTM = tryTeamMask(TM, roleMask, Ps, PlayersInTeam)
            if tTM:
                s += tTM
        # print(*sorted(s, key=cmp_to_key(sort_comparator))[0:100], sep="\n")
        return ExtendedLobby, sorted(s, key=cmp_to_key(sort_comparator))
    return False


# d1 = datetime.datetime.now()
# createGame(1)
# d2 = datetime.datetime.now()
# print(str(d2 - d1))
