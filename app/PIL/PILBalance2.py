from PIL import Image, ImageDraw, ImageFont
from app.Static.globalClasses import *

RBronse = Image.open("app/icons/PIL2/Rank/RBronse.png").resize((80, 80))
RSilver = Image.open("app/icons/PIL2/Rank/RSilver.png").resize((80, 80))
RGold = Image.open("app/icons/PIL2/Rank/RGold.png").resize((80, 80))
RPlatinum = Image.open("app/icons/PIL2/Rank/RPlatinum.png").resize((80, 80))
RDiamond = Image.open("app/icons/PIL2/Rank/RDiamond.png").resize((80, 80))
RMaster = Image.open("app/icons/PIL2/Rank/RMaster.png").resize((80, 80))
RGm = Image.open("app/icons/PIL2/Rank/RGm.png").resize((80, 80))

BBronse = Image.open("app/icons/PIL2/Rank/BBronse.png").resize((80, 80))
BSilver = Image.open("app/icons/PIL2/Rank/BSilver.png").resize((80, 80))
BGold = Image.open("app/icons/PIL2/Rank/BGold.png").resize((80, 80))
BPlatinum = Image.open("app/icons/PIL2/Rank/BPlatinum.png").resize((80, 80))
BDiamond = Image.open("app/icons/PIL2/Rank/BDiamond.png").resize((80, 80))
BMaster = Image.open("app/icons/PIL2/Rank/BMaster.png").resize((80, 80))
BGm = Image.open("app/icons/PIL2/Rank/BGm.png").resize((80, 80))

team_font = ImageFont.truetype("app/icons/font.ttf", 84)
vs_font = ImageFont.truetype("app/icons/VS_font.otf", 84)
avg_font = ImageFont.truetype("app/icons/font.ttf", 42)
text_font = ImageFont.truetype("app/icons/font.ttf", 68)
text_ranknum = ImageFont.truetype("app/icons/font.ttf", 28)

bheal_icon = Image.open("app/icons/PIL2/Roles/bheal_icon2.png").resize((80, 80))
bdps_icon = Image.open("app/icons/PIL2/Roles/bdps_icon2.png").resize((80, 80))
btank_icon = Image.open("app/icons/PIL2/Roles/btank_icon2.png").resize((80, 80))

rheal_icon = Image.open("app/icons/PIL2/Roles/rheal_icon2.png").resize((80, 80))
rdps_icon = Image.open("app/icons/PIL2/Roles/rdps_icon2.png").resize((80, 80))
rtank_icon = Image.open("app/icons/PIL2/Roles/rtank_icon2.png").resize((80, 80))

gheal_icon = Image.open("app/icons/PIL1/Roles/GrayHeal.png")
gdps_icon = Image.open("app/icons/PIL1/Roles/GrayDps.png")
gtank_icon = Image.open("app/icons/PIL1/Roles/GrayTank.png")

sword = Image.open("app/icons/PIL2/sword.png").resize((100, 100))

wheal_icon = Image.open("app/icons/PIL1/Roles/heal_icon.png").resize((60, 60))
wdps_icon = Image.open("app/icons/PIL1/Roles/dps_icon.png").resize((60, 60))
wtank_icon = Image.open("app/icons/PIL1/Roles/tank_icon.png").resize((60, 60))
wflex = Image.open("app/icons/PIL1/Roles/flex.png").resize((60, 60))
role_font = ImageFont.truetype("app/icons/font.ttf", 84)
percent_font = ImageFont.truetype("app/icons/font.ttf", 30)


def get_rank_icon(rank, team):
    rank = int(rank)
    if rank < 1500:
        return RBronse if team else BBronse
    elif 1500 <= rank < 2000:
        return RSilver if team else BSilver
    elif 2000 <= rank < 2500:
        return RGold if team else BGold
    elif 2500 <= rank < 3000:
        return RPlatinum if team else BPlatinum
    elif 3000 <= rank < 3500:
        return RDiamond if team else BDiamond
    elif 3500 <= rank < 4000:
        return RMaster if team else BMaster
    else:
        return RGm if team else BGm


