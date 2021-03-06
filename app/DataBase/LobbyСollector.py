from app.DataBase.db import *


def GetLobby(Profile_ID):
    U = Profile.select().where(Profile.ID == Profile_ID)
    if U.exists():
        return U[0].getLobbyInfo()


def GetUserSettings(Profile_ID):
    U = Profile.select().where(Profile.ID == Profile_ID)
    if U.exists():
        return U[0].getUserSettings()


def AddToLobby(U, Custom_ID):
    C = Custom.select().where(Custom.ID == Custom_ID)
    if C.exists():
        C = C[0]

        CMass = U.getLobbyInfo()
        USettings = U.getUserSettings()
        TeamPlayers = USettings["Amount"]["T"] + USettings["Amount"]["D"] + USettings["Amount"]["H"]
        if len(CMass) < TeamPlayers * 2 or USettings["ExtendedLobby"]:
            cacheToChange = -1
            for C_ID in CMass:
                if Custom.get(Custom.ID == C_ID).Player == C.Player:
                    cacheToChange = C_ID
            if cacheToChange != -1:
                CMass.remove(cacheToChange)

            if C.ID not in CMass:
                CMass.append(C.ID)
            U.updateLobbyInfo(CMass)
            return True
    return False


def DeleteFromLobby(U, Custom_ID):
    C = Custom.select().where(Custom.ID == Custom_ID)
    if C.exists():
        C = C[0]
        CMass = U.getLobbyInfo()

        if C.ID in CMass:
            CMass.remove(C.ID)
        U.updateLobbyInfo(CMass)
        return True
    return False


def ClearLobby(Profile_ID):
    U = Profile.select().where(Profile.ID == Profile_ID)
    if U.exists():
        U[0].updateLobbyInfo([])
        return True
    return False


# print(GetRolesAmount(1))
# print(DeleteFromLobby(1, 16))
# for i in range(1, 13):
#     print(AddToLobby(1, i))
# print(GetLobby(1))
# AddToLobby(1, 16)
