from PIL import Image, ImageDraw, ImageFont, ImageColor
# from app.DataBase.db import Profile

bronze_icon = Image.open("app/icons/PIL1/bronse.png").resize((80, 80))
silver_icon = Image.open("app/icons/PIL1/silver.png").resize((80, 80))
gold_icon = Image.open("app/icons/PIL1/gold.png").resize((80, 80))
plat_icon = Image.open("app/icons/PIL1/plat.png").resize((80, 80))
diamond_icon = Image.open("app/icons/PIL1/diamond.png").resize((80, 80))
masters_icon = Image.open("app/icons/PIL1/masters.png").resize((80, 80))
gm_icon = Image.open("app/icons/PIL1/gm.png").resize((80, 80))

heal_icon = Image.open("app/icons/PIL1/Roles/Heal1.png").resize((100, 100))
dps_icon = Image.open("app/icons/PIL1/Roles/Dps1.png").resize((100, 100))
tank_icon = Image.open("app/icons/PIL1/Roles/Tank1.png").resize((100, 100))
flex_icon = Image.open("app/icons/PIL1/Roles/flex.png").resize((100, 100))

team_font = ImageFont.truetype("app/icons/font.ttf", 96)
vs_font = ImageFont.truetype("app/icons/VS_font.otf", 84)
avg_font = ImageFont.truetype("app/icons/font.ttf", 48)
text_font = ImageFont.truetype("app/icons/font.ttf", 68)
text_ranknum = ImageFont.truetype("app/icons/font.ttf", 32)


def get_rank_icon(rank):
    if rank < 1500:
        return bronze_icon
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


def generatePlayer(d, role, color_hex):
    width = 870
    height = 144

    image = Image.new('RGB', (width, height), '#161B22')
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 110, height), color_hex)
    if role == 0:
        role_ico = tank_icon
    elif role == 1:
        role_ico = dps_icon
    else:
        role_ico = heal_icon
    color = Image.new('RGB', role_ico.size, ImageColor.getcolor(color_hex, 'RGB'))
    mask = Image.new("L", role_ico.size, 45)
    image.paste(Image.composite(role_ico.convert("L"), color, mask), (5, 20), mask=role_ico)
    if role == 0:
        rank = d["TSR"]
    elif role == 1:
        rank = d["DSR"]
    else:
        rank = d["HSR"]
    rank_ico = get_rank_icon(rank)
    image.paste(rank_ico, (15, 20), mask=rank_ico)
    draw.text((20, 90), f"{rank}", font=text_ranknum)
    draw.text((150, 30), f"{d['Username']}", font=text_font)

    ico = None
    if d["Flex"]:
        ico = flex_icon
    elif d["Roles"][0] == "T":
        ico = tank_icon
    elif d["Roles"][0] == "D":
        ico = dps_icon
    elif d["Roles"][0] == "H":
        ico = heal_icon
    if ico:
        ico = ico.resize((60, 60))
        color = Image.new('RGB', ico.size, ImageColor.getcolor('white', 'RGB'))
        mask = Image.new("L", ico.size, 16)
        image.paste(Image.composite(ico.convert("L"), color, mask), (width - 90, 40), mask=ico)
    sRoles = d["Roles"][1:]
    if not d["Flex"]:
        for r in range(len(sRoles)):
            ico = None
            if sRoles[r] == "T":
                ico = tank_icon
            elif sRoles[r] == "D":
                ico = dps_icon
            elif sRoles[r] == "H":
                ico = heal_icon
            if ico:
                ico = ico.resize((40, 40))
                color = Image.new('RGB', ico.size, ImageColor.getcolor('grey', 'RGB'))
                mask = Image.new("L", ico.size, 32)
                image.paste(Image.composite(ico.convert("L"), color, mask), (width - 130 - (r * 40), 60), mask=ico)
    return image