def roles_priority(M, image, width, k, pl, left_padding):
    roles = M.Roles
    pl = pl * 93
    s_roles = roles[1:]
    ico = None
    if M.isFlex:
        ico = wflex
    elif roles[0] == 0:
        ico = wtank_icon
    elif roles[0] == 1:
        ico = wdps_icon
    elif roles[0] == 2:
        ico = wheal_icon
    if ico:
        image.paste(ico, (width // 2 - 160 + left_padding, 275 + k + pl), mask=ico)

    if not M.isFlex:
        for r in range(len(s_roles)):
            ico = None
            if s_roles[r] == 0:
                ico = gtank_icon.resize((40, 40))
            elif s_roles[r] == 1:
                ico = gdps_icon.resize((40, 40))
            elif s_roles[r] == 2:
                ico = gheal_icon.resize((40, 40))
            if ico:
                image.paste(ico, (width // 2 - 200 - (r * 40) + left_padding, 295 + k + pl))


def foo(draw, width, image, text_role, color, k, icon, Ms, RoleID, team):
    if len(Ms):
        left_padding = width // 2 + 50 if team else 0
        draw.text((150 + left_padding, 160 + k), text_role, font=role_font, fill=color)
        # draw.line((150, 254 + k, 367, 254 + k), fill=color, width=6)

        draw.line((30 + left_padding, 164 + k, 109 + left_padding, 164 + k), fill=color, width=10)
        image.paste(icon, (30 + left_padding, 170 + k))
        draw.line((30 + left_padding, 254 + k, 109 + left_padding, 254 + k), fill=color, width=10)

        for i, M in enumerate(Ms):
            p = i * 93
            top_padding = p + k
            rank_icon = get_rank_icon(M.Rating[RoleID], team)
            image.paste(rank_icon, (30 + left_padding, 260 + top_padding), mask=rank_icon)
            draw.text((38 + left_padding, 320 + top_padding), str(M.Rating[RoleID]), font=text_ranknum)
            draw.text((150 + left_padding, 270 + top_padding), M.Name, font=text_font)
            roles_priority(M, image, width, k, i, left_padding)
        return k + (len(Ms) * 93 + 114)
    return k


def createImage(gameData, U):
    width = 1920
    height = 1080
    image = Image.new('RGB', (width, height), '#090C10')
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), "#090C10")
    draw.rectangle((20, 20, width - 20, height - 20), outline="#161b22", width=10)

    draw.rectangle((120, 160, width // 2 - 70, height - 20), fill="#161b22", width=10)
    draw.rectangle((20, 160, 119, height - 20), outline="#1e90ff", width=10)

    draw.rectangle((width // 2 + 170, 160, width - 20, height - 20), fill="#161b22", width=10)
    draw.rectangle((width // 2 + 70, 160, width // 2 + 169, height - 20), outline="#ff6347", width=10)

    image.paste(sword, (width // 2 - 50, 560), mask=sword)

    # название команд и AVG
    USettings = U.getUserSettings()
    draw.text((40, 20), USettings["TeamNames"]["1"], font=team_font)
    draw.text((40, 110), f"AVG: {gameData['first']['AVG']}", font=avg_font)

    team2 = USettings["TeamNames"]["2"]
    avg2 = f"AVG: {gameData['second']['AVG']}"
    wt, ht = team_font.getsize(team2)
    wa, ha = avg_font.getsize(avg2)
    draw.text((width - 40 - wt, 20), team2, font=team_font)
    draw.text((width - 40 - wa, 110), avg2, font=avg_font)

    TDiff = f"Evaluation: {gameData['pareTeamAVG']}"
    w, h = avg_font.getsize(TDiff)
    draw.text((width // 2 - w // 2, 30), TDiff, font=avg_font, fill="#46494D")

    # предсказание победителя

    if len(gameData["second"]["0"]) == len(gameData["second"]["1"]) == len(gameData["second"]["2"]) == 2:
        if gameData["NeuroPredict"] > 13.4:
            percent_color = "#ff6347"
        elif gameData["NeuroPredict"] < -13.4:
            percent_color = "#1e90ff"
        else:
            percent_color = "#505459"
        prediction = int(gameData["NeuroPredict"] * 5.2) + 960
        draw.line((prediction, 120, prediction, 140), fill=percent_color, width=8)
        percent = str(gameData["NeuroPredict"]) + "%"
        w, h = percent_font.getsize(percent)
        draw.text((prediction - w // 2, 115 - h), percent, font=percent_font, fill=percent_color)

        draw.line((width // 2 + 70, 140, 1450, 140), fill="#ff6347", width=10)
        draw.line((1450, 120, 1450, 145), fill="#ff6347", width=10)
        draw.text((1460, 115), "100%", font=percent_font, fill="#ff6347")

        draw.line((width // 2 - 70, 141, 470, 141), fill="#1e90ff", width=10)
        draw.line((470, 120, 470, 145), fill="#1e90ff", width=10)
        w, h = percent_font.getsize("-100%")
        draw.text((460 - w, 115), "-100%", font=percent_font, fill="#1e90ff")

        draw.line((width // 2 - 69, 140, width // 2 + 69, 140), fill="#505459", width=10)

    # баланс
    RedColor = "#ff6347"
    BlueColor = "#1e90ff"
    k = 0
    for i in range(3):
        role_name = None
        role_icon = None
        if i == 0:
            role_name = "Tanks"
            role_icon = btank_icon
        elif i == 1:
            role_name = "Dps"
            role_icon = bdps_icon
        elif i == 2:
            role_name = "Healers"
            role_icon = bheal_icon
        Ms = []
        for j in gameData['first'][str(i)]:
            Ms.append(Member(j))
        k = foo(draw, width, image, role_name, BlueColor, k, role_icon, Ms, i, 0)

    k = 0
    for i in range(3):
        role_name = None
        role_icon = None
        if i == 0:
            role_name = "Tanks"
            role_icon = rtank_icon
        elif i == 1:
            role_name = "Dps"
            role_icon = rdps_icon
        elif i == 2:
            role_name = "Healers"
            role_icon = rheal_icon
        Ms = []
        for j in gameData['second'][str(i)]:
            Ms.append(Member(j))
        k = foo(draw, width, image, role_name, RedColor, k, role_icon, Ms, i, 1)
    return image


# if __name__ == '__main__':
#     d = {'pareTeamAVG': 0,
#          'NeuroPredict': -15,
#          'first': {
#              'AVG': 0,
#              'RolePoints': 16,
#              '0': [
#                  {'C': 5, 'Roles': [0, 2, 1], 'isFlex': False, 'P': 5, 'Rating': [0, 0, 0]},
#                  {'C': 6, 'Roles': [0, 2], 'isFlex': False, 'P': 6, 'Rating': [0, 0, 0]}
#              ], '1': [
#                  {'C': 9, 'Roles': [1, 2, 0], 'isFlex': False, 'P': 9, 'Rating': [0, 0, 0]},
#                  {'C': 12, 'Roles': [1, 0], 'isFlex': False, 'P': 12, 'Rating': [0, 0, 0]}
#              ], '2': [
#                  {'C': 1, 'Roles': [0, 2, 1], 'isFlex': False, 'P': 1, 'Rating': [0, 0, 0]},
#                  {'C': 8, 'Roles': [0, 2, 1], 'isFlex': False, 'P': 8, 'Rating': [0, 0, 0]}
#              ]
#          }, 'second': {
#             'AVG': 0,
#             'RolePoints': 18,
#             '0': [
#                 {'C': 4, 'Roles': [0, 2, 1], 'isFlex': False, 'P': 4, 'Rating': [0, 0, 0]},
#                 {'C': 11, 'Roles': [0], 'isFlex': False, 'P': 11, 'Rating': [0, 0, 0]}
#             ], '1': [
#                 {'C': 2, 'Roles': [1], 'isFlex': False, 'P': 2, 'Rating': [0, 0, 0]},
#                 {'C': 3, 'Roles': [0, 2, 1], 'isFlex': True, 'P': 3, 'Rating': [0, 0, 0]}
#             ], '2': [
#                 {'C': 7, 'Roles': [2, 1], 'isFlex': False, 'P': 7, 'Rating': [0, 0, 0]},
#                 {'C': 10, 'Roles': [2, 0], 'isFlex': False, 'P': 10, 'Rating': [0, 0, 0]}
#             ]
#         },
#          'rangeTeam': 0.0}
#
#     img = createImage(d, Profile.select().where(Profile.Username == "Ivarys")[0])
#     img.save('IMAGE.jpg')
