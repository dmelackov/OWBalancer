from app.DataBase.db import *
from app.DataBase.LobbyСollector import GetLobby, GetUserSettings
import random
import datetime
from functools import cmp_to_key
import torch


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
    C = Custom.select().where(Custom.ID << Lobby)
    if C.exists():
        for CustomIterator in C:
            Ps.append(CustomIterator)
    return Ps


def formGoodBal(first, second, fMask, sMask, fAVG, sAVG, fTeamRolePrior, sTeamRolePrior, main_net):
    data = {"pareTeamAVG": 0, "NeuroPredict": 0,
            "first": {"AVG": fAVG, "RolePoints": fTeamRolePrior, 0: [], 1: [], 2: []},
            "second": {"AVG": sAVG, "RolePoints": sTeamRolePrior, 0: [], 1: [], 2: []}}
    T_Range = 0
    D_Range = 0
    H_Range = 0
    FTSquare = 0
    STSquare = 0
    dsr = {0: {0: [], 1: [], 2: []}, 1: {0: [], 1: [], 2: []}}
    for i in range(len(fMask)):
        data["first"][fMask[i]].append(first[i].ID)
        if fMask[i] == 0:
            T_Range += first[i].TSR
            dsr[0][0].append(first[i].TSR)
            FTSquare += (first[i].TSR - data["first"]["AVG"]) ** 2
        elif fMask[i] == 1:
            D_Range += first[i].DSR
            dsr[0][1].append(first[i].DSR)
            FTSquare += (first[i].DSR - data["first"]["AVG"]) ** 2
        elif fMask[i] == 2:
            H_Range += first[i].HSR
            dsr[0][2].append(first[i].HSR)
            FTSquare += (first[i].HSR - data["first"]["AVG"]) ** 2
    for i in range(len(sMask)):
        data["second"][sMask[i]].append(second[i].ID)
        if sMask[i] == 0:
            T_Range -= second[i].TSR
            dsr[1][0].append(second[i].TSR)
            STSquare += (first[i].TSR - data["second"]["AVG"]) ** 2
        elif sMask[i] == 1:
            D_Range -= second[i].DSR
            dsr[1][1].append(second[i].DSR)
            STSquare += (first[i].DSR - data["second"]["AVG"]) ** 2
        elif sMask[i] == 2:
            H_Range -= second[i].HSR
            dsr[1][2].append(second[i].HSR)
            STSquare += (first[i].HSR - data["second"]["AVG"]) ** 2
    data["pareTeamAVG"] = abs(T_Range) + abs(D_Range) + abs(H_Range)
    data["rangeTeam"] = abs((FTSquare // len(fMask)) ** 0.5 - (STSquare // len(sMask)) ** 0.5)
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
    elif abs(left_arg - right_arg) <= 100:
        if abs(left["rangeTeam"]) < abs(right["rangeTeam"]):
            return -1
        else:
            return 1
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


def tryRoleMask(team, roleMask, PlayersInTeam):
    goodMask = []
    for RM in roleMask:
        tr = True
        AVG = 0
        TeamRolePrior = 0
        for i in range(len(RM)):
            P = team[i].Player
            if not RM[i] in [0 if j == "T" else 1 if j == "D" else 2 if j == "H" else -1
                             for j in P.Roles]:
                tr = False
            else:
                if RM[i] == 0:
                    AVG += team[i].TSR
                    TeamRolePrior += (3 - P.Roles.index("T")) if not P.isFlex else 3
                elif RM[i] == 1:
                    AVG += team[i].DSR
                    TeamRolePrior += (3 - P.Roles.index("D")) if not P.isFlex else 3
                elif RM[i] == 2:
                    AVG += team[i].HSR
                    TeamRolePrior += (3 - P.Roles.index("H")) if not P.isFlex else 3
        if tr:
            goodMask.append([AVG // PlayersInTeam, RM, TeamRolePrior])
    return goodMask


def tryTeamMask(TM, roleMask, Ps, PlayersInTeam, pareTeam, main_net):
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
            if abs(s[0] - f[0]) <= 50:
                gd_bl = formGoodBal(first_team, second_team, f[1], s[1], f[0], s[0], f[2], s[2], main_net)
                if gd_bl["pareTeamAVG"] <= pareTeam:
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


def createGame(Profile_ID, pareTeam=1000):
    main_net = torch.load("app/Calculation/NeuroBalance/Data.txt")
    UserSettings = GetUserSettings(Profile_ID)
    PlayersInTeam = UserSettings["Amount"]["T"] + UserSettings["Amount"]["D"] + UserSettings["Amount"]["H"]

    teamMask, roleMask = preGenerate(UserSettings, PlayersInTeam)
    Lobby = GetLobby(Profile_ID)
    Lobby, ExtendedLobby = randLobby(Lobby, PlayersInTeam)

    if len(Lobby) == PlayersInTeam * 2:
        Ps = formPlayersData(Lobby)
        s = []
        for TM in teamMask:
            tTM = tryTeamMask(TM, roleMask, Ps, PlayersInTeam, pareTeam, main_net)
            if tTM:
                s += tTM
        linear_sort = sorted(s, key=cmp_to_key(sort_comparator))[0:1000]
        if UserSettings["Amount"]["T"] == UserSettings["Amount"]["D"] == UserSettings["Amount"]["H"] == 2:
            for ind, el in enumerate(linear_sort):
                linear_sort[ind]['NeuroPredict'] = doPredict(main_net, el)
            neuro_sorted = sorted(linear_sort, key=lambda item: abs(item['NeuroPredict']))

            # print(*neuro_sorted[:600], sep="\n")
            return ExtendedLobby, neuro_sorted
        else:
            return ExtendedLobby, linear_sort
    return False


# d1 = datetime.datetime.now()
# print(len(createGame(1)[1]))
# d2 = datetime.datetime.now()
# print("Весь метод:", str(d2 - d1))
