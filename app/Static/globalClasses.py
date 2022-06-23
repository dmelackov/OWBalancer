from app.Calculation.CalculationMethods import imbalanceFunc
from typing import TypeVar, Generic, Union

T = TypeVar('T')

class ClassRole:
    SR = 0
    tag = ""
    index = -1
    active = False

    def __init__(self, SR, tag, index):
        self.SR = SR
        self.tag = tag
        self.index = index

    def activate(self):
        self.active = True

    def checkRole(self, role):
        if self.index == role or self.tag == role:
            return True
        else:
            return False


class ClassPlayer:
    Roles = ""
    Username = ""
    Flex = False

    def __init__(self, TankSR, DpsSR, HealSR, Username):
        self.Username = Username
        self.TankSR = ClassRole(TankSR, "T", 0)
        self.DpsSR = ClassRole(DpsSR, "D", 1)
        self.HealSR = ClassRole(HealSR, "H", 2)

    def dict(self):
        return {
            'Username': self.Username,
            'TSR': self.TankSR.SR,
            'DSR': self.DpsSR.SR,
            'HSR': self.HealSR.SR,
            'Flex': self.Flex,
            'Roles': self.Roles
        }

    def roleList(self):
        return [self.TankSR, self.DpsSR, self.HealSR]

    def selectRoles(self, R, Flex):
        self.Roles = R
        self.Flex = Flex
        for selector in R:
            if self.TankSR.index == selector or self.TankSR.tag == selector:
                self.TankSR.activate()
            elif self.DpsSR.index == selector or self.DpsSR.tag == selector:
                self.DpsSR.activate()
            elif self.HealSR.index == selector or self.HealSR.tag == selector:
                self.HealSR.activate()

    def checkRole(self, R):
        if self.TankSR.index == R or self.TankSR.tag == R:
            return self.TankSR.active
        elif self.DpsSR.index == R or self.DpsSR.tag == R:
            return self.DpsSR.active
        elif self.HealSR.index == R or self.HealSR.tag == R:
            return self.HealSR.active
        else:
            return False

    def getRoleSR(self, R):
        if self.TankSR.index == R or self.TankSR.tag == R:
            return self.TankSR.SR
        elif self.DpsSR.index == R or self.DpsSR.tag == R:
            return self.DpsSR.SR
        elif self.HealSR.index == R or self.HealSR.tag == R:
            return self.HealSR.SR

    def rolePriorityPoints(self, R):
        R = "T" if R == 0 else "D" if R == 1 else "H" if R == 2 else R
        if self.Flex:
            return 3
        if R not in self.Roles:
            return 0
        return 3 - self.Roles.index(R)


class ClassTeam:
    def __init__(self, Members, TeamMask, TeamIndex):
        self.Players = []
        for i in range(len(TeamMask)):
            if int(TeamMask[i]) == TeamIndex:
                self.Players.append(Members[i])

    def checkMask(self, Mask):
        for i, m in enumerate(Mask):
            if not self.Players[i].checkRole(int(m)) and not self.Players[i].Flex:
                return False
        return True


class ClassGameBalance:
    result = 1e9
    fairness = 0
    rolesFairness = 0
    teamRolePriority = 0
    uniformity = 0
    fMask = []
    sMask = []

    def __init__(self, fTeam, sTeam, TeamMask, fMask, sMask):
        self.fTeam = fTeam
        self.sTeam = sTeam
        self.TeamMask = TeamMask
        self.fTeamSR = []
        self.fMask = fMask
        for i, x in enumerate(self.fTeam.Players):
            self.fTeamSR.append(x.getRoleSR(int(fMask[i])))

        self.sMask = sMask
        self.sTeamSR = []
        for i, y in enumerate(self.sTeam.Players):
            self.sTeamSR.append(y.getRoleSR(int(sMask[i])))

    def calcResult(self, USettings):
        self.fairness, self.rolesFairness, self.teamRolePriority, self.uniformity = \
            imbalanceFunc(self.fTeamSR, self.sTeamSR, self.fMask, self.sMask, self.fTeam, self.sTeam, USettings)
        self.result = self.fairness + self.rolesFairness + self.teamRolePriority + self.uniformity

    def dict(self):
        return {
            'TeamMask': self.TeamMask,
            'fMask': self.fMask,
            'sMask': self.sMask,
            'dpFairness': round(self.fairness, 2),
            'rgRolesFairness': round(self.rolesFairness, 2),
            'teamRolePriority': round(self.teamRolePriority, 2),
            'vqUniformity': round(self.uniformity, 2),
            'result': round(self.result, 2)
        }



class AnswerForm(Generic[T]):
    def __init__(self, status: bool, error: Union[None, str], data: T=None):
        self.status: bool = status
        self.error: Union[None, str] = error
        self.data: T = data

    def __bool__(self):
        return self.status
