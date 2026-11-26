"""Render the news-image-20261126 entry: one 1024x1024 page that sums up the
world news of Thursday 26 November 2026.

Every story below was reported on Thursday 26 November 2026 (see
NEWS_SOURCES.md for the per-item source and date basis). The page carries
12 lead cards with a dotted world map, a market panel, a UTC timeline,
a strip naming big stories deliberately left out because they are
yesterday's news, and the rest of the day as one-line briefs.

Run:  python3 render.py   ->  writes entry.png next to this file.
The render is deterministic: same data, same bytes, every run.
"""

import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
HERE = os.path.dirname(os.path.abspath(__file__))

PAPER = (247, 243, 234)
CARD_BG = (255, 253, 247)
INK = (20, 24, 29)
MUTE = (96, 90, 78)
RULE = (216, 210, 196)
RED = (179, 53, 43)
DARK = (24, 26, 31)

REGION_COLORS = {
    "WORLD": (140, 106, 0),
    "ASIA": (179, 53, 43),
    "EUROPE": (36, 86, 166),
    "MIDEAST": (122, 59, 143),
    "AMERICAS": (30, 122, 70),
    "SPORT": (194, 97, 0),
    "AFRICA": (138, 90, 18),
}

# ---------------------------------------------------------------- data ----
# (region, headline, sub, pin number, lon, lat, pin label)
CARDS = [
    ("WORLD",
     "Japan conveys regrets over US Section 301 tariff plan",
     "Unveiled Wed: China 20%, Vietnam 35%, India 25%; Japan, EU, "
     "Korea 15%.",
     1, 139.7, 35.7, "TOKYO"),
    ("ASIA",
     "Bank of Korea raises rates 25bp to 3.25% in split decision",
     "5-2 vote; 2026 growth outlook lifted to 3.9%, 2027 to 4.1%, as the "
     "won slides.",
     2, 127.0, 37.6, "SEOUL"),
    ("ASIA",
     "Asia shares bounce after brutal month as Wall Street steadies",
     "Nikkei +1.6%, Kospi +1.9% early; US shut for Thanksgiving, S&P "
     "futures +0.5%.",
     3, 139.7, 35.7, "TOKYO"),
    ("EUROPE",
     "Russia and Ukraine trade overnight strikes; Ryazan refinery burns",
     "Moscow claims hub, substation, ship; Kyiv drones spark Ryazan "
     "refinery fire.",
     4, 39.7, 54.6, "RYAZAN"),
    ("MIDEAST",
     "Overnight Gaza strike kills Hamas deputy education minister",
     "Khaled Abu Nada and his wife killed in a Deir el-Balah apartment "
     "strike.",
     5, 34.3, 31.4, "GAZA"),
    ("MIDEAST",
     "Blast rocks Sanaa as Houthi missiles are intercepted over Riyadh",
     "Saudi air defences down two Houthi ballistic missiles fired "
     "towards Riyadh.",
     6, 44.2, 15.4, "SANAA"),
    ("AMERICAS",
     "Thanksgiving nor'easter slams US East Coast",
     "Flooding, 70 mph gusts, coastal surge; NJ emergency in force for "
     "the holiday.",
     7, -74.0, 40.7, "NEW YORK"),
    ("EUROPE",
     "EU leaders open special summit on budget and Ukraine",
     "Two days in Brussels on Costa's 2028-34 budget plan; Merz pushes "
     "spending limits.",
     8, 4.35, 50.85, "BRUSSELS"),
    ("ASIA",
     "China unveils roadmap for next-generation networks by 2030",
     "Implementation plan out Thursday targets full coverage and leading "
     "performance.",
     9, 116.4, 39.9, "BEIJING"),
    ("ASIA",
     "India shares set to extend winning streak toward record high",
     "GIFT Nifty at 26,061.5 early; foreign buying a record $15.16bn "
     "this month.",
     10, 72.9, 19.1, "MUMBAI"),
    ("SPORT",
     "Europa League matchday 5: 18 games across two kickoff windows",
     "Olympiakos host Milan early; Palace face Sociedad and Juventus "
     "host Omonia late.",
     11, -0.1, 51.5, "LONDON"),
    ("ASIA",
     "Kim Jong Un vows North Korea will keep developing nuclear weapons",
     "State media say he toured nuclear sites Wednesday and pledged "
     "stronger deterrence.",
     12, 125.8, 39.0, "PYONGYANG"),
]