def createBackground(d, USettings, fColor, sColor):
    PlayersInTeam = USettings["Amount"]["T"] + USettings["Amount"]["D"] + USettings["Amount"]["H"]

    width = 1920
    height = PlayersInTeam * 144 + 220
    image = Image.new('RGB', (width, height), "#090C10")
    draw = ImageDraw.Draw(image)

    draw.rectangle((20, 160, width // 2 - 70, height - 20), "#161B22")
    draw.rectangle((width // 2 + 70, 160, width - 20, height - 20), "#161B22")
    draw.rectangle((40, 180, 150, height - 40), fColor)
    draw.rectangle((width // 2 + 90, 180, width // 2 + 200, height - 40), sColor)

    draw.text((20, 0), USettings["TeamNames"]["1"], "#ffffff", font=team_font)
    draw.text((width // 2 - 62, height // 2 + 20), "VS", "#ffffff", font=vs_font)

    w, h = team_font.getsize(USettings["TeamNames"]["2"])
    draw.text((width - 20 - w, 0), USettings["TeamNames"]["2"], "#ffffff", font=team_font)

    TDiff = f"Evaluation: {d['active']['result']}"
    w, h = avg_font.getsize(TDiff)
    draw.text((width // 2 - w // 2, 10), TDiff, font=avg_font, fill="#46494D")
    if USettings["ExpandedResult"]:
        Fairness = "Fairness: " + str(d['active']["rgRolesFairness"] + d['active']["dpFairness"])
        Uniformity = "Uniformity: " + str(d['active']["vqUniformity"])
        w, h = avg_font.getsize(Fairness)
        draw.text((width // 2 - 70 - w, 100), Fairness, "#46494D", font=avg_font)
        draw.text((width // 2 + 70, 100), Uniformity, "#46494D", font=avg_font)
    return image


def generateWholeData(d, U):
    UserSettings = U.getUserSettings()
    fColor = UserSettings["fColor"]
    sColor = UserSettings["sColor"]
    static = d["static"]
    fInd = 0
    sInd = 0
    fTeam = []
    sTeam = []
    Back = createBackground(d, UserSettings, fColor, sColor)
    mask = d["active"]["TeamMask"]
    for i in range(len(mask)):
        if int(mask[i]) == 0:
            im = generatePlayer(static[i], int(d["active"]["fMask"][fInd]), fColor)
            fTeam.append(im)
            # im.save(f"BalanceImages/{static[i]['Username']}.jpg")
            fInd += 1
        else:
            im = generatePlayer(static[i], int(d["active"]["sMask"][sInd]), sColor)
            sTeam.append(im)
            # im.save(f"BalanceImages/{static[i]['Username']}.jpg")
            sInd += 1
    ans = {"Background": Back, "fTeam": fTeam, "sTeam": sTeam}
    return ans


# x = {'static':
#          [{'Username': 'Artmagic', 'TSR': 3100, 'DSR': 2900, 'HSR': 2800, 'Flex': False, 'Roles': 'TDH'},
#           {'Username': 'Ivarys', 'TSR': 2900, 'DSR': 2900, 'HSR': 2799, 'Flex': False, 'Roles': 'DT'},
#           {'Username': 'Honoka', 'TSR': 3200, 'DSR': 3200, 'HSR': 3200, 'Flex': False, 'Roles': 'HD'},
#           {'Username': 'Quru', 'TSR': 2700, 'DSR': 2800, 'HSR': 3300, 'Flex': False, 'Roles': 'DH'},
#           {'Username': 'Dima', 'TSR': 2800, 'DSR': 2900, 'HSR': 3100, 'Flex': False, 'Roles': 'TD'},
#           {'Username': 'S1lver', 'TSR': 2600, 'DSR': 2600, 'HSR': 2900, 'Flex': False, 'Roles': 'DT'},
#           {'Username': 'zMize', 'TSR': 2800, 'DSR': 2600, 'HSR': 2400, 'Flex': False, 'Roles': 'TD'},
#           {'Username': 'Konder', 'TSR': 3800, 'DSR': 3100, 'HSR': 3400, 'Flex': False, 'Roles': 'DT'},
#           {'Username': 'Svevoloch', 'TSR': 3000, 'DSR': 2900, 'HSR': 2850, 'Flex': False, 'Roles': 'DH'},
#           {'Username': 'AuntPetunia', 'TSR': 3200, 'DSR': 2700, 'HSR': 2800, 'Flex': False, 'Roles': 'HD'},
#           {'Username': 'Cherry', 'TSR': 3200, 'DSR': 2850, 'HSR': 3300, 'Flex': False, 'Roles': 'HT'},
#           {'Username': 'Tia_ti', 'TSR': 2000, 'DSR': 3200, 'HSR': 2500, 'Flex': False, 'Roles': 'HT'}],
#      'active': {"TeamMask": "011001110100", "fMask": "010122", "sMask": "021012", "dpFairness": 29.47,
#                 "rgRolesFairness": 164.11, "teamRolePriority": 80.0, "vqUniformity": 51.66, "result": 325.25}
#      }
# print(generateWholeData(x, Profile.select().where(Profile.ID == 1)[0]))
# print(ImageColor.getcolor('grey', 'RGB'))