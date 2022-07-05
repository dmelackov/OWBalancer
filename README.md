# **[Balancer](https://owbalancer.ddns.net)** user guide
____
## Manage Workspace
____
## Create Players
After selecting workspace you can add new players in small menu on the top.
Than player will appear in the bottom of players menu. You can also edit player nicknames or delete players / customs in this menu

![image](https://user-images.githubusercontent.com/63819958/176691488-d7badc02-ad4c-4369-a798-15d73e2242e0.png)
![image](https://user-images.githubusercontent.com/63819958/177334323-a39c61cf-4ce9-4bad-bfde-65dbfca0b56b.png)

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

## Balance Lobby
When lobby is filled u should click on "Balance teams" button on the bottom

![image](https://user-images.githubusercontent.com/63819958/176712007-93801e29-1699-4b24-b6f9-5ab318db13e6.png)

Then after loading you will get balance.

![image](https://user-images.githubusercontent.com/63819958/176713245-d104b760-a5cb-4421-8e01-b66c45172157.png)

You can also scroll through the balance options to find the best one. And you can also swap players manually by drag n drop system.

____
## Settings
You can get access to user settings by clicking onto nickname in right top corner and click `settings`

![image](https://user-images.githubusercontent.com/63819958/177350191-cab567e3-1074-4b81-8200-9a7b2b291da7.png)


![image](https://user-images.githubusercontent.com/63819958/177349956-c6d1ff8c-3ea4-4ba6-b773-74851bf405d8.png)

Here you can edit decoration settings and balancer math coefficients (more about math __here__)

____
# Math
Balance list is sorted by analyzing each of the balances using the mathematical formulas described below (hereinafter simply `evaluation`)

let:

```math
\sqrt{3}
```

```math
\sum
X - list of players in team A
Y - list of players in team B
then:
s(X) = \sum_{x\in X} x\in X
```
