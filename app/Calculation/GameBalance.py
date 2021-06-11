from app.DataBase.db import *
from app.DataBase.LobbyСollector import GetLobby
import itertools
import copy


def createGame(Profile_ID):
    Lobby = GetLobby(Profile_ID)
    # Sorted_Lobby = {
    #     "T": {},
    #     "D": {},
    #     "H": {}
    # }
    Data = {
        "T": [],
        "D": [],
        "H": []
    }
    for Custom_ID in Lobby:
        C = Custom.select().where(Custom.ID == Custom_ID)
        if C.exists():
            C = C[0]
            for role in C.Player.Roles:
                Data[role].append(C)
                # if role == "T":
                #     Data[role].append(C)
                #     Sorted_Lobby[role][C.Player.Username] = C.TSR
                # if role == "D":
                #     Data[role].append(C)
                #     Sorted_Lobby[role][C.Player.Username] = C.DSR
                # if role == "H":
                #     Data[role].append(C)
                #     Sorted_Lobby[role][C.Player.Username] = C.HSR
    iterating_players(Data)
    # for i in itertools.product(Data["T"], Data["T"], Data["D"], Data["D"], Data["H"], Data["H"]):
    #     if len(set(i)) == 6:
    #         a = 0
    #         for j in range(6):
    #             if 0 <= j <= 1:
    #                 print("T:" + i[j].Player.Username, end=" ")
    #             if 2 <= j <= 3:
    #                 print("D:" + i[j].Player.Username, end=" ")
    #             if 4 <= j <= 5:
    #                 print("H:" + i[j].Player.Username, end=" ")
    #         print()
    print(Data)


def iterating_players(Data):
    for i in itertools.product(Data["T"], Data["T"], Data["D"], Data["D"], Data["H"], Data["H"]):
        if len(set(i)) == 6:

            cacheData = copy.deepcopy(Data)

            for j in i:
                if j in cacheData["T"]:
                    cacheData["T"].remove(j)
                if j in cacheData["D"]:
                    cacheData["D"].remove(j)
                if j in cacheData["H"]:
                    cacheData["H"].remove(j)

            # for j in range(6):
            #     if 0 <= j <= 1:
            #         print("T:" + i[j].Player.Username, end=" ")
            #     if 2 <= j <= 3:
            #         print("D:" + i[j].Player.Username, end=" ")
            #     if 4 <= j <= 5:
            #         print("H:" + i[j].Player.Username, end=" ")
            # print()


mass = [1, 2, 3, 4, 5, 6]
for i in mass:
    mass.remove(i)
print(mass)
