from app.DataBase.db import *



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
