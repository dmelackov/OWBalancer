from app.Static.globalClasses import ClassPlayer, ClassGameBalance, ClassTeam


def checkTeamMask(TeamMask, PlayersOnline):
    return TeamMask.count("1") == TeamMask.count("0") == (PlayersOnline // 2)


def checkRoleMask(fTeamMask, sTeamMask, PlayersOnline):
    return (
            fTeamMask.count("0") == sTeamMask.count("0") and
            fTeamMask.count("1") == sTeamMask.count("1") and
            fTeamMask.count("2") == sTeamMask.count("2") and
            len(fTeamMask) + len(sTeamMask) == PlayersOnline
    )


def recountModel(static, active, U):
    UserSettings = U.getUserSettings()
    Members = [ClassPlayer(i["TSR"], i["DSR"], i["HSR"], i["Username"]) for i in static]
    for i in range(len(Members)):
        Members[i].selectRoles(static[i]["Roles"], static[i]["Flex"])
    if checkTeamMask(active["TeamMask"], len(Members)) and \
            checkRoleMask(active["fMask"], active["sMask"], len(Members)):
        fTeam = ClassTeam(Members, active["TeamMask"], 0)
        sTeam = ClassTeam(Members, active["TeamMask"], 1)
        #if fTeam.checkMask(active["fMask"]) and sTeam.checkMask(active["sMask"]):
        Balance = ClassGameBalance(fTeam, sTeam, active["TeamMask"], active["fMask"], active["sMask"])
        Balance.calcResult(UserSettings)
        return Balance.dict()
    return False


# static = {'static':
#               [{'Username': 'Artmagic', 'TSR': 3100, 'DSR': 2900, 'HSR': 2800, 'Flex': False, 'Roles': 'TD'},
#                {'Username': 'Ivarys', 'TSR': 2900, 'DSR': 2900, 'HSR': 2799, 'Flex': False, 'Roles': 'DT'},
#                {'Username': 'Honoka', 'TSR': 3200, 'DSR': 3200, 'HSR': 3200, 'Flex': False, 'Roles': 'HD'},
#                {'Username': 'Quru', 'TSR': 2700, 'DSR': 2800, 'HSR': 3300, 'Flex': False, 'Roles': 'DH'},
#                {'Username': 'Dima', 'TSR': 2800, 'DSR': 2900, 'HSR': 3100, 'Flex': False, 'Roles': 'TD'},
#                {'Username': 'S1lver', 'TSR': 2600, 'DSR': 2600, 'HSR': 2900, 'Flex': False, 'Roles': 'DT'},
#                {'Username': 'zMize', 'TSR': 2800, 'DSR': 2600, 'HSR': 2400, 'Flex': False, 'Roles': 'TD'},
#                {'Username': 'Konder', 'TSR': 3800, 'DSR': 3100, 'HSR': 3400, 'Flex': False, 'Roles': 'DT'},
#                {'Username': 'Svevoloch', 'TSR': 3000, 'DSR': 2900, 'HSR': 2850, 'Flex': False, 'Roles': 'DH'},
#                {'Username': 'AuntPetunia', 'TSR': 3200, 'DSR': 2700, 'HSR': 2800, 'Flex': False, 'Roles': 'HD'},
#                {'Username': 'Cherry', 'TSR': 3200, 'DSR': 2850, 'HSR': 3300, 'Flex': False, 'Roles': 'HT'},
#                {'Username': 'Tia_ti', 'TSR': 2000, 'DSR': 3200, 'HSR': 2500, 'Flex': False, 'Roles': 'HT'}]}
# active = {'active': {'TeamMask': '011001110100', 'fMask': '010122', 'sMask': '021012', 'dpFairness': 0,
#                      'rgRolesFairness': 0, 'teamRolePriority': 0, 'vqUniformity': 0, 'result': 0}}
# print(recountModel(
#     static["static"], active["active"]
# ))