# (region, one-line brief) -- numbered on the page. Only briefs the
# independent reviewer verified as Thursday 26 Nov news are listed;
# replacements verified the same way are appended before the final render.
BRIEFS = [
    ("ASIA", "BOJ's Tamura: monetary conditions still accommodative, not yet neutral"),
    ("ASIA", "Chinese shares open higher Thursday; Shanghai Composite +0.39% to 3,490.14"),
    ("ASIA", "Japan opposition files censure motion against education minister Seki"),
    ("ASIA", "Nagasaki's A-bombed Virgin Mary head heads to US, first time in 16 years"),
    ("ASIA", "India marks Constitution Day; Congress holds 'Samvidhan Raksha' marches"),
    ("ASIA", "CPTPP, ASEAN and EU trade chiefs open dialogue in Vietnam"),
    ("ASIA", "Indonesia illegal gold-mine flood toll rises to 13, 13 still missing"),
    ("ASIA", "SE Asia markets mixed Thursday: Jakarta +1.32%, KL +1.05%, Bangkok -1.59%"),
    ("EUROPE", "Le Monde: European leaders ready to resume talking to Putin"),
    ("EUROPE", "Spain's Sanchez: majority 'within fingertips' before Sunday snap vote"),
    ("EUROPE", "UK to publish new treaties agreed with EU"),
    ("EUROPE", "Stalking to become a single offence under UK law change"),
    ("MIDEAST", "Houthi shelling kills woman, wounds seven in Yemen's Taiz"),
    ("MIDEAST", "Senator Sanders urges halt to US military aid for Israel"),
    ("AMERICAS", "California warns of flooding as King Tides peak over Thanksgiving"),
    ("ASIA", "POSTECH team unveils solid-state battery working at low pressure"),
    ("ASIA", "Survey: 52% of New Zealand businesses now use AI, MBIE says"),
    ("ASIA", "Watchdog: police justified in firing shot during Kaitaia arrest"),
    ("ASIA", "Bay of Plenty partners plan native forest on 180ha near Rotorua"),
    ("ASIA", "Wellington committee agrees in principle to ease pet travel rules"),
    ("ASIA", "Newstalk ZB tops New Zealand radio in GfK Survey 3 results"),
    ("ASIA", "European Union Film Festival opens in Dhaka, running to 29 Nov"),
    ("ASIA", "Boyz II Men play Perth's RAC Arena with Salt-N-Pepa on Thursday"),
    ("EUROPE", "Amsterdam Light Festival's 15th edition opens on Thursday night"),
    ("SPORT", "Brighton host Universitatea Craiova in Conference League Thursday"),
    ("SPORT", "New Zealand host India in second Test starting Thursday night GMT"),
    ("AMERICAS", "NFL Thanksgiving tripleheader: Bears-Lions, Eagles-Cowboys, Chiefs-Bills"),
    ("AFRICA", "Ethiopia defends Sudan dialogue offer after Khartoum's rejection"),
    ("AFRICA", "Nigeria women's league holds AGM and Premiership draw in Abuja"),
    ("AFRICA", "Johannesburg HYROX opens with 15,000 athletes over four days"),
]

