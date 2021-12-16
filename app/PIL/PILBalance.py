from PIL import Image, ImageDraw, ImageFont
from app.Static.globalClasses import *
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


def roles_priority_right(M, image, i, width):
    roles = M.Roles
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
        image.paste(ico, (width - 110, 220 + (i * 144)), mask=ico)

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
                image.paste(ico, (width - 150 - (r * 40), 240 + (i * 144)))


def roles_priority_left(M, image, i, width):
    roles = M.Roles
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
        image.paste(ico, (width // 2 - 160, 220 + (i * 144)), mask=ico)

    if not M.isFlex:
        for r in range(len(s_roles)):
            ico = None
            if s_roles[r] == 0:
                ico = gtank_icon
            elif s_roles[r] == 1:
                ico = gdps_icon
            elif s_roles[r] == 2:
                ico = gheal_icon
            if ico:
                image.paste(ico.resize((40, 40)), (width // 2 - 200 - (r * 40), 240 + (i * 144)))


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

    # right team handler
    ind = 0
    for j in range(3):
        ite = 0
        role_index = str(j)
        if j == 0:
            role_ico = rtank_icon
        elif j == 1:
            role_ico = rdps_icon
        else:
            role_ico = rheal_icon
        for i in range(ind, ind + len(gameData["second"][role_index])):
            image.paste(role_ico, (width // 2 + 95, 200 + (i * 144)))
            M = Member(gameData["second"][role_index][ite])

            roles_priority_right(M, image, i, width)

            rank_ico = get_rank_icon(M.Rating[j])
            image.paste(rank_ico, (width // 2 + 105, 200 + (i * 144)), mask=rank_ico)
            draw.text((width // 2 + 110, 270 + (i * 144)), f"{M.Rating[j]}", font=text_ranknum)
            draw.text((width // 2 + 240, 210 + (i * 144)), f"{M.Name}", font=text_font)
            ite += 1
        ind += len(gameData["second"][role_index])

    # left team handler
    ind = 0
    for j in range(3):
        ite = 0
        role_index = str(j)
        if j == 0:
            role_ico = btank_icon
        elif j == 1:
            role_ico = bdps_icon
        else:
            role_ico = bheal_icon
        for i in range(ind, ind + len(gameData["first"][role_index])):
            image.paste(role_ico, (45, 200 + (i * 144)))
            M = Member(gameData["first"][role_index][ite])

            roles_priority_left(M, image, i, width)

            rank_ico = get_rank_icon(M.Rating[j])
            image.paste(rank_ico, (55, 200 + (i * 144)), mask=rank_ico)
            draw.text((60, 270 + (i * 144)), f"{M.Rating[j]}", font=text_ranknum)
            draw.text((190, 210 + (i * 144)), f"{M.Name}", font=text_font)
            ite += 1
        ind += len(gameData["first"][role_index])
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
#             },
#          'rangeTeam': 0.0}
#
#     img = createImage(d, Profile.select().where(Profile.Username == "Ivarys")[0])
#     img.save('IMAGE.jpg')
