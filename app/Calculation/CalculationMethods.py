# 0 - closest
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