# Reuters global-markets wrap, 2026-11-26 01:53 UTC
MARKET = [
    ("BRENT", "$94.81 +0.2%"),
    ("WTI", "$84.24 +0.6%"),
    ("GOLD", "$3,566 -0.4%"),
    ("USD/JPY", "159.14"),
    ("DOLLAR IDX", "103.71"),
    ("EUR/USD", "1.0973"),
    ("US 10Y", "4.848%"),
    ("NIKKEI", "+1.6% EARLY"),
    ("KOSPI", "+1.9% EARLY"),
    ("S&P FUT", "+0.5%"),
    ("WALL ST", "CLOSED THU"),
]

TIMELINE = [
    ("01:00", "Bank of Korea raises policy rate 25bp to 3.25% (10:00 KST decision)"),
    ("01:09", "Japan opposition files censure motion against education minister"),
    ("01:27", "BOJ's Tamura: conditions still accommodative, not yet neutral"),
    ("01:53", "Reuters: Asia shares bounce; Brent $94.81, gold $3,566 early"),
    ("02:23", "Gaza: Deir el-Balah apartment strike kills two"),
    ("02:36", "Japan conveys regrets to US over new tariff plan (11:36 JST)"),
    ("02:40", "Yemen: Houthi shelling kills woman, wounds seven in Taiz"),
    ("04:23", "Al Jazeera: Moscow says it hit a Kharkiv-area hub, substation and cargo ship"),
]

LEFT_OUT = (
    "Shenzhou-24 launch with first Pakistani astronaut (Wed) \u00b7 Ukraine's "
    "Savasleyka airbase strike and Russia's energy-grid attacks (Wed) \u00b7 "
    "Cairo fuel-tanker fire, 31 dead (Wed) \u00b7 US Q3 GDP revised to 4.3%, "
    "core PCE 3.3% (Wed data) \u00b7 Poundland collapse reports (Wed) \u00b7 "
    "Brazil-Argentina ambassador row (Tue)"
)

# Dotted world map: land spans per grid row (96 cols x 36 rows,
# equirectangular; row 0 ~ lat 88, row 35 ~ lat -51). (row, [(c0, c1), ...])
LAND = {
    0: [(40, 45)],
    1: [(29, 36), (40, 46)],
    2: [(24, 38), (40, 47), (52, 53), (58, 60), (68, 72)],
    3: [(2, 10), (18, 38), (41, 46), (56, 64), (68, 76), (80, 90)],
    4: [(1, 12), (16, 40), (42, 45), (50, 54), (55, 92)],
    5: [(2, 13), (15, 29), (34, 41), (43, 43), (46, 46), (50, 55), (56, 93)],
    6: [(3, 12), (14, 29), (34, 42), (49, 93)],
    7: [(15, 40), (46, 48), (49, 94)],
    8: [(16, 38), (46, 48), (48, 95)],
    9: [(15, 36), (47, 93)],
    10: [(14, 35), (47, 90)],
    11: [(14, 35), (47, 89)],
    12: [(13, 34), (45, 47), (51, 54), (55, 88)],
    13: [(13, 33), (44, 70), (72, 87)],
    14: [(12, 30), (42, 65), (68, 74), (75, 83)],
    15: [(12, 24), (42, 66), (68, 73), (76, 80)],
    16: [(13, 22), (43, 60), (68, 72), (76, 79)],
    17: [(14, 19), (42, 61), (68, 71), (76, 79)],
    18: [(15, 18), (43, 60), (69, 70), (76, 79), (81, 82)],
    19: [(24, 30), (44, 59), (78, 86)],
    20: [(24, 32), (45, 58), (77, 88)],
    21: [(25, 33), (46, 57), (79, 90)],
    22: [(25, 34), (46, 57), (87, 91)],
    23: [(25, 34), (46, 56)],
    24: [(25, 33), (47, 56), (82, 88)],
    25: [(26, 33), (47, 55), (80, 89)],
    26: [(26, 32), (48, 55), (56, 57), (79, 89)],
    27: [(26, 31), (48, 54), (79, 88)],
    28: [(26, 30), (48, 53), (80, 87)],
    29: [(26, 29), (49, 52), (81, 86), (93, 94)],
    30: [(26, 28), (82, 85), (93, 95)],
    31: [(26, 28), (94, 95)],
    32: [(26, 27)],
    33: [(26, 27)],
    34: [(26, 27)],
}

