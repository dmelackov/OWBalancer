from PIL import Image, ImageDraw, ImageFont
from app.DataBase.db import Custom, Profile
bronse_icon = Image.open("app/icons/PIL1/bronse.png").resize((80, 80))
silver_icon = Image.open("app/icons/PIL1/silver.png").resize((80, 80))
gold_icon = Image.open("app/icons/PIL1/gold.png").resize((80, 80))
plat_icon = Image.open("app/icons/PIL1/plat.png").resize((80, 80))
diamond_icon = Image.open("app/icons/PIL1/diamond.png").resize((80, 80))
masters_icon = Image.open("app/icons/PIL1/masters.png").resize((80, 80))
gm_icon = Image.open("app/icons/PIL1/gm.png").resize((80, 80))
team_font = ImageFont.truetype("app/Calculation/font.ttf", 96)
vs_font = ImageFont.truetype("app/Calculation/VS_font.otf", 84)
avg_font = ImageFont.truetype("app/Calculation/font.ttf", 48)
text_font = ImageFont.truetype("app/Calculation/font.ttf", 68)
text_ranknum = ImageFont.truetype("app/Calculation/font.ttf", 32)
percent_font = ImageFont.truetype("app/Calculation/font.ttf", 30)
bheal_icon = Image.open("app/icons/PIL1/Roles/BlueHeal2.png").resize((100, 100))
bdps_icon = Image.open("app/icons/PIL1/Roles/BlueDps2.png").resize((100, 100))
btank_icon = Image.open("app/icons/PIL1/Roles/BlueTank2.png").resize((100, 100))

rheal_icon = Image.open("app/icons/PIL1/Roles/RedHeal2.png").resize((100, 100))
rdps_icon = Image.open("app/icons/PIL1/Roles/RedDps2.png").resize((100, 100))
rtank_icon = Image.open("app/icons/PIL1/Roles/RedTank2.png").resize((100, 100))

gheal_icon = Image.open("app/icons/PIL1/Roles/GrayHeal.png")
gdps_icon = Image.open("app/icons/PIL1/Roles/GrayDps.png")
gtank_icon = Image.open("app/icons/PIL1/Roles/GrayTank.png")


