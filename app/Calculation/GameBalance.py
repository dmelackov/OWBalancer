from app.Static.globalClasses import ClassPlayer, ClassGameBalance, ClassTeam
import itertools
import random
import datetime
from app.DataBase.db import *


def generateMask(countPlayers, countTanks, countDps):
    teamMask = []
    roleMask = []

    for i in itertools.product(range(2), repeat=(countPlayers * 2) - 1):
        if i.count(1) == countPlayers:
            teamMask.append("".join(["0"] + [str(el) for el in i]))

    for i in itertools.product(range(3), repeat=countPlayers):
        if i.count(0) == countTanks and i.count(1) == countDps:
            roleMask.append("".join([str(el) for el in i]))

    return teamMask, roleMask


def formPlayersData(Lobby, Creator):
    Members = []
    accord = {}
    C = Custom.select().where(Custom.ID << Lobby)
    PlayersList = []
    if C.exists():
        for CustomIterator in C:
            P = CustomIterator.Player
            PlayersList.append(P)
            M = ClassPlayer(CustomIterator.TSR, CustomIterator.DSR, CustomIterator.HSR, CustomIterator.Player.Username)
            Members.append(M)
            accord[CustomIterator.Player] = M
    PR = PlayerRoles.select().where(PlayerRoles.Player << PlayersList, PlayerRoles.Creator == Creator)
    if PR.exists():
        for PRIterator in PR:
            accord[PRIterator.Player].selectRoles(PRIterator.Roles, PRIterator.isFlex)
    return Members


def generateLobby(Lobby, PlayersInTeam):
    if PlayersInTeam * 2 < len(Lobby):
        PlayersLobby = random.sample(Lobby, PlayersInTeam * 2)
    else:
        PlayersLobby = Lobby
    if len(PlayersLobby) == PlayersInTeam * 2:
        return PlayersLobby
    else:
        return False


def checkMask(tm, roleMask, Members, UserSettings):
    fTeam = ClassTeam(Members, tm, 0)
    sTeam = ClassTeam(Members, tm, 1)

    fGoodMask = []
    for mask in roleMask:
        if fTeam.checkMask(mask):
            fGoodMask.append(mask)
    sGoodMask = []
    for mask in roleMask:
        if sTeam.checkMask(mask):
            sGoodMask.append(mask)

    mass = []
    for fMask in fGoodMask:
        for sMask in sGoodMask:
            Balance = ClassGameBalance(fTeam, sTeam, tm, fMask, sMask)
            Balance.calcResult()
            if Balance.result <= UserSettings["BalanceLimit"]:
                mass.append(Balance)
    return mass


def createGame(U):
    UserSettings = U.getUserSettings()
    PlayersInTeam = UserSettings["Amount"]["T"] + UserSettings["Amount"]["D"] + UserSettings["Amount"]["H"]
    teamMask, roleMask = generateMask(PlayersInTeam, UserSettings["Amount"]["T"], UserSettings["Amount"]["D"])

    Lobby = U.getLobbyInfo()
    Lobby = generateLobby(Lobby, PlayersInTeam)

    if Lobby:
        Members = formPlayersData(Lobby, U)
        PlayersDict = []
        for M in Members:
            PlayersDict.append(M.dict())
        s = []
        for tm in teamMask:
            s += checkMask(tm, roleMask, Members, UserSettings)
        s.sort()
        # s[0].calcResult()
        response = {'static': PlayersDict,
                    'active': [i.dict() for i in s[:1000]]}
        return response


# d1 = datetime.datetime.now()
# print(createGame(Profile.select().where(Profile.ID == 1)[0]))
# d2 = datetime.datetime.now()
# print("Весь метод:", str(d2 - d1))