# ------------------------------------------------------------- drawing ----
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSerif-Bold.ttf", 30)
F_DATE = font("DejaVuSans-Bold.ttf", 15)
F_STRIP = font("DejaVuSans.ttf", 10)
F_TAG = font("DejaVuSans-Bold.ttf", 8)
F_HEAD = font("DejaVuSans-Bold.ttf", 12)
F_SUB = font("DejaVuSans.ttf", 9)
F_SEC = font("DejaVuSans-Bold.ttf", 11)
F_MKT = font("DejaVuSansMono.ttf", 10)
F_MKTB = font("DejaVuSansMono-Bold.ttf", 10)
F_TL_T = font("DejaVuSansMono-Bold.ttf", 9)
F_TL = font("DejaVuSans.ttf", 8)
F_BRIEF = font("DejaVuSans.ttf", 9)
F_BRIEF_B = font("DejaVuSans-Bold.ttf", 9)
F_PIN = font("DejaVuSans-Bold.ttf", 8)
F_FOOT = font("DejaVuSans.ttf", 9)

MARGIN = 14
CW = W - 2 * MARGIN  # 996 usable width


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns the list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def check_layout(draw):
    """Fail loudly if any text block overflows its box."""
    problems = []
    if len(CARDS) != 12 or len(BRIEFS) < 10 or len(MARKET) != 11 \
            or len(TIMELINE) != 8:
        problems.append("story counts wrong")
    card_text_w = 225 - 16
    for region, head, sub, *_ in CARDS:
        if len(wrap(draw, head, F_HEAD, card_text_w)) > 3:
            problems.append(f"head wraps >3 lines: {head[:40]}")
        if len(wrap(draw, sub, F_SUB, card_text_w)) > 2:
            problems.append(f"sub wraps >2 lines: {sub[:40]}")
    brief_w = (CW - 16) // 2
    for i, (region, text) in enumerate(BRIEFS, 1):
        line = f"{i:02d} {region} \u2014 {text}"
        if draw.textlength(line, font=F_BRIEF) > brief_w:
            problems.append(f"brief {i:02d} too wide")
    tl_w = (CW - 3 * 10) // 4 - 40
    for t, text in TIMELINE:
        if len(wrap(draw, text, F_TL, tl_w)) > 3:
            problems.append(f"timeline wraps >3 lines: {t}")
    if len(wrap(draw, LEFT_OUT, F_STRIP, CW - 184)) > 2:
        problems.append("left-out strip wraps >2 lines")
    return problems


def draw_header(draw):
    draw.rectangle([0, 0, W, 56], fill=DARK)
    draw.text((MARGIN, 8), "THE WORLD ON THURSDAY", font=F_TITLE,
              fill=(247, 243, 234))
    draw.text((MARGIN, 40), "26 NOVEMBER 2026", font=F_DATE, fill=RED)
    right = f"ONE IMAGE \u00b7 {12 + len(BRIEFS)} STORIES \u00b7 EVERY DATE CHECKED"
    rw = draw.textlength(right, font=F_DATE)
    draw.text((W - MARGIN - rw, 22), right, font=F_DATE, fill=(247, 243, 234))
    draw.rectangle([0, 56, W, 58], fill=RED)
    strip = ("Every story on this page was reported on Thursday 26 November "
             "2026 \u2014 dates checked against Reuters, Yonhap, Kyodo, "
             "Xinhua, Al Jazeera and the BBC.")
    draw.text((MARGIN, 64), strip, font=F_STRIP, fill=MUTE)