wheal_icon = Image.open("app/icons/PIL1/Roles/heal_icon.png").resize((60, 60))
wdps_icon = Image.open("app/icons/PIL1/Roles/dps_icon.png").resize((60, 60))
wtank_icon = Image.open("app/icons/PIL1/Roles/tank_icon.png").resize((60, 60))
wflex = Image.open("app/icons/PIL1/Roles/flex.png").resize((60, 60))


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
    if P.Player.isFlex:
        image.paste(wflex, (width - 110, 220 + (i * 144)), mask=wflex)
    elif roles[0] == "T":
        image.paste(wtank_icon, (width - 110, 220 + (i * 144)), mask=wtank_icon)
    elif roles[0] == "D":
        image.paste(wdps_icon, (width - 110, 220 + (i * 144)), mask=wdps_icon)
    elif roles[0] == "H":
        image.paste(wheal_icon, (width - 110, 220 + (i * 144)), mask=wheal_icon)

    if not P.Player.isFlex:
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
    if P.Player.isFlex:
        image.paste(wflex, (width // 2 - 160, 220 + (i * 144)), mask=wflex)
    elif roles[0] == "T":
        image.paste(wtank_icon, (width // 2 - 160, 220 + (i * 144)), mask=wtank_icon)
    elif roles[0] == "D":
        image.paste(wdps_icon, (width // 2 - 160, 220 + (i * 144)), mask=wdps_icon)
    elif roles[0] == "H":
        image.paste(wheal_icon, (width // 2 - 160, 220 + (i * 144)), mask=wheal_icon)

    if not P.Player.isFlex:
        for r in range(len(s_roles)):
            if s_roles[r] == "T":
                image.paste(gtank_icon.resize((40, 40)), (width // 2 - 200 - (r * 40), 240 + (i * 144)))
            elif s_roles[r] == "D":
                image.paste(gdps_icon.resize((40, 40)), (width // 2 - 200 - (r * 40), 240 + (i * 144)))
            elif s_roles[r] == "H":
                image.paste(gheal_icon.resize((40, 40)), (width // 2 - 200 - (r * 40), 240 + (i * 144)))


def createImage(gameData, U):
    width = 1920
    height = 1080
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, width, height), "#090C10")
    draw.rectangle((20, 160, width // 2 - 70, height - 20), "#161B22")
    draw.rectangle((40, 180, 150, height - 40), "#1e90ff")
    draw.rectangle((width // 2 + 70, 160, width - 20, height - 20), "#161B22")
    draw.rectangle((width // 2 + 90, 180, width // 2 + 200, height - 40), "#ff6347")

    USettings = U.getUserSettings()
    draw.text((20, 0), USettings["TeamNames"]["1"], "#ffffff", font=team_font)
    draw.text((width // 2 - 62, 560), "VS", "#ffffff", font=vs_font)
    draw.text((30, 100), f"AVG: {gameData['first']['AVG']}", "#ffffff", font=avg_font)

    w, h = team_font.getsize(USettings["TeamNames"]["2"])
    draw.text((width - 20 - w, 0), USettings["TeamNames"]["2"], "#ffffff", font=team_font)
    avg = f"AVG: {gameData['second']['AVG']}"
    w, h = avg_font.getsize(avg)
    draw.text((width - 30 - w, 100), avg, "#ffffff", font=avg_font)

    TDiff = f"Evaluation: {gameData['pareTeamAVG']}"
    w, h = avg_font.getsize(TDiff)
    draw.text((width // 2 - w // 2, 10), TDiff, font=avg_font, fill="#46494D")

    # предсказание победителя
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

    # right team handler
    ind = len(gameData["second"]["0"])
    ite = 0
    for i in range(ind):
        image.paste(rtank_icon, (width // 2 + 95, 200 + (i * 144)))
        C = Custom.select().where(Custom.ID == gameData["second"]["0"][ite])
        if C.exists():
            C = C[0]

            roles_priority_right(C, image, i, width)

            image.paste(get_rank_icon(C.TSR), (width // 2 + 105, 200 + (i * 144)), mask=get_rank_icon(C.TSR))
            draw.text((width // 2 + 110, 270 + (i * 144)), f"{C.TSR}", font=text_ranknum)
            draw.text((width // 2 + 240, 210 + (i * 144)), f"{C.Player.Username}", font=text_font)
            ite += 1

    ite = 0
    for i in range(ind, ind + len(gameData["second"]["1"])):
        image.paste(rdps_icon, (width // 2 + 95, 200 + (i * 144)))
        C = Custom.select().where(Custom.ID == gameData["second"]["1"][ite])
        if C.exists():
            C = C[0]

            roles_priority_right(C, image, i, width)

            image.paste(get_rank_icon(C.DSR), (width // 2 + 105, 200 + (i * 144)), mask=get_rank_icon(C.DSR))
            draw.text((width // 2 + 110, 270 + (i * 144)), f"{C.DSR}", font=text_ranknum)
            draw.text((width // 2 + 240, 210 + (i * 144)), f"{C.Player.Username}", font=text_font)
            ite += 1
    ind += len(gameData["second"]["1"])

    ite = 0
    for i in range(ind, ind + len(gameData["second"]["2"])):
        image.paste(rheal_icon, (width // 2 + 95, 200 + (i * 144)))
        C = Custom.select().where(Custom.ID == gameData["second"]["2"][ite])
        if C.exists():
            C = C[0]

            roles_priority_right(C, image, i, width)

            image.paste(get_rank_icon(C.HSR), (width // 2 + 105, 200 + (i * 144)), mask=get_rank_icon(C.HSR))
            draw.text((width // 2 + 110, 270 + (i * 144)), f"{C.HSR}", font=text_ranknum)
            draw.text((width // 2 + 240, 210 + (i * 144)), f"{C.Player.Username}", font=text_font)
            ite += 1

    # left team handler
    ind = len(gameData["first"]["0"])
    ite = 0
    for i in range(ind):
        image.paste(btank_icon, (45, 200 + (i * 144)))
        C = Custom.select().where(Custom.ID == gameData["first"]["0"][ite])
        if C.exists():
            C = C[0]

            roles_priority_left(C, image, i, width)

            image.paste(get_rank_icon(C.TSR), (55, 200 + (i * 144)), mask=get_rank_icon(C.TSR))
            draw.text((60, 270 + (i * 144)), f"{C.TSR}", font=text_ranknum)
            draw.text((190, 210 + (i * 144)), f"{C.Player.Username}", font=text_font)
            ite += 1

    ite = 0
    for i in range(ind, ind + len(gameData["first"]["1"])):
        image.paste(bdps_icon, (45, 200 + (i * 144)))
        C = Custom.select().where(Custom.ID == gameData["first"]["1"][ite])
        if C.exists():
            C = C[0]

            roles_priority_left(C, image, i, width)

            image.paste(get_rank_icon(C.DSR), (55, 200 + (i * 144)), mask=get_rank_icon(C.DSR))
            draw.text((60, 270 + (i * 144)), f"{C.DSR}", font=text_ranknum)
            draw.text((190, 210 + (i * 144)), f"{C.Player.Username}", font=text_font)
            ite += 1
    ind += len(gameData["first"]["1"])

    ite = 0
    for i in range(ind, ind + len(gameData["first"]["2"])):
        image.paste(bheal_icon, (45, 200 + (i * 144)))
        C = Custom.select().where(Custom.ID == gameData["first"]["2"][ite])
        if C.exists():
            C = C[0]

            roles_priority_left(C, image, i, width)

            image.paste(get_rank_icon(C.HSR), (55, 200 + (i * 144)), mask=get_rank_icon(C.HSR))
            draw.text((60, 270 + (i * 144)), f"{C.HSR}", font=text_ranknum)
            draw.text((190, 210 + (i * 144)), f"{C.Player.Username}", font=text_font)
            ite += 1

    return image


# if __name__ == '__main__':
#     d = {'pareTeamAVG': 900, 'NeuroPredict': 0,
#          'first': {'AVG': 3100, 'RolePoints': 16, "0": [7, 8], "1": [10, 22], "2": [5, 21]},
#          'second': {'AVG': 3083, 'RolePoints': 16, "0": [1, 9], "1": [3, 6], "2": [4, 11]},
#          'rangeTeam': 1824.814471757034}
#
#     img = createImage(d, Profile.select().where(Profile.Username == "Ivarys")[0])
#     img.save('IMAGE.jpg')
