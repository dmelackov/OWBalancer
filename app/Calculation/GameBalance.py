from app.DataBase.LobbyСollector import GetLobby, GetUserSettings
import random
import datetime
from functools import cmp_to_key
import torch
from app.Static.globalClasses import *


def minmaxscaler(data):
    mass = []
    for ind, el in enumerate(data):
        mass.append(el / 5000)
    return mass


class Network(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.Sigm = torch.nn.Sigmoid()
        self.fc1 = torch.nn.Linear(6, 12)
        self.Act1 = torch.nn.LeakyReLU()
        self.fc2 = torch.nn.Linear(12, 6)
        self.Act2 = torch.nn.LeakyReLU()
        self.Last = torch.nn.Linear(12, 1)

    def forward(self, x):
        t1 = self.fc1(torch.tensor(minmaxscaler(x[1])))
        t2 = self.fc1(torch.tensor(minmaxscaler(x[0])))
        t1 = self.Act1(t1)
        t2 = self.Act1(t2)
        t1 = self.fc2(t1)
        t2 = self.fc2(t2)
        x = self.Act2(torch.cat((t1, t2), 0))
        x = self.Last(x)
        x = self.Sigm(x)
        return x


def doPredict(main_net, data):
    prepared_mass = [data["NeuroPredict"][0][0] + data["NeuroPredict"][0][1] + data["NeuroPredict"][0][2]]
    prepared_mass += [data["NeuroPredict"][1][0] + data["NeuroPredict"][1][1] + data["NeuroPredict"][1][2]]
    tensor_data = torch.FloatTensor(prepared_mass)
    predict = main_net.forward(tensor_data)
    return int((float(predict) - 0.5) * 200)


def preGenerate(RolesAmount, PlayersInTeam):
    teamMask = [0 for _ in range(PlayersInTeam * 2)]
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

    roleMask = [0 for _ in range(PlayersInTeam)]
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


def formPlayersData(Lobby, Creator):
    Members = []
    accord = {}
    C = Custom.select().where(Custom.ID << Lobby)
    PlayersList = []
    if C.exists():
        for CustomIterator in C:
            P = CustomIterator.Player
            PlayersList.append(P)
            M = Member()
            M.setData(P, CustomIterator)
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


def sort_comparator(left, right):
    left_arg = left["pareTeamAVG"]
    right_arg = right["pareTeamAVG"]

    lf = left["first"]["RolePoints"]
    ls = left["second"]["RolePoints"]
    rf = right["first"]["RolePoints"]
    rs = right["second"]["RolePoints"]
    if lf + ls > rf + rs:
        return -1
    elif lf + ls < rf + rs:
        return 1
    elif 0 < abs(left_arg - right_arg) <= 100:
        if abs(left["rangeTeam"]) < abs(right["rangeTeam"]):
            return -1
        elif abs(left["rangeTeam"]) > abs(right["rangeTeam"]):
            return 1
        else:
            return 0
    elif left_arg < right_arg:
        return -1
    elif left_arg > right_arg:
        return 1
    elif abs(lf - ls) < abs(rf - rs):
        return -1
    elif abs(lf - ls) > abs(rf - rs):
        return 1
    else:
        return 0


def tryRoleMask(team, roleMask):
    goodMask = []
    for RM in roleMask:
        accord = True
        AVG = 0
        PriorityPoints = 0
        for i in range(len(RM)):
            P = team[i]
            if RM[i] not in P.Roles or not accord:
                accord = False
            else:
                PriorityPoints += (3 - P.Roles.index(RM[i])) if not P.isFlex else 3
                AVG += team[i].Rating[RM[i]]
        if accord:
            goodMask.append(Balance(AVG // len(RM), RM, PriorityPoints))
    return goodMask


def tryTeamMask(TM, roleMask, Members, pareTeam):
    first_team = []
    second_team = []
    for i in range(len(TM)):
        if TM[i]:
            second_team.append(Members[i])
        else:
            first_team.append(Members[i])

    ft_gm = tryRoleMask(first_team, roleMask)
    st_gm = tryRoleMask(second_team, roleMask)

    final_balance = []
    for f in ft_gm:
        for s in st_gm:
            if f - s <= 50:
                gd_bl = formGoodBal(first_team, second_team, f, s)
                if gd_bl["pareTeamAVG"] <= pareTeam:
                    final_balance.append(gd_bl)
    return final_balance


def randLobby(Lobby, PlayersInTeam):
    if PlayersInTeam * 2 < len(Lobby):
        PlayersLobby = random.sample(Lobby, PlayersInTeam * 2)
    else:
        PlayersLobby = Lobby
    return PlayersLobby


def createGame(U):
    main_net = torch.load("app/Calculation/NeuroBalance/Data.txt")
    UserSettings = U.getUserSettings()
    PlayersInTeam = UserSettings["Amount"]["T"] + UserSettings["Amount"]["D"] + UserSettings["Amount"]["H"]

    teamMask, roleMask = preGenerate(UserSettings, PlayersInTeam)
    Lobby = U.getLobbyInfo()
    Lobby = randLobby(Lobby, PlayersInTeam)

    if len(Lobby) == PlayersInTeam * 2:
        Members = formPlayersData(Lobby, U.ID)
        s = []
        for TM in teamMask:
            tTM = tryTeamMask(TM, roleMask, Members, UserSettings["BalanceLimit"])
            if tTM:
                s += tTM
        linear_sort = sorted(s, key=cmp_to_key(sort_comparator))[0:1000]
        if UserSettings["Amount"]["T"] == UserSettings["Amount"]["D"] == UserSettings["Amount"]["H"] == 2 \
                and UserSettings["Network"]:
            for ind, el in enumerate(linear_sort):
                linear_sort[ind]['NeuroPredict'] = doPredict(main_net, el)
            # neuro_sorted = sorted(linear_sort, key=lambda item: abs(item['NeuroPredict']))

            # print(*neuro_sorted[:600], sep="\n")
            return linear_sort
        else:
            for ind, el in enumerate(linear_sort):
                linear_sort[ind]['NeuroPredict'] = 0
            return linear_sort
    return False


# d1 = datetime.datetime.now()
# User = Profile.get(Profile.ID == 1)
# print(*createGame(User), sep="\n")
# d2 = datetime.datetime.now()
# print("Весь метод:", str(d2 - d1))
