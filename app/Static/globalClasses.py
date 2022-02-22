# 0 - closest
def dpFairness(X, Y, p):
    # count p-Fairness of the game,
    # where s - skillRatings; X, Y - players for each team
    return abs(
        pow(sum(map(lambda x: x ** p, X)), 1/p) - pow(sum(map(lambda y: y ** p, Y)), 1/p)
    )


def rgRolesFairness(X, Y, fMask, sMask, g, tWeight, dWeight, hWeight):
    # count g-RoleFairness with role weights
    fRoles = [0] * 3
    sRoles = [0] * 3
    for i, role in enumerate(fMask):
        fRoles[role] += X[i]
    for i, role in enumerate(sMask):
        sRoles[role] += Y[i]
    return abs(
        pow(
            (
                (
                    (abs(fRoles[0] - sRoles[0]) * tWeight) ** g +
                    (abs(fRoles[1] - sRoles[1]) * dWeight) ** g +
                    (abs(fRoles[2] - sRoles[2]) * hWeight) ** g
                ) / 3
            ),
            1/g
        )
    )


# 0 - closest
def vqUniformity(X, Y, q):
    # count q-uniformity of the game
    # Z = X + Y - all players
    Z = X + Y
    muz = sum(Z) / len(Z)
    return abs(
        pow(sum(map(lambda x: abs(x - muz) ** q, X)) / len(X), 1/q) -
        pow(sum(map(lambda y: abs(y - muz) ** q, Y)) / len(Y), 1/q)
    )


def teamRolePriority(fPlayers, sPlayers, fMask, sMask):
    Points = 40
    for i, role in enumerate(fMask):
        Points -= fPlayers[i].rolePriorityPoints(role)
    for i, role in enumerate(sMask):
        Points -= sPlayers[i].rolePriorityPoints(role)
    return Points


def calcNormalize(X, Y):
    alpha = 1
    p = 2
    q = 2
    return (
            alpha * dpFairness(X, Y, p) +
            # beta * rgRolesFairness(X, Y, fMask, sMask, p, tWeight, dWeight, hWeight) +
            vqUniformity(X, Y, q)
    )


def calcRoles(fMask, sMask, fPlayers, sPlayers):
    gamma = 1000
    return gamma * teamRolePriority(fPlayers, sPlayers, fMask, sMask)


def imbalanceFunc(X, Y, fMask, sMask, fPlayers, sPlayers):
    # const init
    alpha = 1
    gamma = 1000
    p = 2
    q = 2
    return (
            alpha * dpFairness(X, Y, p) +
            # beta * rgRolesFairness(X, Y, fMask, sMask, p, tWeight, dWeight, hWeight) +
            gamma * teamRolePriority(fPlayers, sPlayers, fMask, sMask) +
            vqUniformity(X, Y, q)
    )


# class Role:
#     SR = 0
#     tag = ""
#     index = -1
#     active = False
#
#     def __init__(self, SR, tag, index, priority):
#         self.SR = SR
#         self.tag = tag
#         self.index = index
#         self.priority = priority
#
#     def activate(self):
#         self.active = True
#
#     def checkRole(self, role):
#         if self.index == role or self.tag == role:
#             return True
#         else:
#             return False


class ClassPlayer:
    Roles = ""
    Flex = False

    def __init__(self, SR):
        self.SR = SR

    def setRoles(self, R, Flex):
        self.Roles = R
        self.Flex = Flex

    # def roleList(self):
    #     return [self.TankSR, self.DpsSR, self.HealSR]
    #
    # def selectRoles(self, R):
    #     for selector in R:
    #         if self.TankSR.index == selector or self.TankSR.tag == selector:
    #             self.TankSR.activate()
    #         elif self.DpsSR.index == selector or self.DpsSR.tag == selector:
    #             self.DpsSR.activate()
    #         elif self.HealSR.index == selector or self.HealSR.tag == selector:
    #             self.HealSR.activate()
    #
    # def checkRole(self, R):
    #     if self.TankSR.index == R or self.TankSR.tag == R:
    #         return True
    #     elif self.DpsSR.index == R or self.DpsSR.tag == R:
    #         return True
    #     elif self.HealSR.index == R or self.HealSR.tag == R:
    #         return True
    #     else:
    #         return False
    #
    # def getRoleSR(self, R):
    #     if self.TankSR.index == R or self.TankSR.tag == R:
    #         return self.TankSR
    #     elif self.DpsSR.index == R or self.DpsSR.tag == R:
    #         return self.DpsSR
    #     elif self.HealSR.index == R or self.HealSR.tag == R:
    #         return self.HealSR

    def rolePriorityPoints(self, R):
        R = "S" if R == 0 else "I" if R == 1 else "C" if R == 2 else "D" if R == 3 else R
        return (4 - self.Roles.index(R)) if not self.Flex else 4


class ClassGameBalance:
    result = 1e9
    rawSR = 1e9
    rawRoles = 1e9
    fMask = []
    sMask = []

    def __eq__(self, other):
        if self.rawSR == other.rawSR:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.rawSR < other.rawSR:
            return True
        else:
            return False

    def __init__(self, X, Y):
        # self.fMask = m1
        # self.sMask = m2
        self.fTeamSR = []
        self.sTeamSR = []
        self.fPlayers = X
        self.sPlayers = Y
        for x in X:
            self.fTeamSR.append(x.SR)
        for y in Y:
            self.sTeamSR.append(y.SR)

    def selectMask(self, m1, m2):
        self.fMask = m1
        self.sMask = m2

    def calcResult(self):
        self.result = imbalanceFunc(self.fTeamSR, self.sTeamSR, self.fMask, self.sMask, self.fPlayers, self.sPlayers)
        return self.result

    def calcSR(self):
        self.rawSR = calcNormalize(self.fTeamSR, self.sTeamSR)
        return self.rawSR

    def calcRoles(self):
        self.rawRoles = calcRoles(self.fMask, self.sMask, self.fPlayers, self.sPlayers)
        return self.rawRoles

    def __str__(self):
        return ", ".join([str(i) for i in self.fTeamSR]) + " - " + ", ".join([str(i) for i in self.sTeamSR])
