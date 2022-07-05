# **[Balancer](https://owbalancer.ddns.net)** user guide
## Manage Workspace
____
## Create Players
<img src="https://user-images.githubusercontent.com/63819958/176691488-d7badc02-ad4c-4369-a798-15d73e2242e0.png" align="left" height=auto width="200" />

After selecting workspace you can add new players in small menu on the top.
Than player will appear in the bottom of players menu.
##
You can also edit player nicknames or delete players / customs by rcl on players name in the list

<img src="https://user-images.githubusercontent.com/63819958/177334323-a39c61cf-4ce9-4bad-bfde-65dbfca0b56b.png" align="left" height=auto width="600" />
<br clear="left"/>

____
## Manage Customs
P.S - Customs are "profiles" of players created by different users. You can use other users's customs, but you can't edit not your own custom. 
Depending on the settings of the workspace (custom system), there can be 2 options for working with custom:
* if "noCustom" setting is ON in the workspace, then custom will not be used and all players will be shared between different users
* else there is a menu when you trying to add player to lobby:

  ![image](https://user-images.githubusercontent.com/63819958/176694147-0c00ba1c-3a61-45a8-8cf7-4c697bb9037c.png)
  
  Here you can select which one of the customs you want to add into the lobby.
  Your own custom is highlighted with green.
____
## Manage Lobby
- [ ] Update this section after implementing general lobby feature into the frontline

____
## Balance Lobby
<img src="https://user-images.githubusercontent.com/63819958/176712007-93801e29-1699-4b24-b6f9-5ab318db13e6.png" align="right" height=auto width="500px" />
When lobby is filled u should click on "Balance teams" button on the bottom

This may take some time due to a lot of calculations or server load
<br clear="right"/>
##
<img src="https://user-images.githubusercontent.com/63819958/176713245-d104b760-a5cb-4421-8e01-b66c45172157.png" align="right" height=auto width="500px" />
Then after loading you will get balance.

You can scroll through the balance options to find the best one. And you can also swap players manually by drag n drop system.

<br clear="right"/>

____
## Settings
<img src="https://user-images.githubusercontent.com/63819958/177350191-cab567e3-1074-4b81-8200-9a7b2b291da7.png" align="right" height=auto width="200px" />

You can get access to user settings by clicking onto nickname in right top corner and click `settings`
<br clear="right"/>

##
<img src="https://user-images.githubusercontent.com/63819958/177349956-c6d1ff8c-3ea4-4ba6-b773-74851bf405d8.png" align="right" height=auto width="500px" />

Here you can edit decoration settings and balancer math coefficients (more about math __here__)
<br clear="right"/>

____
# Math
Balance list is sorted by analyzing each of the balances using the mathematical formulas described below (hereinafter simply `evaluation`)

let:

<p align="center">
  X - list of players in team A<br>
  Y - list of players in team B<br>
</p>
then:

$$s_p(X) = \left( \sum_{x\in X} sr_x \right)^{1/p}$$
$$d(X, Y) = |\s_p(X)|$$

