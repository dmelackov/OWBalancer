from PIL import Image, ImageDraw, ImageFont
from app.DataBase.db import Custom
bronse_icon = Image.open("app/icons/bronse.png").resize((80, 80))
silver_icon = Image.open("app/icons/silver.png").resize((80, 80))
gold_icon = Image.open("app/icons/gold.png").resize((80, 80))
plat_icon = Image.open("app/icons/plat.png").resize((80, 80))
diamond_icon = Image.open("app/icons/diamond.png").resize((80, 80))
masters_icon = Image.open("app/icons/masters.png").resize((80, 80))
gm_icon = Image.open("app/icons/gm.png").resize((80, 80))
team_font = ImageFont.truetype("app/Calculation/font.ttf", 96)
vs_font = ImageFont.truetype("app/Calculation/VS_font.otf", 84)
avg_font = ImageFont.truetype("app/Calculation/font.ttf", 48)
text_font = ImageFont.truetype("app/Calculation/font.ttf", 68)
text_ranknum = ImageFont.truetype("app/Calculation/font.ttf", 32)
bheal_icon = Image.open("app/icons/BlueHeal2.png").resize((100, 100))
bdps_icon = Image.open("app/icons/BlueDps2.png").resize((100, 100))
btank_icon = Image.open("app/icons/BlueTank2.png").resize((100, 100))

rheal_icon = Image.open("app/icons/RedHeal2.png").resize((100, 100))
rdps_icon = Image.open("app/icons/RedDps2.png").resize((100, 100))
rtank_icon = Image.open("app/icons/RedTank2.png").resize((100, 100))

gheal_icon = Image.open("app/icons/GrayHeal.png")
gdps_icon = Image.open("app/icons/GrayDps.png")
gtank_icon = Image.open("app/icons/GrayTank.png")


wheal_icon = Image.open("app/icons/heal_icon.png").resize((60, 60))
wdps_icon = Image.open("app/icons/dps_icon.png").resize((60, 60))
wtank_icon = Image.open("app/icons/tank_icon.png").resize((60, 60))


def get_rank_icon(rank):
    if rank < 1500:
        return bronse_icon
    elif 1500 <= rank < 2000:
        return silver_icon
    elif 2000 <= rank < 2500:
        return gold_icon
    elif 2500 <= rank < 3000:
        return plat_icon
    elif 3000 <= rank < 3500:
        return diamond_icon
    elif 3500 <= rank < 4000:
        return masters_icon
    else:
        return gm_icon


def roles_priority_right(P, image, i, width):
    roles = P.Player.Roles
    s_roles = roles[1:]
    if roles[0] == "T":
        image.paste(wtank_icon, (width - 110, 220 + (i * 144)), mask=wtank_icon)
    elif roles[0] == "D":
        image.paste(wdps_icon, (width - 110, 220 + (i * 144)), mask=wdps_icon)
    elif roles[0] == "H":
        image.paste(wheal_icon, (width - 110, 220 + (i * 144)), mask=wheal_icon)

    for r in range(len(s_roles)):
        if s_roles[r] == "T":
            image.paste(gtank_icon.resize((40, 40)), (width - 150 - (r * 40), 240 + (i * 144)))
        elif s_roles[r] == "D":
            image.paste(gdps_icon.resize((40, 40)), (width - 150 - (r * 40), 240 + (i * 144)))
        elif s_roles[r] == "H":
            image.paste(gheal_icon.resize((40, 40)), (width - 150 - (r * 40), 240 + (i * 144)))


