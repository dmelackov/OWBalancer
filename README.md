# **[Balancer](https://owbalancer.ddns.net)** user guide
# <a name="Contents">Contents</a>
- <h2 src="#manage-Workspace">Workspace</h2>

## Manage Workspace


[Back](#Contents)
____
## <a name="Players">Create Players</a> 

<img src="https://user-images.githubusercontent.com/63819958/176691488-d7badc02-ad4c-4369-a798-15d73e2242e0.png" align="left" height=auto width="200" />

After selecting workspace you can add new players in small menu on the top.
Than player will appear in the bottom of players menu.
##
You can also edit player nicknames or delete players / customs by rcl on players name in the list

<img src="https://user-images.githubusercontent.com/63819958/177334323-a39c61cf-4ce9-4bad-bfde-65dbfca0b56b.png" align="left" height=auto width="600" />
<br clear="left"/>

[Back](#Contents)
____
## Manage Customs
<a name="Customs"></a>
P.S - Customs are "profiles" of players created by different users. You can use other users's customs, but you can't edit not your own custom. 
Depending on the settings of the workspace (custom system), there can be 2 options for working with custom:
* if "noCustom" setting is ON in the workspace, then custom will not be used and all players will be shared between different users
* else there is a menu when you trying to add player to lobby:

  ![image](https://user-images.githubusercontent.com/63819958/176694147-0c00ba1c-3a61-45a8-8cf7-4c697bb9037c.png)
  
  Here you can select which one of the customs you want to add into the lobby.
  Your own custom is highlighted with green.
  
[Back](#Contents)
____
## Manage Lobby
<a name="Lobby"></a>
- [ ] Update this section after implementing general lobby feature into the frontline

[Back](#Contents)
____
## Balance Lobby
<a name="Balance"></a>
<img src="https://user-images.githubusercontent.com/63819958/176712007-93801e29-1699-4b24-b6f9-5ab318db13e6.png" align="right" height=auto width="500px" />
When lobby is filled u should click on "Balance teams" button on the bottom

This may take some time due to a lot of calculations or server load
<br clear="right"/>
##
<img src="https://user-images.githubusercontent.com/63819958/176713245-d104b760-a5cb-4421-8e01-b66c45172157.png" align="right" height=auto width="500px" />
Then after loading you will get balance.

You can scroll through the balance options to find the best one. And you can also swap players manually by drag n drop system.

<br clear="right"/>

[Back](#Contents)
____
## Settings
<a name="Settings"></a>
<img src="https://user-images.githubusercontent.com/63819958/177350191-cab567e3-1074-4b81-8200-9a7b2b291da7.png" align="right" height=auto width="200px" />

You can get access to user settings by clicking onto nickname in right top corner and click `settings`
<br clear="right"/>

##
<img src="https://user-images.githubusercontent.com/63819958/177349956-c6d1ff8c-3ea4-4ba6-b773-74851bf405d8.png" align="right" height=auto width="500px" />

Here you can edit decoration settings and balancer math coefficients (more about math [__here__](#Math))
* Custom Autochoice - let you automaticly select your own custom while adding people into lobby
* Extended Lobby - let you add additional people into lobby. When balance it will pick random players to generate balance
* Extended Result - shows you additional information on balance image (Uniformity and Fairness)
* Autoincrement - Not realised yet
<br clear="right"/>

[Back](#Contents)
____
# Math
<a name="Math"></a>
Balance list is sorted by analyzing each of the balances using the mathematical formulas described below (hereinafter simply `evaluation`)

let:

<p align="center">
  X - list of players in team A<br>
  Y - list of players in team B<br>
  Z - list of player for both teams A and B
</p>
then:

$$s_p(X) = \left( \sum_{x\in X} sr_x^p \right)^{1/p}$$

$$dpFairness(X, Y) = |s_p(X) - s_p(Y)| = \left|\left( \sum_{x\in X} sr_x^p \right)^{1/p} - \left( \sum_{y\in Y} sr_y^p \right)^{1/p}\right|$$
##
$$r_p(Role) = \left(\left|\sum_{{Role_x}\in X} sr_{Role_x} - \sum_{{Role_y}\in Y} sr_{Role_y}\right| * roleWeight\right) ^ p$$

$$
dpRoleFairness(X, Y) = \left|\left(
r_p(Tank) + r_p(Dps) + r_p(Support) \over 3
\right)^{1/p}\right|
$$
##
$$MU_z = {\sum_{z\in Z} sr_z \over len_Z}$$

$$vqUniformity(X, Y) = \left|
\left({\sum_{x\in X} |x-MU_z|^q \over len_X}\right)^{1/q} - \left({\sum_{y\in Y} |y-MU_z|^q \over len_Y}\right)^{1/q}
\right|$$
##
<p align="center"># evaluation</p>

$$ImbalanceFunc(X, Y) = \alpha * dpFairness(X, Y) + \beta * dpRoleFairness(X, Y) + \gamma * RolePriorityPoints + vqUniformity(X, Y)$$
##
All coefficients can be changed on the settings page according to this list:
<p align="center">
  alpha - LinearFairnessCoef<br>
  beta - LinearRolesCoef<br>
  gamma - OffrolesPenalty<br>
  p - FairnessPowerApproximation<br>
  q - UnifomityPowerApproximation<br>
  tWeight - TankMultiplier<br>
  hWeight - HealMultiplier<br>
  dWeight - DpsMultiplier
</p>

On the balance result you can see $Evaluation = ImbalaceFunc(X, Y)$, $Fairness = \alpha * dpFairness(X, Y) + \beta * dpRoleFairness(X, Y)$ and $Uniformity = vqUniformity(X, Y)$

[Back](#Contents)
