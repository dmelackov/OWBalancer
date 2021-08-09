from PIL import Image, ImageDraw, ImageFont
from app.DataBase.db import Custom

RBronse = Image.open("app/icons/PIL2/Rank/RBronse.png").resize((60, 60))
RSilver = Image.open("app/icons/PIL2/Rank/RSilver.png").resize((60, 60))
RGold = Image.open("app/icons/PIL2/Rank/RGold.png").resize((60, 60))
RPlatinum = Image.open("app/icons/PIL2/Rank/RPlatinum.png").resize((60, 60))
RDiamond = Image.open("app/icons/PIL2/Rank/RDiamond.png").resize((60, 60))
RMaster = Image.open("app/icons/PIL2/Rank/RMaster.png").resize((60, 60))
RGm = Image.open("app/icons/PIL2/Rank/RGm.png").resize((60, 60))

BBronse = Image.open("app/icons/PIL2/Rank/BBronse.png").resize((60, 60))
BSilver = Image.open("app/icons/PIL2/Rank/BSilver.png").resize((60, 60))
BGold = Image.open("app/icons/PIL2/Rank/BGold.png").resize((60, 60))
BPlatinum = Image.open("app/icons/PIL2/Rank/BPlatinum.png").resize((60, 60))
BDiamond = Image.open("app/icons/PIL2/Rank/BDiamond.png").resize((60, 60))
BMaster = Image.open("app/icons/PIL2/Rank/BMaster.png").resize((60, 60))
BGm = Image.open("app/icons/PIL2/Rank/BGm.png").resize((60, 60))

team_font = ImageFont.truetype("app/Calculation/font.ttf", 96)
vs_font = ImageFont.truetype("app/Calculation/VS_font.otf", 84)
avg_font = ImageFont.truetype("app/Calculation/font.ttf", 48)
text_font = ImageFont.truetype("app/Calculation/font.ttf", 68)
text_ranknum = ImageFont.truetype("app/Calculation/font.ttf", 28)

bheal_icon = Image.open("app/icons/PIL2/Roles/bheal_icon.png").resize((80, 80))
bdps_icon = Image.open("app/icons/PIL2/Roles/bdps_icon.png").resize((80, 80))
btank_icon = Image.open("app/icons/PIL2/Roles/btank_icon.png").resize((80, 80))

rheal_icon = Image.open("app/icons/PIL2/Roles/rheal_icon.png").resize((80, 80))
rdps_icon = Image.open("app/icons/PIL2/Roles/rdps_icon.png").resize((80, 80))
rtank_icon = Image.open("app/icons/PIL2/Roles/rtank_icon.png").resize((80, 80))

gheal_icon = Image.open("app/icons/PIL2/Roles/gheal_icon.png")
gdps_icon = Image.open("app/icons/PIL2/Roles/gdps_icon.png")
gtank_icon = Image.open("app/icons/PIL2/Roles/gtank_icon.png")


wheal_icon = Image.open("app/icons/PIL1/Roles/heal_icon.png").resize((60, 60))
wdps_icon = Image.open("app/icons/PIL1/Roles/dps_icon.png").resize((60, 60))
wtank_icon = Image.open("app/icons/PIL1/Roles/tank_icon.png").resize((60, 60))
wflex = Image.open("app/icons/PIL1/Roles/flex.png").resize((60, 60))
role_font = ImageFont.truetype("app/Calculation/font.ttf", 84)


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
    k = k * 300
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
        image.paste(rank_icon, (40 + left_padding, 270 + top_padding), mask=rank_icon)
        draw.line((150 + left_padding, 345 + top_padding, width // 2 - 100 + left_padding, 345 + top_padding),
                  width=5, fill="#161b22")
        draw.text((38 + left_padding, 315 + top_padding), Ranks[i], font=text_ranknum)
        draw.text((150 + left_padding, 270 + top_padding), C.Player.Username, font=text_font)
        roles_priority(C.Player, image, width, k, i, left_padding)


def createImage(d):
    width = 1980
    height = 1080
    image = Image.new('RGB', (width, height), '#090C10')
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), "#090C10")
    draw.rectangle((20, 20, width // 2 - 70, height - 20), outline="#161b22", width=10)
    draw.rectangle((20, 150, width // 2 - 70, height - 20), outline="#161b22", width=10)
    draw.rectangle((20, 160, 119, height - 20), outline="#1e90ff", width=10)

    draw.rectangle((width // 2 + 70, 20, width - 20, height - 20), outline="#161b22", width=10)
    draw.rectangle((width // 2 + 70, 150, width - 20, height - 20), outline="#161b22", width=10)
    draw.rectangle((width // 2 + 70, 160, width // 2 + 169, height - 20), outline="#ff6347", width=10)

    RedColor = "#ff6347"
    BlueColor = "#1e90ff"
    Cs = Custom.select().where(Custom.ID << d['first']['0'])
    Ranks = []
    for C in Cs:
        Ranks.append(str(C.TSR))
    if len(Cs) == len(d['first']['0']):
        foo(draw, width, image, "Tanks", BlueColor, 0, btank_icon, Cs, Ranks, 0)

    Cs = Custom.select().where(Custom.ID << d['first']['1'])
    Ranks = []
    for C in Cs:
        Ranks.append(str(C.DSR))
    if len(Cs) == len(d['first']['1']):
        foo(draw, width, image, "Dps", BlueColor, 1, bdps_icon, Cs, Ranks, 0)

    Cs = Custom.select().where(Custom.ID << d['first']['2'])
    Ranks = []
    for C in Cs:
        Ranks.append(str(C.HSR))
    if len(Cs) == len(d['first']['2']):
        foo(draw, width, image, "Healers", BlueColor, 2, bheal_icon, Cs, Ranks, 0)

    Cs = Custom.select().where(Custom.ID << d['second']['0'])
    Ranks = []
    for C in Cs:
        Ranks.append(str(C.TSR))
    if len(Cs) == len(d['second']['0']):
        foo(draw, width, image, "Tanks", RedColor, 0, rtank_icon, Cs, Ranks, 1)

    Cs = Custom.select().where(Custom.ID << d['second']['1'])
    Ranks = []
    for C in Cs:
        Ranks.append(str(C.DSR))
    if len(Cs) == len(d['second']['1']):
        foo(draw, width, image, "Dps", RedColor, 1, rdps_icon, Cs, Ranks, 1)

    Cs = Custom.select().where(Custom.ID << d['second']['2'])
    Ranks = []
    for C in Cs:
        Ranks.append(str(C.HSR))
    if len(Cs) == len(d['second']['2']):
        foo(draw, width, image, "Healers", RedColor, 2, rheal_icon, Cs, Ranks, 1)
    return image


d = \
    {'pareTeamAVG': 450, 'first': {'AVG': 2991, 'RolePoints': 17, "0": [7, 15], "1": [9, 10], "2": [11, 14]},
     'second': {'AVG': 2983, 'RolePoints': 17, "0": [4, 8], "1": [1, 6], "2": [5, 13]}}

img = createImage(d)
img.save('IMAGE.png')
