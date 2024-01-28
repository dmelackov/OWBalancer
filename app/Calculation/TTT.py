import json
from app.DataBase.db import Custom, Games, GausianPlayer, Player, Profile, Roles, Workspace, WorkspaceProfile
from app.params import TRUESKILL_PASSWORD
from trueskillthroughtime import History, Player as TTTPlayer, Gaussian

DEFAULT_GAMMA = 0.2
DEFAULT_BETA = 1
DEFAULT_SIGMA = 1


def recalculateWorkspace(workspace_id: int):
    P = Profile.getProfile("TrueSkill")
    if P is None:
        P = Profile.create("TrueSkill", TRUESKILL_PASSWORD).data
    W = Workspace.getInstance(workspace_id)
    WP = WorkspaceProfile.getWU(P, W).data
    if WP is None:
        WP = WorkspaceProfile.create(P, W).data
        WP.setRole(Roles.getInstance(4))
        
    tttMatches = []
    agents = []
    results = []
    priors = {}
    dates = []
    last_rating = {}
    
    for game in Games.getByWorkspace(W):
        results.append([game.FirstTeamPoints, game.SecondTeamPoints])
        dates.append(game.Timestamp.timestamp()/(60*60*24))
        
        GameActive = json.loads(game.GameData)
        GameStatic = json.loads(game.GameStatic)
        
        fMaskIndex = 0
        sMaskIndex = 0
        team1 = []
        team2 = []
        
        for i in range(len(GameActive["TeamMask"])):
            C = Custom.getInstance(int(GameStatic[i]["CustomID"]))
            if GameActive["TeamMask"][i] == "0":
                role = int(GameActive["fMask"][fMaskIndex])
                rating = ["TSR", "DSR", "HSR"][role]
                role = ["tank", "dps", "support"][role]
                team1.append(f"{C.Player.ID}-{role}")
                last_rating[f"{C.Player.ID}-{role}"] = GameStatic[i][rating]
                agents.append(f"{C.Player.ID}-{role}")
                fMaskIndex += 1
            else:
                role = int(GameActive["sMask"][sMaskIndex])
                rating = ["TSR", "DSR", "HSR"][role]
                role = ["tank", "dps", "support"][role]
                team2.append(f"{C.Player.ID}-{role}")
                last_rating[f"{C.Player.ID}-{role}"] = GameStatic[i][rating]
                agents.append(f"{C.Player.ID}-{role}")
                sMaskIndex += 1

        tttMatches.append([team1, team2])
    
    gausian_instances: dict[str, GausianPlayer] = {}
    
    for agent in agents:
        P = Player.getInstance(int(agent.split("-")[0]))
        GP = GausianPlayer.getInstance(P, agent.split("-")[1])
        if GP is None:
            GP = GausianPlayer.create(player=P, role=agent.split("-")[1], mu=last_rating[agent] / 100, sigma=DEFAULT_SIGMA, beta=DEFAULT_BETA, gamma=DEFAULT_GAMMA)
            gausian_instances[agent] = GP
            prior = TTTPlayer(Gaussian(last_rating[agent] / 100, DEFAULT_SIGMA), DEFAULT_BETA, DEFAULT_GAMMA)
        else:
            gausian_instances[agent] = GP
            prior = TTTPlayer(Gaussian(GP.mu, GP.sigma), GP.beta, GP.gamma)
        priors[agent] = prior
    
    h = History(tttMatches, results=results, times=dates, priors=priors, p_draw=0.1)
    h.convergence(iterations=100)
    lc = h.learning_curves()
    
    
    for k, v in lc.items():
        GP = gausian_instances[k]
        GP.mu = v[-1][1].mu
        GP.sigma = v[-1][1].sigma
        GP.save()
        C = Custom.get_byPlayerAndWorkspace(GP.player, WP)
        if C is None:
            C = Custom.create(WP, GP.player).data
        if GP.role == "tank":
            C.TSR = GP.mu * 100
        elif GP.role == "dps":
            C.DSR = GP.mu * 100
        else:
            C.HSR = GP.mu * 100
        C.save()