def draw_cards(draw, x0, y0):
    col_w, row_h, gap = 225, 112, 8
    for idx, (region, head, sub, pin, lon, lat, label) in enumerate(CARDS):
        cx = x0 + (idx % 3) * (col_w + gap)
        cy = y0 + (idx // 3) * (row_h + gap)
        draw.rectangle([cx, cy, cx + col_w, cy + row_h], fill=CARD_BG,
                       outline=RULE)
        color = REGION_COLORS[region]
        tag_w = draw.textlength(region, font=F_TAG) + 10
        draw.rectangle([cx + 8, cy + 7, cx + 8 + tag_w, cy + 20], fill=color)
        draw.text((cx + 13, cy + 9), region, font=F_TAG,
                  fill=(255, 255, 255))
        pin_txt = f"PIN {pin} \u00b7 {label}"
        pw = draw.textlength(pin_txt, font=F_TAG)
        draw.text((cx + col_w - 8 - pw, cy + 9), pin_txt, font=F_TAG,
                  fill=MUTE)
        ty = cy + 26
        for line in wrap(draw, head, F_HEAD, col_w - 16):
            draw.text((cx + 8, ty), line, font=F_HEAD, fill=INK)
            ty += 14.5
        ty += 2
        for line in wrap(draw, sub, F_SUB, col_w - 16):
            draw.text((cx + 8, ty), line, font=F_SUB, fill=MUTE)
            ty += 11.5


def draw_map(draw, x, y, w, h):
    draw.text((x, y), "WHERE IT HAPPENED \u2014 THE 12 LEAD STORIES",
              font=F_SEC, fill=INK)
    my = y + 18
    mh = h - 18
    draw.rectangle([x, my, x + w, my + mh], fill=(238, 233, 220),
                   outline=RULE)
    cols, rows = 96, 36
    dx, dy = w / cols, mh / rows
    for r, spans in LAND.items():
        for c0, c1 in spans:
            for c in range(c0, c1 + 1):
                px = x + (c + 0.5) * dx
                py = my + (r + 0.5) * dy
                draw.ellipse([px - 1.1, py - 1.1, px + 1.1, py + 1.1],
                             fill=(178, 170, 152))
    # display nudges so clustered pins (Washington/New York, London/
    # Brussels, Beijing/Pyongyang/Seoul/Tokyo) stay separately readable
    nudge = {1: (-11, -8), 7: (7, -6), 8: (-8, 5), 11: (8, -5),
             9: (-9, -2), 12: (-3, -9), 2: (4, 8), 3: (10, 3)}
    for region, head, sub, pin, lon, lat, label in CARDS:
        px = x + (lon + 180) / 360 * w
        py = my + (90 - lat) / 141 * mh
        if pin in nudge:
            px += nudge[pin][0]
            py += nudge[pin][1]
        draw.ellipse([px - 7.5, py - 7.5, px + 7.5, py + 7.5], fill=RED,
                     outline=(255, 255, 255), width=1)
        num = str(pin)
        nw = draw.textlength(num, font=F_PIN)
        draw.text((px - nw / 2, py - 4.5), num, font=F_PIN,
                  fill=(255, 255, 255))


def draw_market(draw, x, y, w):
    draw.text((x, y), "MARKETS \u2014 EARLY THURSDAY (REUTERS)", font=F_SEC,
              fill=INK)
    ty = y + 20
    for name, val in MARKET:
        draw.text((x, ty), name, font=F_MKTB, fill=INK)
        vw = draw.textlength(val, font=F_MKT)
        draw.text((x + w - vw, ty), val, font=F_MKT, fill=MUTE)
        ty += 19.5
        draw.line([x, ty - 4, x + w, ty - 4], fill=RULE)


def draw_timeline(draw, y):
    draw.text((MARGIN, y), "THURSDAY IN UTC", font=F_SEC, fill=INK)
    col_w = (CW - 3 * 10) // 4
    ty = y + 18
    for i, (t, text) in enumerate(TIMELINE):
        cx = MARGIN + (i % 4) * (col_w + 10)
        cy = ty + (i // 4) * 36
        draw.text((cx, cy), t, font=F_TL_T, fill=RED)
        lines = wrap(draw, text, F_TL, col_w - 40)
        ly = cy
        for line in lines[:3]:
            draw.text((cx + 40, ly), line, font=F_TL, fill=INK)
            ly += 10.5


def draw_left_out(draw, y):
    draw.rectangle([MARGIN, y, MARGIN + CW, y + 34], fill=(238, 233, 220))
    draw.text((MARGIN + 8, y + 3), "LEFT OUT ON PURPOSE", font=F_TAG,
              fill=RED)
    draw.text((MARGIN + 8, y + 13), "\u2014 big stories, but", font=F_TAG,
              fill=MUTE)
    draw.text((MARGIN + 8, y + 23), "yesterday's, not Thursday's:",
              font=F_TAG, fill=MUTE)
    lines = wrap(draw, LEFT_OUT, F_STRIP, CW - 184)
    ly = y + 6
    for line in lines[:2]:
        draw.text((MARGIN + 176, ly), line, font=F_STRIP, fill=INK)
        ly += 12.5


def draw_briefs(draw, y):
    draw.text((MARGIN, y),
              f"AND THE REST OF THURSDAY \u2014 {len(BRIEFS)} MORE STORIES",
              font=F_SEC, fill=INK)
    col_w = (CW - 16) // 2
    rows = (len(BRIEFS) + 1) // 2
    step = min(18, 272 / max(rows - 1, 1)) if rows > 1 else 13.6
    ty = y + 18
    for i, (region, text) in enumerate(BRIEFS, 1):
        cx = MARGIN + (0 if i <= rows else col_w + 16)
        cy = ty + ((i - 1) % rows) * step
        head = f"{i:02d} {region} \u2014 "
        draw.text((cx, cy), head, font=F_BRIEF_B,
                  fill=REGION_COLORS[region])
        hw = draw.textlength(head, font=F_BRIEF_B)
        draw.text((cx + hw, cy), text, font=F_BRIEF, fill=INK)


def draw_footer(draw):
    draw.line([MARGIN, 988, MARGIN + CW, 988], fill=RULE)
    line1 = ("Sources: Reuters \u00b7 Yonhap \u00b7 Kyodo \u00b7 Xinhua "
             "\u00b7 Al Jazeera \u00b7 BBC \u00b7 Times of Israel \u00b7 "
             "The Hindu \u00b7 Le Monde \u00b7 El Pa\u00eds \u00b7 Wazema "
             "\u00b7 Scoop \u00b7 UEFA \u00b7 per-item detail in "
             "NEWS_SOURCES.md")
    draw.text((MARGIN, 993), line1, font=F_FOOT, fill=MUTE)
    line2 = (f"12 lead stories \u00b7 {len(BRIEFS)} briefs \u00b7 "
             f"{12 + len(BRIEFS)} in all \u00b7 "
             "drawn by render.py for the make.fun news-image-20261126 "
             "contest \u00b7 all dates verified against Thursday 26 "
             "November 2026")
    draw.text((MARGIN, 1006), line2, font=F_FOOT, fill=MUTE)


def render(path):
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    problems = check_layout(draw)
    if problems:
        raise SystemExit("LAYOUT PROBLEMS:\n" + "\n".join(problems))
    draw_header(draw)
    draw_cards(draw, MARGIN, 88)
    draw_map(draw, 718, 88, 292, 212)
    draw_market(draw, 718, 316, 292)
    draw_timeline(draw, 566)
    draw_left_out(draw, 656)
    draw_briefs(draw, 696)
    draw_footer(draw)
    img.save(path, optimize=True)
    return path


if __name__ == "__main__":
    out = os.path.join(HERE, "entry.png")
    render(out)
    data = open(out, "rb").read()
    print(f"entry.png {len(data)} bytes sha256 "
          f"{hashlib.sha256(data).hexdigest()}")
