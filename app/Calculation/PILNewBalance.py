from PIL import Image, ImageDraw, ImageFont
from app.DataBase.db import Custom

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

team_font = ImageFont.truetype("app/Calculation/font.ttf", 84)
vs_font = ImageFont.truetype("app/Calculation/VS_font.otf", 84)
avg_font = ImageFont.truetype("app/Calculation/font.ttf", 42)
text_font = ImageFont.truetype("app/Calculation/font.ttf", 68)
text_ranknum = ImageFont.truetype("app/Calculation/font.ttf", 28)

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
role_font = ImageFont.truetype("app/Calculation/font.ttf", 84)
percent_font = ImageFont.truetype("app/Calculation/font.ttf", 30)


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


def roles_priority(P, image, width, k, pl, left_padding):
    roles = P.Roles
    pl = pl * 93
    s_roles = roles[1:]
    if P.isFlex:
        image.paste(wflex, (width // 2 - 160 + left_padding, 275 + k + pl), mask=wflex)
    elif roles[0] == "T":
        image.paste(wtank_icon, (width // 2 - 160 + left_padding, 275 + k + pl), mask=wtank_icon)
    elif roles[0] == "D":
        image.paste(wdps_icon, (width // 2 - 160 + left_padding, 275 + k + pl), mask=wdps_icon)
    elif roles[0] == "H":
        image.paste(wheal_icon, (width // 2 - 160 + left_padding, 275 + k + pl), mask=wheal_icon)

    if not P.isFlex:
        for r in range(len(s_roles)):
            if s_roles[r] == "T":
                image.paste(gtank_icon.resize((40, 40)), (width // 2 - 200 - (r * 40) + left_padding, 295 + k + pl))
            elif s_roles[r] == "D":
                image.paste(gdps_icon.resize((40, 40)), (width // 2 - 200 - (r * 40) + left_padding, 295 + k + pl))
            elif s_roles[r] == "H":
                image.paste(gheal_icon.resize((40, 40)), (width // 2 - 200 - (r * 40) + left_padding, 295 + k + pl))


def foo(draw, width, image, text_role, color, k, icon, Cs, Ranks, team):
    if len(Cs):
        left_padding = width // 2 + 50 if team else 0
        draw.text((150 + left_padding, 160 + k), text_role, font=role_font, fill=color)
        # draw.line((150, 254 + k, 367, 254 + k), fill=color, width=6)

        draw.line((30 + left_padding, 164 + k, 109 + left_padding, 164 + k), fill=color, width=10)
        image.paste(icon, (30 + left_padding, 170 + k))
        draw.line((30 + left_padding, 254 + k, 109 + left_padding, 254 + k), fill=color, width=10)

        for i, C in enumerate(Cs):
            p = i * 93
            top_padding = p + k
            rank_icon = get_rank_icon(Ranks[i], team)
            image.paste(rank_icon, (30 + left_padding, 260 + top_padding), mask=rank_icon)
            draw.text((38 + left_padding, 320 + top_padding), Ranks[i], font=text_ranknum)
            draw.text((150 + left_padding, 270 + top_padding), C.Player.Username, font=text_font)
            roles_priority(C.Player, image, width, k, i, left_padding)
        return k + (len(Cs) * 93 + 114)
    return k


def createImage(d):
    width = 1980
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
    draw.text((40, 20), "Team 1", font=team_font)
    draw.text((40, 110), f"AVG: {d['first']['AVG']}", font=avg_font)

    team2 = "Team 2"
    avg2 = f"AVG: {d['second']['AVG']}"
    wt, ht = team_font.getsize(team2)
    wa, ha = avg_font.getsize(avg2)
    draw.text((width - 40 - wt, 20), team2, font=team_font)
    draw.text((width - 40 - wa, 110), avg2, font=avg_font)

    TDiff = f"Evaluation: {d['pareTeamAVG']}"
    w, h = avg_font.getsize(TDiff)
    draw.text((width // 2 - w // 2, 30), TDiff, font=avg_font)

    # предсказание победителя
    if d["rangeTeam"] / 10 > 13.4:
        percent_color = "#ff6347"
    elif d["rangeTeam"] / 10 < -13.4:
        percent_color = "#1e90ff"
    else:
        percent_color = "#505459"
    prediction = int(d["rangeTeam"] / 10 * 5.2) + 990
    draw.line((prediction, 120, prediction, 140), fill=percent_color, width=8)
    percent = str(d["rangeTeam"] / 10)
    w, h = percent_font.getsize(percent)
    draw.text((prediction - w // 2, 115 - h), percent, font=percent_font, fill=percent_color)

    draw.line((width // 2 + 70, 140, 1510, 140), fill="#ff6347", width=10)
    draw.line((1510, 120, 1510, 145), fill="#ff6347", width=10)
    draw.text((1520, 115), "100", font=percent_font, fill="#ff6347")

    draw.line((width // 2 - 70, 141, 470, 141), fill="#1e90ff", width=10)
    draw.line((470, 120, 470, 145), fill="#1e90ff", width=10)
    w, h = percent_font.getsize("-100")
    draw.text((460 - w, 115), "-100", font=percent_font, fill="#1e90ff")

    draw.line((width // 2 - 69, 140, width // 2 + 69, 140), fill="#505459", width=10)

    # баланс
    RedColor = "#ff6347"
    BlueColor = "#1e90ff"
    Cs = Custom.select().where(Custom.ID << d['first']['0'])
    Ranks = []
    k = 0
    for C in Cs:
        Ranks.append(str(C.TSR))
    if len(Cs) == len(d['first']['0']):
        k = foo(draw, width, image, "Tanks", BlueColor, k, btank_icon, Cs, Ranks, 0)

    Cs = Custom.select().where(Custom.ID << d['first']['1'])
    Ranks = []
    for C in Cs:
        Ranks.append(str(C.DSR))
    if len(Cs) == len(d['first']['1']):
        k = foo(draw, width, image, "Dps", BlueColor, k, bdps_icon, Cs, Ranks, 0)

    Cs = Custom.select().where(Custom.ID << d['first']['2'])
    Ranks = []
    for C in Cs:
        Ranks.append(str(C.HSR))
    if len(Cs) == len(d['first']['2']):
        foo(draw, width, image, "Healers", BlueColor, k, bheal_icon, Cs, Ranks, 0)

    k = 0
    Cs = Custom.select().where(Custom.ID << d['second']['0'])
    Ranks = []
    for C in Cs:
        Ranks.append(str(C.TSR))
    if len(Cs) == len(d['second']['0']):
        k = foo(draw, width, image, "Tanks", RedColor, k, rtank_icon, Cs, Ranks, 1)

    Cs = Custom.select().where(Custom.ID << d['second']['1'])
    Ranks = []
    for C in Cs:
        Ranks.append(str(C.DSR))
    if len(Cs) == len(d['second']['1']):
        k = foo(draw, width, image, "Dps", RedColor, k, rdps_icon, Cs, Ranks, 1)

    Cs = Custom.select().where(Custom.ID << d['second']['2'])
    Ranks = []
    for C in Cs:
        Ranks.append(str(C.HSR))
    if len(Cs) == len(d['second']['2']):
        foo(draw, width, image, "Healers", RedColor, k, rheal_icon, Cs, Ranks, 1)

    return image


# d = {'pareTeamAVG': 400, 'first': {'AVG': 3066, 'RolePoints': 17, '0': [1, 3], '1': [7, 22], '2': [11, 21]},
#      'second': {'AVG': 3066, 'RolePoints': 17, '0': [6, 8], '1': [9, 10], '2': [4, 5]}, 'rangeTeam': 0}
# img = createImage(d)
# img.save('IMAGE.jpg')
