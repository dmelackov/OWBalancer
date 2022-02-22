from app.DataBase.LobbyСollector import GetLobby, GetUserSettings
import random
import itertools
import datetime
from functools import cmp_to_key
from app.DataBase.db import *
from app.Static.globalClasses import *


def generateMask(countPlayers):
    teamMask = []
    roleMask = []

    for i in itertools.product(range(2), repeat=countPlayers * 2):
        if i.count(0) == countPlayers:
            teamMask.append(i)

    for i in itertools.product(range(4), repeat=countPlayers):
        if 0 in i and 2 in i:
            roleMask.append(i)

    return teamMask, roleMask


def groupTeamMask(teamMask):
    groups = []
    points = {2: []}

    for i in


def formPlayersData(Lobby, Creator):
    Members = []
    accord = {}
    C = Custom.select().where(Custom.ID << Lobby)
    PlayersList = []
    if C.exists():
        for CustomIterator in C:
            P = CustomIterator.Player
            PlayersList.append(P)
            M = ClassPlayer(CustomIterator.SR)
            Members.append(M)
            accord[CustomIterator.Player] = M
    PR = PlayerRoles.select().where(PlayerRoles.Player << PlayersList, PlayerRoles.Creator == Creator)
    if PR.exists():
        for PRIterator in PR:
            accord[PRIterator.Player].setRoles(PRIterator.Roles, PRIterator.isFlex)
    return Members


def formGoodBal(first, second, fBalance, sBalance):
    data = {"pareTeamAVG": 0, "NeuroPredict": 0,
            "first": {"AVG": fBalance.AVG, "RolePoints": fBalance.PriorityPoints, 0: [], 1: [], 2: []},
            "second": {"AVG": sBalance.AVG, "RolePoints": sBalance.PriorityPoints, 0: [], 1: [], 2: []}}
    Range = 0
    FTSquare = 0
    STSquare = 0
    dsr = {0: {0: [], 1: [], 2: []}, 1: {0: [], 1: [], 2: []}}
    for i in range(len(fBalance.Mask)):
        data["first"][fBalance.Mask[i]].append(first[i].serialization())
        RoleRating = first[i].Rating[fBalance.Mask[i]]
        Range += RoleRating
        dsr[0][fBalance.Mask[i]].append(RoleRating)
        FTSquare += (RoleRating - fBalance.AVG) ** 2

    for i in range(len(sBalance.Mask)):
        data["second"][sBalance.Mask[i]].append(second[i].serialization())
        RoleRating = second[i].Rating[sBalance.Mask[i]]
        Range -= RoleRating
        dsr[1][sBalance.Mask[i]].append(RoleRating)
        STSquare += (RoleRating - sBalance.AVG) ** 2
    data["pareTeamAVG"] = abs(Range)
    data["rangeTeam"] = abs((FTSquare // len(fBalance.Mask)) ** 0.5 - (STSquare // len(sBalance.Mask)) ** 0.5)
    data["NeuroPredict"] = dsr
    return data


def tryRoleMask(Balance, roleMask):
    goodMask = []
    for RM in roleMask:
        accord = True
        AVG = 0
        PriorityPoints = 0
        for i in range(len(RM)):
            P = team[i]
            if (RM[i] not in P.Roles and not P.isFlex) or not accord:
                accord = False
            else:
                PriorityPoints += (3 - P.Roles.index(RM[i])) if not P.isFlex else 3
                AVG += team[i].Rating[RM[i]]
        if accord:
            goodMask.append(Balance(AVG // len(RM), RM, PriorityPoints))
    return goodMask


def tryTeamMask(TM, Members):
    first_team = []
    second_team = []
    for i in range(len(TM)):
        if TM[i]:
            second_team.append(Members[i])
        else:
            first_team.append(Members[i])
    Balance = ClassGameBalance(first_team, second_team)
    return Balance.calcSR(), Balance

    # ft_gm = tryRoleMask(first_team, roleMask)
    # st_gm = tryRoleMask(second_team, roleMask)
    #
    # final_balance = []
    # for f in ft_gm:
    #     for s in st_gm:
    #         if f - s <= 50:
    #             gd_bl = formGoodBal(first_team, second_team, f, s)
    #             if gd_bl["pareTeamAVG"] <= pareTeam:
    #                 final_balance.append(gd_bl)
    # return final_balance


def randLobby(Lobby, PlayersInTeam):
    if PlayersInTeam * 2 < len(Lobby):
        PlayersLobby = random.sample(Lobby, PlayersInTeam * 2)
    else:
        PlayersLobby = Lobby
    return PlayersLobby


def createGame(U):
    UserSettings = U.getUserSettings()
    PlayersInTeam = UserSettings["PlayersIn"]

    teamMask, roleMask = generateMask(PlayersInTeam)
    Lobby = U.getLobbyInfo()
    Lobby = randLobby(Lobby, PlayersInTeam)

    if len(Lobby) == PlayersInTeam * 2:
        Members = formPlayersData(Lobby, U.ID)
        s = []
        for TM in teamMask:
            CBalance = tryTeamMask(TM, Members)
            s.append(CBalance)
        for TM in sorted(s)[:50]:


    #     linear_sort = sorted(s, key=cmp_to_key(sort_comparator))[0:1000]
    #     if UserSettings["Amount"]["T"] == UserSettings["Amount"]["D"] == UserSettings["Amount"]["H"] == 2 \
    #             and UserSettings["Network"]:
    #         for ind, el in enumerate(linear_sort):
    #             linear_sort[ind]['NeuroPredict'] = doPredict(main_net, el)
    #         # neuro_sorted = sorted(linear_sort, key=lambda item: abs(item['NeuroPredict']))
    #
    #         # print(*neuro_sorted[:600], sep="\n")
    #         return linear_sort
    #     else:
    #         for ind, el in enumerate(linear_sort):
    #             linear_sort[ind]['NeuroPredict'] = 0
    #         return linear_sort
    # return False


d1 = datetime.datetime.now()
User = Profile.get(Profile.ID == 1)
print(*createGame(User), sep="\n")
d2 = datetime.datetime.now()
print("Весь метод:", str(d2 - d1))