def roles_priority_left(P, image, i, width):
    roles = P.Player.Roles
    s_roles = roles[1:]
    padding = 0
    if roles[0] == "T":
        image.paste(wtank_icon, (width // 2 - 160 - (padding * 40), 220 + (i * 144)), mask=wtank_icon)
    elif roles[0] == "D":
        image.paste(wdps_icon, (width // 2 - 160 - (padding * 40), 220 + (i * 144)), mask=wdps_icon)
    elif roles[0] == "H":
        image.paste(wheal_icon, (width // 2 - 160 - (padding * 40), 220 + (i * 144)), mask=wheal_icon)

    for r in range(len(s_roles)):
        if s_roles[r] == "T":
            image.paste(gtank_icon.resize((40, 40)), (width // 2 - 200 - (r * 40), 240 + (i * 144)))
        elif s_roles[r] == "D":
            image.paste(gdps_icon.resize((40, 40)), (width // 2 - 200 - (r * 40), 240 + (i * 144)))
        elif s_roles[r] == "H":
            image.paste(gheal_icon.resize((40, 40)), (width // 2 - 200 - (r * 40), 240 + (i * 144)))


def createImage(gameData):
    width = 1920
    height = 1080
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, width, height), "#090C10")
    draw.rectangle((20, 160, width // 2 - 70, height - 20), "#161B22")
    draw.rectangle((40, 180, 150, height - 40), "#1e90ff")
    draw.rectangle((width // 2 + 70, 160, width - 20, height - 20), "#161B22")
    draw.rectangle((width // 2 + 90, 180, width // 2 + 200, height - 40), "#ff6347")

    draw.text((20, 0), "Team 1", "#ffffff", font=team_font)
    draw.text((width // 2 - 65, 180), "VS", "#ffffff", font=vs_font)
    draw.text((30, 100), f"AVG: {gameData['first']['AVG']}", "#ffffff", font=avg_font)

    draw.text((width // 2 + 70, 0), "Team 2", "#ffffff", font=team_font)
    draw.text((width // 2 + 80, 100), f"AVG: {gameData['second']['AVG']}", "#ffffff", font=avg_font)

    # right team handler
    ind = len(gameData["second"][0])
    ite = 0
    for i in range(ind):
        image.paste(rtank_icon, (width // 2 + 95, 200 + (i * 144)))
        P = Custom.select().where(Custom.ID == gameData["second"][0][ite])
        if P.exists():
            P = P[0]

            roles_priority_right(P, image, i, width)

            image.paste(get_rank_icon(P.TSR), (width // 2 + 105, 200 + (i * 144)), mask=get_rank_icon(P.TSR))
            draw.text((width // 2 + 110, 270 + (i * 144)), f"{P.TSR}", font=text_ranknum)
            draw.text((width // 2 + 240, 210 + (i * 144)), f"{P.Player.Username}", font=text_font)
            ite += 1

    ite = 0
    for i in range(ind, ind + len(gameData["second"][1])):
        image.paste(rdps_icon, (width // 2 + 95, 200 + (i * 144)))
        P = Custom.select().where(Custom.ID == gameData["second"][1][ite])
        if P.exists():
            P = P[0]

            roles_priority_right(P, image, i, width)

            image.paste(get_rank_icon(P.DSR), (width // 2 + 105, 200 + (i * 144)), mask=get_rank_icon(P.DSR))
            draw.text((width // 2 + 110, 270 + (i * 144)), f"{P.DSR}", font=text_ranknum)
            draw.text((width // 2 + 240, 210 + (i * 144)), f"{P.Player.Username}", font=text_font)
            ite += 1
    ind += len(gameData["second"][1])

    ite = 0
    for i in range(ind, ind + len(gameData["second"][2])):
        image.paste(rheal_icon, (width // 2 + 95, 200 + (i * 144)))
        P = Custom.select().where(Custom.ID == gameData["second"][2][ite])
        if P.exists():
            P = P[0]

            roles_priority_right(P, image, i, width)

            image.paste(get_rank_icon(P.HSR), (width // 2 + 105, 200 + (i * 144)), mask=get_rank_icon(P.HSR))
            draw.text((width // 2 + 110, 270 + (i * 144)), f"{P.HSR}", font=text_ranknum)
            draw.text((width // 2 + 240, 210 + (i * 144)), f"{P.Player.Username}", font=text_font)
            ite += 1

    # left team handler
    ind = len(gameData["first"][0])
    ite = 0
    for i in range(ind):
        image.paste(btank_icon, (45, 200 + (i * 144)))
        P = Custom.select().where(Custom.ID == gameData["first"][0][ite])
        if P.exists():
            P = P[0]

            roles_priority_left(P, image, i, width)

            image.paste(get_rank_icon(P.TSR), (55, 200 + (i * 144)), mask=get_rank_icon(P.TSR))
            draw.text((60, 270 + (i * 144)), f"{P.TSR}", font=text_ranknum)
            draw.text((190, 210 + (i * 144)), f"{P.Player.Username}", font=text_font)
            ite += 1

    ite = 0
    for i in range(ind, ind + len(gameData["first"][1])):
        image.paste(bdps_icon, (45, 200 + (i * 144)))
        P = Custom.select().where(Custom.ID == gameData["first"][1][ite])
        if P.exists():
            P = P[0]

            roles_priority_left(P, image, i, width)

            image.paste(get_rank_icon(P.DSR), (55, 200 + (i * 144)), mask=get_rank_icon(P.DSR))
            draw.text((60, 270 + (i * 144)), f"{P.DSR}", font=text_ranknum)
            draw.text((190, 210 + (i * 144)), f"{P.Player.Username}", font=text_font)
            ite += 1
    ind += len(gameData["first"][1])

    ite = 0
    for i in range(ind, ind + len(gameData["first"][2])):
        image.paste(bheal_icon, (45, 200 + (i * 144)))
        P = Custom.select().where(Custom.ID == gameData["first"][2][ite])
        if P.exists():
            P = P[0]

            roles_priority_left(P, image, i, width)

            image.paste(get_rank_icon(P.HSR), (55, 200 + (i * 144)), mask=get_rank_icon(P.HSR))
            draw.text((60, 270 + (i * 144)), f"{P.HSR}", font=text_ranknum)
            draw.text((190, 210 + (i * 144)), f"{P.Player.Username}", font=text_font)
            ite += 1
    rtank_icon.save('rt.png')

    return image


d = {'pareTeamAVG': 300, 'first': {'AVG': 2933, 'RolePoints': 18, 0: [4, 6], 1: [7, 12], 2: [3, 5]}, 'second': {'AVG': 2950, 'RolePoints': 15, 0: [1, 8], 1: [9, 11], 2: [2, 10]}}

createImage(d).save('draw-smile.jpg')
