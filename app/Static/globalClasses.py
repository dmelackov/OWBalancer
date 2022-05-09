# 0 - closest
import json


def dpFairness(X, Y, p):
    # count p-Fairness of the game,
    # where s - skillRatings; X, Y - players for each team
    return abs(
        pow(sum(map(lambda x: x ** p, X)), 1 / p) - pow(sum(map(lambda y: y ** p, Y)), 1 / p)
    )


def rgRolesFairness(X, Y, fMask, sMask, g, tWeight, dWeight, hWeight):
    # count g-RoleFairness with role weights
    fRoles = [0] * 3
    sRoles = [0] * 3
    for i, role in enumerate(fMask):
        fRoles[int(role)] += X[i]
    for i, role in enumerate(sMask):
        sRoles[int(role)] += Y[i]
    return abs(
        pow(
            (
                    (
                            (abs(fRoles[0] - sRoles[0]) * tWeight) ** g +
                            (abs(fRoles[1] - sRoles[1]) * dWeight) ** g +
                            (abs(fRoles[2] - sRoles[2]) * hWeight) ** g
                    ) / 3
            ),
            1 / g
        )
    )


# 0 - closest
def vqUniformity(X, Y, q):
    # count q-uniformity of the game
    # where s - skillRatings; Z = X + Y - all players
    Z = X + Y
    muz = sum(Z) / len(Z)
    return abs(
        pow(sum(map(lambda x: abs(x - muz) ** q, X)) / len(X), 1 / q) -
        pow(sum(map(lambda y: abs(y - muz) ** q, Y)) / len(Y), 1 / q)
    )


def teamRolePriority(fPlayers, sPlayers, fMask, sMask):
    Points = (len(fPlayers) + len(sPlayers)) * 3
    fTeamRoles = len(fPlayers) * 3
    for i, role in enumerate(fMask):
        sub = fPlayers[i].rolePriorityPoints(int(role))
        Points -= sub
        fTeamRoles -= sub

    sTeamRoles = len(sPlayers) * 3
    for i, role in enumerate(sMask):
        sub = sPlayers[i].rolePriorityPoints(int(role))
        sTeamRoles -= sub
        Points -= sub
    Points += 0.2 * (abs(fTeamRoles - sTeamRoles) if abs(fTeamRoles - sTeamRoles) > 1 else 0)
    return Points


def imbalanceFunc(X, Y, fMask, sMask, fPlayers, sPlayers, USettings):
    # const init
    MathSettings = USettings["Math"]
    tWeight = MathSettings["tWeight"]
    dWeight = MathSettings["dWeight"]
    hWeight = MathSettings["hWeight"]
    alpha = MathSettings["alpha"]
    beta = MathSettings["beta"]
    gamma = MathSettings["gamma"]
    p = MathSettings["p"]
    q = MathSettings["q"]
    return (
        alpha * dpFairness(X, Y, p),
        beta * rgRolesFairness(X, Y, fMask, sMask, p, tWeight, dWeight, hWeight),
        gamma * teamRolePriority(fPlayers.Players, sPlayers.Players, fMask, sMask),
        vqUniformity(X, Y, q)
    )


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
        if R not in self.Roles:
            return 0
        return (3 - self.Roles.index(R)) if not self.Flex else 3


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

    def __eq__(self, other):
        if self.result == other.result:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.result < other.result:
            return True
        else:
            return False
