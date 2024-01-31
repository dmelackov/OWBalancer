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
    
    prev_gamedata = ""
    prev_gamestatic = ""
    prev_score = ""
    for game in Games.getByWorkspace(W):
        
        if prev_gamedata == game.GameData and prev_gamestatic == game.GameStatic and f"{game.FirstTeamPoints}, {game.SecondTeamPoints}" == prev_score:
            continue
        
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
        prev_gamedata = game.GameData
        prev_gamestatic = game.GameStatic
        prev_score = f"{game.FirstTeamPoints}, {game.SecondTeamPoints}"
        tttMatches.append([team1, team2])
    
    gausian_instances: dict[str, GausianPlayer] = {}
    
    for agent in agents:
        P = Player.getInstance(int(agent.split("-")[0]))
        GP = GausianPlayer.getInstance(P, agent.split("-")[1])
        if GP is None:
            GP = GausianPlayer.create(player=P, role=agent.split("-")[1], mu=last_rating[agent] / 100, sigma=DEFAULT_SIGMA, beta=DEFAULT_BETA, gamma=DEFAULT_GAMMA)
            gausian_instances[agent] = GP
        else:
            gausian_instances[agent] = GP
        priors[agent] = TTTPlayer(Gaussian(last_rating[agent] / 100, DEFAULT_SIGMA), DEFAULT_BETA, DEFAULT_GAMMA)
    
    h = History(tttMatches, results=results, times=dates, priors=priors, p_draw=0.1)
    h.convergence(iterations=100)
    lc = h.learning_curves()
    
    agent_customs: list[Custom] = []
    
    for k, v in lc.items():
        GP = gausian_instances[k]
        GP.mu = v[-1][1].mu
        GP.sigma = v[-1][1].sigma
        GP.save()
        C = Custom.get_byPlayerAndWorkspace(GP.player, WP)
    
        
        if C is None:
            C = Custom.create(WP, GP.player).data
        agent_customs.append(C)
        
        
        if GP.role == "tank":
            C.TSR = GP.mu * 100
        elif GP.role == "dps":
            C.DSR = GP.mu * 100
        else:
            C.HSR = GP.mu * 100
        C.save()
    
    for custom in agent_customs:
        if custom.TSR != 0 and custom.DSR != 0 and custom.HSR != 0:
            continue
        customs = Custom.get_byPlayer(custom.Player.ID).data
        TSR_count = 0
        HSR_count = 0
        DSR_count = 0
        
        TSR_sum = 0
        HSR_sum = 0
        DSR_sum = 0
        
        for i in customs:
            if i.Creator == WP:
                continue
            if i.TSR != 0:
                TSR_count += 1
                TSR_sum += i.TSR
            if i.DSR != 0:
                DSR_count += 1
                DSR_sum += i.DSR
            if i.TSR != 0:
                HSR_count += 1
                HSR_sum += i.HSR
        
        if custom.TSR == 0 and TSR_count:
            custom.TSR = TSR_sum / TSR_count
        if custom.DSR == 0 and DSR_count:
            custom.DSR = DSR_sum / DSR_count
        if custom.HSR == 0 and HSR_count:
            custom.HSR = HSR_sum / HSR_count
        custom.save()