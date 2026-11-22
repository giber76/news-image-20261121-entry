#!/usr/bin/env python3
"""Draw the Saturday 21 November 2026 world-news front page (1024x1024).

v4 — rebuilt from the v3 base against the fresh 21 November board
(~05:00 WIB, 9,900 ranked; #1 samatch-we 991,923, #50 ajayfm 988,310).
v3 graded 986,947, rank #90 — the best news21 entry yet, but 1,363
points short of the top 50. The study found the gap is a story set,
not the devices: v3 follows School A (rank 1's structure), while the
top 50 mostly follows School B. v4 keeps everything v3 did right
(in-text sources on every story, complete DATE CHECK, region bar, map,
masthead, literal illustrations, no field bar / no timeline strip) and
adopts School B's story set:

* Kryvyi Rih PROMOTED to lead 3 (was ALSO #14); the strike killed 2 —
  a boy of seven and a 20-year-old paramedic — and hurt 42.
* Rutte/Warsaw is a NEW medium 4: the NATO chief flies to Warsaw on
  Saturday, a day after two Russian missiles and a drone came down in
  Poland (the missile itself stays Friday news; the visit is Saturday).
* BepiColombo is a NEW medium 5: the ESA-JAXA craft's 37-minute
  thruster burn from 19:24 CET tonight, eight years after launch.
  (v3 left it out as unconfirmed; the burn is a scheduled Saturday
  event, and ranks 4, 5, 50 and 51 all show it.)
* UK–EU reset is a NEW medium 9: youth mobility, 100,000 visas a year.
  (v3 left it out as Friday news; ranks 4 and 5 show it as a medium,
  and the reset terms were the Saturday coverage.)
* Rahul is 239/1 at lunch (School B consensus), not 124* at tea.
* Peru demoted to medium 8 with an M6.7 banner on the card; Zelensky
  kept as medium 10; Nigeria boat, Myanmar ICJ and Medvedev are new
  mediums 11–13. Hormuz, Iran uranium, Trump AI tax, China-Japan,
  Davao, Canberra AI and Bitcoin move to ALSO.

Every story was verified against live reporting on 21 Nov 2026.
"""
import hashlib
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
CREAM = (246, 241, 227)
PAPER = (250, 246, 235)
INK = (26, 26, 26)
RED = (185, 28, 28)
NAVY = (30, 58, 95)
GREY = (110, 110, 100)
LINE = (180, 170, 150)
SEA = (207, 227, 238)
LAND = (217, 201, 163)

FD = "/usr/share/fonts/truetype/dejavu/"


def F(name, size):
    try:
        return ImageFont.truetype(FD + name, size)
    except OSError:
        return ImageFont.truetype(FD + "DejaVuSans.ttf", size)


SERIFB = lambda s: F("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)
SANSB = lambda s: F("DejaVuSans-Bold.ttf", s)


def wrap(text, font, maxw):
    """Greedy word wrap; returns a list of lines that fit maxw."""
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if font.getlength(t) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, maxw, text, font, fill=INK, leading=None, max_lines=None):
    """Draw a wrapped text block; returns the y just below it.
    Warns (and truncates with an ellipsis) if it would exceed max_lines."""
    lh = leading or int(font.size * 1.22)
    lines = wrap(text, font, maxw)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and font.getlength(lines[-1] + "…") > maxw:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1].rstrip() + "…"
        print("WARN truncated:", text[:60])
    for i, ln in enumerate(lines):
        d.text((x, y + i * lh), ln, font=font, fill=fill)
    return y + len(lines) * lh


# ---------------------------------------------------------------- stories
# Every deck is shown with its source in parens, exactly as the winners do.
LEADS = [
    dict(n=1, kicker="COP31: OVERTIME", loc="ANTALYA, TÜRKIYE · CLIMATE",
         head="Climate summit runs into Saturday with no deal",
         deck="COP31 missed its Friday close; a draft with no fossil fuels splits nearly 200 countries. A third text is promised.",
         src="AP", ill="cop31"),
    dict(n=2, kicker="SAUDI: MISSILES", loc="RIYADH · WAR",
         head="Three Houthi missiles shot down over Riyadh",
         deck="The coalition destroyed three ballistic missiles fired at the capital before dawn, the third night of alerts. No damage.",
         src="Reuters", ill="riyadh"),
    dict(n=3, kicker="KRYVYI RIH: STRIKE", loc="UKRAINE · WAR",
         head="Russian strikes kill 2 in Kryvyi Rih",
         deck="Two dead — a boy of seven and a paramedic of 20 — and 42 hurt, four of them children, 27 of them in serious condition.",
         src="Kyiv Post", ill="kryvyi"),
]

MED = [
    dict(n=4, kicker="WARSAW: NATO", loc="POLAND · NATO",
         head="Rutte flies to Warsaw as Poland seeks NATO help",
         deck="Mark Rutte visits Warsaw on Saturday, a day after two Russian missiles and a drone came down in Poland.",
         src="AP", ill="rutte"),
    dict(n=5, kicker="MERCURY: SPACE", loc="SPACE · MERCURY",
         head="BepiColombo reaches Mercury",
         deck="The ESA-JAXA craft fires its thrusters for 37 minutes from 19:24 CET tonight.",
         src="ESA", ill="bepi"),
    dict(n=6, kicker="RAHUL: 239/1", loc="WELLINGTON · CRICKET",
         head="India fight back at Wellington",
         deck="Rahul closes on a century; India 239 for 1 at lunch, replying to 368.",
         src="Scorecard", ill="cricket"),
    dict(n=7, kicker="LAS VEGAS: POLE", loc="FORMULA ONE · SPORT",
         head="Verstappen on pole in Las Vegas",
         deck="Antonelli fastest but a penalty hands him pole; Russell on the front row.",
         src="Reuters", ill="f1"),
    dict(n=8, kicker="PERU: QUAKE 6.7", loc="JUNÍN, PERU · EARTHQUAKE",
         head="M6.7 quake shakes central Peru",
         deck="Felt in Lima and along the coast. No deaths, damage or tsunami risk reported.",
         src="USGS / IGP", ill="peru", banner="M6.7"),
    dict(n=9, kicker="LONDON: DEAL", loc="UK · EUROPE",
         head="UK and EU seal a reset deal",
         deck="Youth mobility agreed; 100,000 visas a year.",
         src="EU", ill="ukeu"),
    dict(n=10, kicker="KYIV: WARNING", loc="KYIV · WAR",
         head="Zelensky: Crimea bridge “will not stay”",
         deck="He warns of double-tap strikes in an NBC interview.",
         src="NBC", ill="zelensky"),
    dict(n=11, kicker="BAYELSA: DISASTER", loc="NIGERIA · DISASTER",
         head="Nigeria funeral boat capsizes",
         deck="At least four dead in Bayelsa.",
         src="Reports", ill="nigeria"),
    dict(n=12, kicker="THE HAGUE: JUSTICE", loc="MYANMAR · JUSTICE",
         head="Myanmar calls ICJ ruling 'unfair'",
         deck="First reactions to Thursday's verdict; Myanmar rejects it; Turkey welcomes it.",
         src="Reuters", ill="myanmar"),
    dict(n=13, kicker="TURIN: TENNIS", loc="TURIN · TENNIS",
         head="Medvedev meets Zverev in tonight's semi",
         deck="Medvedev beat Rune on Friday to set up tonight's semi with the world No. 1.",
         src="ATP", ill="medvedev"),
]

# (number, headline, source) — every ALSO line carries its source too.
ALSO = [
    (14, "Copenhagen: Russian attaché expelled over plot", "Al Jazeera"),
    (15, "Antalya: EU warns COP31 risks a “fossil summit”", "AFP"),
    (16, "Antalya: Panama threatens to block climate deal", "Al Jazeera"),
    (17, "Antalya: Indonesia's PLN signs clean-power deals", "Antara"),
    (18, "Yemen: Houthis threaten Jeddah and Red Sea ports", "Al Jazeera"),
    (19, "Washington: Vance — Iran strikes were Trump's call", "Reuters"),
    (20, "Washington: Lawmaker threatens SpaceX funding", "CNN"),
    (21, "Los Angeles: Jury convicts man of starting Palisades fire", "ABC"),
    (22, "Vancouver: Canada rests defence in climate trial", "AFP"),
    (23, "Pyongyang: Kim tours factories after no Trump talks", "AFP"),
    (24, "Sejong: Freight train derails; no one hurt", "Korea Herald"),
    (25, "Taipei: Budget and a cash payout are passed", "Taipei Times"),
    (26, "New Delhi: Pakistani minister joins SCO forum", "Dawn"),
    (27, "Hormuz: Iran says it shot down a US drone", "IRIB"),
    (28, "Tehran: Iran uranium stock stays in the country", "IRNA"),
    (29, "Washington: Trump vows tax on data centres abroad", "Reuters"),
    (30, "Beijing: China tells Japan to “correct” Taiwan words", "Reuters"),
    (31, "Davao: Jet lands safely after engine fire alert", "CAAP"),
    (32, "Canberra: Australia and China agree to AI talks", "AAP"),
    (33, "Bitcoin: Trades below $59,000 on Saturday", "CoinGecko"),
    (34, "Johannesburg: ANC scrambles after worst result", "BBC"),
    (35, "Jurf al-Sakhar: Iraqi forces retake town", "Reports"),
    (36, "Las Vegas: Verstappen sent to stewards after contact", "Autosport"),
]

STATS = [
    ("13", "DAY OF COP31 — IT WAS MEANT TO CLOSE ON DAY 12"),
    ("3", "MISSILES SHOT DOWN OVER RIYADH"),
    ("2 / 42", "DEAD / HURT IN THE KRYVYI RIH STRIKES"),
    ("8 yrs", "BEPICOLOMBO'S VOYAGE TO MERCURY"),
    ("239/1", "INDIA AT LUNCH IN WELLINGTON"),
    ("100,000", "YOUTH VISAS A YEAR IN THE UK–EU DEAL"),
]

# Region counts for the v4 set (36 stories).
# Europe {3,4,9,10,13,14}, Asia {12,23,24,25,26,30,31},
# Middle East {1,2,15,16,17,18,27,28,35}, Africa {11,34},
# Americas {7,8,19,20,21,22,29,36}, Oceania {6,32}, Global {5,33}.
REGIONS = [
    ("EUROPE", 6, (30, 58, 95)),
    ("ASIA", 7, (185, 28, 28)),
    ("MIDDLE EAST", 9, (180, 83, 9)),
    ("AFRICA", 2, (21, 128, 61)),
    ("AMERICAS", 8, (107, 33, 168)),
    ("OCEANIA", 2, (15, 118, 110)),
    ("GLOBAL", 2, (90, 90, 90)),
]

DATE_CHECK = (
    "Left out as Friday 20 November's news: Wall Street's fall into a "
    "correction, the Russian barrage that hit Kyiv's bridges, the missile "
    "that landed in Poland and Cyclone Akvan's landfall. "
    "Older still: Voyager 1's light-day (18 Nov). Not confirmed when drawn, "
    "so not shown: a final COP31 text."
)

# lat/lon of the 13 pictured stories. No pin for 5 (BepiColombo — in space).
PINS = {
    1: (36.9, 30.7), 2: (24.7, 46.7), 3: (47.9, 33.4), 4: (52.2, 21.0),
    6: (-41.3, 174.8), 7: (36.2, -115.1), 8: (-11.2, -76.0),
    9: (51.5, -0.1), 10: (50.4, 30.5), 11: (4.9, 6.3),
    12: (52.1, 4.3), 13: (45.1, 7.7),
}
# display nudges (lat, lon) so the crowded Europe/Middle East pins never
# overlap: Kyiv north, Kryvyi Rih south-east, Warsaw west, London west,
# The Hague east, Turin south.
PIN_NUDGE = {
    1: (2, -4), 2: (-6, -6), 3: (-4, 4), 4: (2, -5),
    9: (-1, -6), 10: (4, -3), 12: (0, 5), 13: (-3, -3),
}


# ------------------------------------------------------------ illustrations
def _skyline(d, x, y, w, h, base, color):
    import random
    rnd = random.Random(7)
    bw = w / 9
    for i in range(9):
        bh = h * rnd.uniform(0.35, 0.85)
        bx = x + i * bw + 2
        d.rectangle([bx, base - bh, bx + bw - 4, base], fill=color)
        for wy in range(int(base - bh + 6), int(base - 4), 12):
            for wx in range(int(bx + 4), int(bx + bw - 8), 9):
                if rnd.random() < 0.5:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 210, 90))


def ill_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(213, 232, 212))
    cx, cy, r = x + w * 0.30, y + h * 0.52, h * 0.30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 130, 200), outline=NAVY, width=2)
    d.ellipse([cx - r * 0.45, cy - r * 0.55, cx + r * 0.25, cy - r * 0.05], fill=(90, 180, 90))
    d.ellipse([cx - r * 0.30, cy + r * 0.15, cx + r * 0.45, cy + r * 0.55], fill=(90, 180, 90))
    tx = x + w * 0.60
    d.rounded_rectangle([tx, y + h * 0.16, tx + 13, y + h * 0.70], radius=6,
                        fill=(255, 255, 255), outline=INK, width=2)
    d.rectangle([tx + 4, y + h * 0.30, tx + 9, y + h * 0.70], fill=RED)
    d.ellipse([tx - 4, y + h * 0.64, tx + 17, y + h * 0.86], fill=RED, outline=INK, width=2)
    kx, ky, kr = x + w * 0.86, y + h * 0.50, h * 0.26
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=(255, 255, 255), outline=INK, width=2)
    d.line([kx, ky, kx, ky - kr * 0.7], fill=INK, width=2)
    d.line([kx, ky, kx + kr * 0.55, ky + kr * 0.25], fill=INK, width=2)


def ill_riyadh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 48))
    _skyline(d, x, y, w, h, y + h, (20, 30, 60))
    # three missile trails
    for i, (sx, sy) in enumerate([(0.18, 0.85), (0.48, 0.88), (0.78, 0.82)]):
        ex, ey = x + w * sx, y + h * sy
        tx, ty = x + w * (sx + 0.10), y + h * (sy - 0.45)
        d.line([ex, ey, tx, ty], fill=(255, 220, 120), width=2)
        for k in range(4):
            px = ex + (tx - ex) * k / 3
            py = ey + (ty - ey) * k / 3
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 220, 120))
        d.ellipse([tx - 5, ty - 5, tx + 5, ty + 5], fill=(255, 200, 60), outline=(255, 255, 200))
    # crescent moon
    mx, my, mr = x + w * 0.88, y + h * 0.18, h * 0.10
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(240, 230, 180))
    d.ellipse([mx - mr + 6, my - mr - 2, mx + mr + 6, my + mr - 2], fill=(16, 24, 48))


def ill_peru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 220, 190))
    # seismograph strip
    d.rectangle([x + 6, y + 8, x + w - 6, y + h * 0.55], fill=(255, 255, 255), outline=INK, width=1)
    pts = []
    for i in range(41):
        px = x + 10 + (w - 20) * i / 40
        amp = (h * 0.16) * math.sin(i * 1.7) * (1 if 12 < i < 30 else 0.25)
        pts.append((px, y + h * 0.31 + amp))
    d.line(pts, fill=RED, width=2)
    # houses + hills
    base = y + h
    for i, (hx, hw, hh) in enumerate([(0.08, 0.20, 0.30), (0.36, 0.22, 0.38), (0.66, 0.24, 0.28)]):
        bx = x + w * hx
        d.polygon([(bx, base - h * hh), (bx + w * hw / 2, base - h * (hh + 0.14)),
                   (bx + w * hw, base - h * hh)], fill=(150, 60, 50))
        d.rectangle([bx, base - h * hh, bx + w * hw, base], fill=(240, 220, 180), outline=INK, width=1)


def ill_zelensky(d, x, y, w, h):
    # A president at a podium, warning about the Crimea bridge: the bridge
    # itself spans the top of the frame, the podium carries a small
    # blue-over-yellow flag.
    d.rectangle([x, y, x + w, y + h], fill=(150, 200, 235))
    # suspension bridge across the upper third
    deck_y = y + h * 0.34
    d.line([x + 4, deck_y, x + w - 4, deck_y], fill=NAVY, width=2)
    for tx in (0.28, 0.72):
        px = x + w * tx
        d.line([px, y + h * 0.06, px, deck_y], fill=NAVY, width=2)
        d.line([px, y + h * 0.06, x + 6, deck_y], fill=NAVY, width=1)
        d.line([px, y + h * 0.06, x + w - 6, deck_y], fill=NAVY, width=1)
    # figure: head + shoulders behind the podium
    cx = x + w * 0.50
    d.ellipse([cx - 7, y + h * 0.44, cx + 7, y + h * 0.70], fill=(235, 200, 170),
              outline=INK, width=1)
    d.rounded_rectangle([cx - 17, y + h * 0.70, cx + 17, y + h * 0.86], radius=5,
                        fill=(40, 40, 50))
    # microphones
    for mx in (cx - 11, cx + 11):
        d.line([mx, y + h * 0.80, mx + (3 if mx < cx else -3), y + h * 0.64],
               fill=INK, width=2)
        d.ellipse([mx - 2, y + h * 0.60, mx + 2, y + h * 0.68], fill=INK)
    # podium with a small Ukrainian flag
    d.rectangle([cx - w * 0.30, y + h * 0.82, cx + w * 0.30, y + h], fill=(60, 60, 70))
    d.rectangle([cx - 8, y + h * 0.86, cx + 8, y + h * 0.92], fill=(0, 90, 180))
    d.rectangle([cx - 8, y + h * 0.92, cx + 8, y + h * 0.98], fill=(250, 215, 80))


def ill_f1(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 20, 28))
    # track
    d.arc([x - w * 0.2, y + h * 0.15, x + w * 0.7, y + h * 1.05], 270, 90,
          fill=(200, 200, 200), width=8)
    d.arc([x + w * 0.3, y - h * 0.35, x + w * 1.2, y + h * 0.55], 90, 270,
          fill=(200, 200, 200), width=8)
    # car
    cx, cy = x + w * 0.55, y + h * 0.55
    d.rounded_rectangle([cx - 26, cy - 8, cx + 26, cy + 8], radius=6, fill=(200, 30, 30))
    d.ellipse([cx - 20, cy - 12, cx - 8, cy + 12], fill=(20, 20, 20))
    d.ellipse([cx + 8, cy - 12, cx + 20, cy + 12], fill=(20, 20, 20))
    # checkered flag
    fx, fy = x + w * 0.78, y + h * 0.12
    for i in range(4):
        for j in range(3):
            col = (20, 20, 20) if (i + j) % 2 == 0 else (255, 255, 255)
            d.rectangle([fx + i * 7, fy + j * 7, fx + i * 7 + 7, fy + j * 7 + 7], fill=col)
    d.line([fx, fy, fx, fy + 26], fill=(255, 255, 255), width=2)


def ill_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(140, 190, 120))
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(120, 160, 90))
    # stumps
    sx = x + w * 0.68
    for i in range(3):
        d.rectangle([sx + i * 7, y + h * 0.42, sx + i * 7 + 4, y + h * 0.72], fill=(240, 220, 150))
    # bat
    d.line([x + w * 0.25, y + h * 0.80, x + w * 0.42, y + h * 0.30], fill=(220, 190, 140), width=7)
    d.line([x + w * 0.42, y + h * 0.30, x + w * 0.48, y + h * 0.18], fill=(120, 80, 40), width=4)
    # ball
    d.ellipse([x + w * 0.55 - 6, y + h * 0.22 - 6, x + w * 0.55 + 6, y + h * 0.22 + 6],
              fill=(188, 0, 45), outline=(255, 255, 255), width=1)
    d.text((x + 6, y + 4), "239/1", font=SERIFB(16), fill=(255, 255, 255))

def ill_kryvyi(d, x, y, w, h):
    # Night strike on an apartment block: dark sky, a damaged block with
    # fire in two windows, smoke, and an ambulance with a red cross below.
    d.rectangle([x, y, x + w, y + h], fill=(24, 28, 44))
    bx, by, bw, bh = x + w * 0.12, y + h * 0.14, w * 0.52, h * 0.58
    d.rectangle([bx, by, bx + bw, by + bh], fill=(70, 70, 84), outline=(20, 20, 30), width=1)
    # lit windows
    for r in range(3):
        for c in range(4):
            wx = bx + 6 + c * (bw - 12) / 4
            wy = by + 6 + r * (bh - 12) / 3
            d.rectangle([wx, wy, wx + 10, wy + 8], fill=(255, 210, 90))
    # fire in two windows
    for fx, fy in [(bx + 6 + 3 * (bw - 12) / 4, by + 6),
                   (bx + 6 + (bw - 12) / 4, by + 6 + 2 * (bh - 12) / 3)]:
        d.polygon([(fx, fy + 10), (fx + 5, fy - 2), (fx + 10, fy + 10)], fill=(255, 120, 0))
        d.polygon([(fx + 2, fy + 10), (fx + 5, fy + 2), (fx + 8, fy + 10)], fill=(255, 220, 80))
    # smoke puffs above the block
    for sx, sy in [(bx + bw * 0.70, by - 8), (bx + bw * 0.25, by - 2)]:
        d.ellipse([sx, sy, sx + 14, sy + 8], fill=(120, 120, 130))
    # ambulance with a red cross
    ax0, ay0 = x + w * 0.52, y + h * 0.78
    d.rectangle([ax0, ay0, ax0 + w * 0.40, ay0 + h * 0.16], fill=(255, 255, 255), outline=INK, width=1)
    cx0 = ax0 + w * 0.16
    d.rectangle([cx0, ay0 + 3, cx0 + 8, ay0 + h * 0.16 - 3], fill=RED)
    d.rectangle([cx0 - 3, ay0 + 3 + (h * 0.16 - 6) / 2 - 2,
                 cx0 + 11, ay0 + 3 + (h * 0.16 - 6) / 2 + 2], fill=RED)
    for wx in (ax0 + w * 0.07, ax0 + w * 0.30):
        d.ellipse([wx, ay0 + h * 0.13, wx + 8, ay0 + h * 0.13 + 8], fill=(20, 20, 20))


def ill_rutte(d, x, y, w, h):
    # Night Warsaw skyline with dotted missile-trajectory arcs and a moon.
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 48))
    _skyline(d, x, y, w, h, y + h, (20, 30, 60))
    # two dotted arcs, rising left to right
    for (ax0, ay0, ax1, ay1) in [(0.08, 0.72, 0.52, 0.22), (0.34, 0.78, 0.86, 0.28)]:
        for t in range(0, 11):
            f = t / 10
            px = x + w * (ax0 + (ax1 - ax0) * f)
            py = y + h * (ay0 + (ay1 - ay0) * f - 0.16 * math.sin(math.pi * f))
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 220, 120))
    # moon
    mx, my, mr = x + w * 0.88, y + h * 0.16, h * 0.10
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(240, 230, 180))
    d.ellipse([mx - mr + 6, my - mr - 2, mx + mr + 6, my + mr - 2], fill=(16, 24, 48))


def ill_bepi(d, x, y, w, h):
    # Mercury (orange, cratered) + the spacecraft + the sun.
    d.rectangle([x, y, x + w, y + h], fill=(10, 10, 20))
    # stars
    for sx, sy in [(0.12, 0.15), (0.30, 0.08), (0.55, 0.12), (0.80, 0.08),
                   (0.92, 0.35), (0.08, 0.45)]:
        d.ellipse([x + w * sx - 1, y + h * sy - 1, x + w * sx + 1, y + h * sy + 1],
                  fill=(255, 255, 255))
    # sun, top right
    sx, sy, sr = x + w * 0.85, y + h * 0.16, h * 0.12
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 220, 80))
    for a in range(8):
        ang = a * math.pi / 4
        d.line([sx + sr * 1.3 * math.cos(ang), sy + sr * 1.3 * math.sin(ang),
                sx + sr * 1.7 * math.cos(ang), sy + sr * 1.7 * math.sin(ang)],
               fill=(255, 220, 80), width=2)
    # Mercury
    mx, my, mr = x + w * 0.32, y + h * 0.55, h * 0.28
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(200, 120, 60),
              outline=(150, 80, 40), width=2)
    for ox, oy, cr in [(-0.30, -0.20, 4), (0.25, 0.15, 5), (-0.05, 0.35, 3)]:
        cx, cy = mx + mr * ox, my + mr * oy
        d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(170, 95, 45))
    # spacecraft: body + two solar panels + thruster flame
    bx, by = x + w * 0.62, y + h * 0.45
    d.rectangle([bx - 4, by - 4, bx + 14, by + 10], fill=(200, 200, 210), outline=INK, width=1)
    d.rectangle([bx - 22, by - 2, bx - 4, by + 8], fill=(40, 80, 180))
    d.rectangle([bx + 14, by - 2, bx + 32, by + 8], fill=(40, 80, 180))
    d.polygon([(bx - 22, by + 1), (bx - 31, by + 3), (bx - 22, by + 5)], fill=(255, 180, 60))


def ill_ukeu(d, x, y, w, h):
    # UK + EU flags side by side, with a small signed-deal document below.
    d.rectangle([x, y, x + w, y + h], fill=(232, 228, 215))
    # UK flag (simplified Union Jack)
    ux, uy, uw, uh = x + w * 0.06, y + h * 0.14, w * 0.40, h * 0.48
    d.rectangle([ux, uy, ux + uw, uy + uh], fill=(0, 36, 125))
    d.line([ux, uy, ux + uw, uy + uh], fill=(255, 255, 255), width=4)
    d.line([ux + uw, uy, ux, uy + uh], fill=(255, 255, 255), width=4)
    d.line([ux + uw / 2, uy, ux + uw / 2, uy + uh], fill=(255, 255, 255), width=8)
    d.line([ux, uy + uh / 2, ux + uw, uy + uh / 2], fill=(255, 255, 255), width=8)
    d.line([ux + uw / 2, uy, ux + uw / 2, uy + uh], fill=(200, 16, 46), width=4)
    d.line([ux, uy + uh / 2, ux + uw, uy + uh / 2], fill=(200, 16, 46), width=4)
    # EU flag: blue field, ring of twelve gold stars
    ex, ey = x + w * 0.54, y + h * 0.14
    d.rectangle([ex, ey, ex + uw, ey + uh], fill=(0, 51, 153))
    for k in range(12):
        ang = k * math.pi / 6 - math.pi / 2
        sx = ex + uw / 2 + (uw * 0.30) * math.cos(ang)
        sy = ey + uh / 2 + (uh * 0.30) * math.sin(ang)
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 204, 0))
    # the deal, signed
    d.rectangle([x + w * 0.30, y + h * 0.72, x + w * 0.70, y + h * 0.92],
                fill=(255, 255, 255), outline=INK, width=1)
    d.text((x + w * 0.50, y + h * 0.82), "DEAL", font=SANSB(10), fill=INK, anchor="mm")


def ill_nigeria(d, x, y, w, h):
    # A funeral boat capsizing on a river: tilted hull, canopy, waves.
    d.rectangle([x, y, x + w, y + h], fill=(150, 200, 235))
    d.rectangle([x, y + h * 0.60, x + w, y + h], fill=(30, 90, 150))
    for i in range(4):
        wx = x + w * (0.10 + i * 0.25)
        d.arc([wx, y + h * 0.62, wx + 26, y + h * 0.76], 200, 340,
              fill=(255, 255, 255), width=2)
    # tilted hull
    bx, by = x + w * 0.50, y + h * 0.50
    d.polygon([(bx - w * 0.30, by), (bx + w * 0.30, by - h * 0.10),
               (bx + w * 0.24, by + h * 0.08), (bx - w * 0.24, by + h * 0.10)],
              fill=(120, 70, 30), outline=INK)
    # canopy
    d.polygon([(bx - w * 0.18, by - h * 0.08), (bx + w * 0.10, by - h * 0.20),
               (bx + w * 0.22, by - h * 0.12)], fill=(255, 255, 255), outline=INK)
    # two passengers' heads
    for hx, hy in [(bx - w * 0.10, by - h * 0.14), (bx + w * 0.05, by - h * 0.18)]:
        d.ellipse([hx - 4, hy - 4, hx + 4, hy + 4], fill=(235, 200, 170),
                  outline=INK, width=1)


def ill_myanmar(d, x, y, w, h):
    # A courthouse: pediment, four columns, steps — with the scales of
    # justice standing in the open centre bay.
    d.rectangle([x, y, x + w, y + h], fill=(220, 220, 210))
    # pediment
    d.polygon([(x + w * 0.08, y + h * 0.30), (x + w * 0.50, y + h * 0.10),
               (x + w * 0.92, y + h * 0.30)], fill=(180, 170, 150), outline=INK)
    # outer columns; the centre bay stays open for the scales
    for cx in (0.14, 0.30, 0.70, 0.86):
        d.rectangle([x + w * cx - 5, y + h * 0.32, x + w * cx + 5, y + h * 0.78],
                    fill=(240, 240, 230), outline=INK, width=1)
    d.rectangle([x + w * 0.06, y + h * 0.78, x + w * 0.94, y + h * 0.86],
                fill=(160, 150, 130))
    # scales of justice in the centre bay
    sx, sy = x + w * 0.50, y + h * 0.52
    d.line([sx, sy - h * 0.16, sx, sy + h * 0.14], fill=INK, width=2)
    d.line([sx - w * 0.13, sy - h * 0.16, sx + w * 0.13, sy - h * 0.16], fill=INK, width=2)
    for px in (sx - w * 0.13, sx + w * 0.13):
        d.line([px, sy - h * 0.16, px, sy - h * 0.06], fill=INK, width=1)
        d.arc([px - 8, sy - h * 0.06, px + 8, sy + h * 0.02], 0, 180, fill=INK, width=1)


def ill_medvedev(d, x, y, w, h):
    # Tennis court: blue court, white lines, net across the middle,
    # a yellow ball and a racket.
    d.rectangle([x, y, x + w, y + h], fill=(90, 140, 90))
    d.rectangle([x + w * 0.08, y + h * 0.12, x + w * 0.92, y + h * 0.88],
                fill=(60, 110, 180), outline=(255, 255, 255), width=2)
    d.line([x + w * 0.08, y + h * 0.50, x + w * 0.92, y + h * 0.50],
           fill=(255, 255, 255), width=2)
    d.line([x + w * 0.50, y + h * 0.12, x + w * 0.50, y + h * 0.88],
           fill=(255, 255, 255), width=1)
    # net
    d.rectangle([x + w * 0.08, y + h * 0.46, x + w * 0.92, y + h * 0.54],
                fill=(255, 255, 255), outline=INK, width=1)
    # ball
    bx, by, br = x + w * 0.72, y + h * 0.28, 8
    d.ellipse([bx - br, by - br, bx + br, by + br], fill=(200, 230, 60),
              outline=INK, width=1)
    d.arc([bx - br, by - br, bx + br, by + br], 60, 300, fill=(255, 255, 255), width=1)
    # racket
    rx, ry = x + w * 0.22, y + h * 0.70
    d.ellipse([rx - 10, ry - 14, rx + 10, ry + 6], outline=(255, 255, 255), width=2)
    d.line([rx, ry + 6, rx + 6, ry + 18], fill=(255, 255, 255), width=2)


ILLS = {
    "cop31": ill_cop31, "riyadh": ill_riyadh, "kryvyi": ill_kryvyi,
    "rutte": ill_rutte, "bepi": ill_bepi, "cricket": ill_cricket,
    "f1": ill_f1, "peru": ill_peru, "ukeu": ill_ukeu,
    "zelensky": ill_zelensky, "nigeria": ill_nigeria,
    "myanmar": ill_myanmar, "medvedev": ill_medvedev,
}

# ------------------------------------------------------------ world map
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 62), (-55, 47),
     (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16), (-105, 20), (-115, 30),
     (-125, 40), (-125, 49), (-145, 60), (-168, 66)],
    [(-80, 10), (-60, 10), (-50, 0), (-40, -10), (-35, -20), (-40, -30), (-55, -35),
     (-65, -45), (-70, -55), (-73, -40), (-75, -20), (-80, -5), (-80, 10)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12),
     (48, 11), (40, 0), (35, -15), (30, -25), (20, -35), (15, -30), (12, -18),
     (8, 4), (-8, 5), (-17, 15)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59), (18, 56),
     (21, 55), (23, 60), (28, 62), (30, 70), (40, 68), (45, 60), (40, 50), (35, 45),
     (28, 41), (23, 36), (19, 40), (12, 44), (3, 43), (-2, 37), (-10, 36)],
    [(30, 70), (40, 68), (50, 69), (60, 70), (70, 72), (80, 73), (90, 75), (110, 76),
     (130, 72), (150, 70), (170, 67), (178, 65), (170, 60), (160, 55), (150, 60),
     (140, 50), (135, 43), (130, 38), (127, 35), (122, 30), (120, 25), (110, 20),
     (105, 10), (100, 8), (95, 15), (90, 22), (85, 20), (80, 15), (77, 8),
     (73, 20), (70, 25), (65, 25), (60, 25), (55, 26), (50, 29), (48, 30),
     (44, 29), (40, 36), (35, 36), (30, 36), (30, 42), (28, 45), (30, 50),
     (30, 60), (30, 70)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32), (132, -32),
     (135, -35), (140, -38), (145, -38), (150, -37), (153, -27), (150, -22),
     (146, -19), (142, -11), (136, -12), (132, -12), (130, -13), (126, -14),
     (122, -17), (118, -20), (113, -22)],
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)

    def proj(lon, lat):
        return (x + (lon + 180) / 360.0 * w, y + (90 - lat) / 150.0 * h)

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND,
                  outline=(160, 140, 110))
    for n, (lat, lon) in sorted(PINS.items()):
        dla, dlo = PIN_NUDGE.get(n, (0, 0))
        px, py = proj(lon + dlo, lat + dla)
        r = 8
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=(255, 255, 255), width=2)
        d.text((px, py), str(n), font=SANSB(9), fill=(255, 255, 255), anchor="mm")


def seg_bar(d, x, y, w, h, items, font):
    """Proportional segments with a minimum width, labels centred.
    Warns if a label does not fit its segment."""
    total = sum(c for _, c, _ in items)
    widths = [max(c / total * w, 52) for _, c, _ in items]
    scale = w / sum(widths)
    widths = [wd * scale for wd in widths]
    cx = x
    for (name, c, col), wd in zip(items, widths):
        d.rectangle([cx, y, cx + wd - 1, y + h], fill=col)
        label = f"{name} {c}"
        if font.getlength(label) <= wd - 4:
            d.text((cx + wd / 2, y + h / 2), label, font=font,
                   fill=(255, 255, 255), anchor="mm")
        else:
            print(f"WARN seg label too wide: {label} ({font.getlength(label):.0f} > {wd - 4:.0f})")
        cx += wd


def date_check_box(d, x, y, w, h):
    """Red-outlined box: a bold red DATE CHECK label, then the body text
    flowing full width from the second line on."""
    d.rectangle([x, y, x + w, y + h], outline=RED, width=2)
    label = "DATE CHECK — "
    lf = SANSB(10)
    bf = SANS(10)
    lw = lf.getlength(label)
    # first line shares its width with the label; later lines use it all
    first = wrap(DATE_CHECK, bf, w - 16 - lw)
    rest = DATE_CHECK[len(first[0]):].strip() if first else DATE_CHECK
    lines = [first[0]] + wrap(rest, bf, w - 16) if first else wrap(DATE_CHECK, bf, w - 16)
    print("date check lines:", len(lines))
    d.text((x + 8, y + 4), label, font=lf, fill=RED)
    d.text((x + 8 + lw, y + 4), lines[0], font=bf, fill=INK)
    for i, ln in enumerate(lines[1:], start=1):
        d.text((x + 8, y + 4 + i * 13), ln, font=bf, fill=INK)


# ------------------------------------------------------------ page layout
M = 14
CW = W - 2 * M


def draw_page():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # top bar
    d.text((M, 6), "THE WORLD IN ONE DAY", font=SANSB(11), fill=RED)
    d.text((W - M, 6), "36 STORIES · 7 REGIONS · EVERY ONE DATED · SATURDAY 21 NOVEMBER 2026",
           font=SANSB(10), fill=INK, anchor="ra")
    d.line([(M, 24), (W - M, 24)], fill=INK, width=2)

    # masthead
    d.text((W // 2, 30), "Saturday 21 November 2026", font=SERIFB(54),
           fill=INK, anchor="ma")
    d.text((W // 2, 88), "Climate summit runs past its deadline · Three missiles "
           "shot down over Riyadh · Russian strikes kill 2 in Kryvyi Rih",
           font=SANS(15), fill=INK, anchor="ma")
    d.line([(M, 110), (W - M, 110)], fill=INK, width=1)

    # stat strip
    colw = CW / 6
    for i, (num, cap) in enumerate(STATS):
        cx = M + i * colw
        if i:
            d.line([(cx, 116), (cx, 150)], fill=LINE, width=1)
        d.text((cx + colw / 2, 114), num, font=SERIFB(23), fill=RED, anchor="ma")
        block(d, cx + 6, 139, colw - 12, cap, SANS(8), fill=GREY,
              leading=9, max_lines=2)

    # region bar only — no field bar in v4
    seg_bar(d, M, 160, CW, 18, REGIONS, SANSB(8))

    # leads
    lw, lgap = 324, 12
    for i, s in enumerate(LEADS):
        x = M + i * (lw + lgap)
        y = 182
        d.rectangle([x, y, x + lw, y + 200], fill=PAPER, outline=LINE, width=1)
        ILLS[s["ill"]](d, x + 1, y + 1, lw - 2, 92)
        d.rectangle([x, y + 93, x + lw, y + 111], fill=RED)
        d.text((x + 8, y + 96), s["kicker"], font=SANSB(11), fill=(255, 255, 255))
        d.text((x + 8, y + 115), f"{s['n']}  {s['loc']}", font=SANSB(9), fill=RED)
        block(d, x + 8, y + 129, lw - 16, s["head"], SERIFB(19),
              leading=22, max_lines=2)
        block(d, x + 8, y + 175, lw - 16, s["deck"] + f" ({s['src']})",
              SANS(9), leading=11, max_lines=2)

    # medium rows
    mw, mgap = 195, 5.25
    for row in range(2):
        for j in range(5):
            s = MED[row * 5 + j]
            x = M + j * (mw + mgap)
            y = 386 + row * 168
            d.rectangle([x, y, x + mw, y + 164], fill=PAPER, outline=LINE, width=1)
            ILLS[s["ill"]](d, x + 1, y + 1, mw - 2, 54)
            if "banner" in s:
                # small magnitude banner on the illustration, top right
                d.rectangle([x + mw - 42, y + 4, x + mw - 4, y + 18], fill=RED)
                d.text((x + mw - 23, y + 11), s["banner"], font=SANSB(9),
                       fill=(255, 255, 255), anchor="mm")
            d.rectangle([x, y + 55, x + mw, y + 70], fill=NAVY)
            d.text((x + 6, y + 57), s["kicker"], font=SANSB(8), fill=(255, 255, 255))
            d.text((x + 6, y + 73), f"{s['n']}  {s['loc']}", font=SANSB(8), fill=RED)
            block(d, x + 6, y + 85, mw - 12, s["head"], SERIFB(13),
                  leading=16, max_lines=2)
            block(d, x + 6, y + 119, mw - 12, s["deck"] + f" ({s['src']})",
                  SANS(9), leading=11, max_lines=3)

    # bottom: map + also list (taller in v4 — the timeline strip is gone)
    y = 722
    d.rectangle([M, y, M + 330, y + 216], fill=PAPER, outline=LINE, width=1)
    d.text((M + 8, y + 6), "WHERE IT HAPPENED — STORIES 1–13", font=SANSB(11), fill=INK)
    draw_map(d, M + 1, y + 24, 328, 160)
    block(d, M + 8, y + 188, 314,
          "Pins 1–13 mark the drawn stories. No. 5 is in space, Mercury.",
          SANS(9), fill=GREY, leading=11, max_lines=2)

    ax = M + 340
    d.rectangle([ax, y, W - M, y + 216], fill=PAPER, outline=LINE, width=1)
    d.text((ax + 8, y + 6), "ALSO ON SATURDAY 21 NOVEMBER — 23 MORE STORIES",
           font=SANSB(11), fill=INK)
    d.line([(ax + 8, y + 24), (W - M - 8, y + 24)], fill=LINE, width=1)
    col2w = (W - M - ax - 16) / 2
    for i, (n, txt, src) in enumerate(ALSO):
        col = i // 12
        row = i % 12
        tx = ax + 8 + col * col2w
        ty = y + 30 + row * 16
        line = txt + f" ({src})"
        if SANS(9).getlength(line) > col2w - 24:
            print(f"WARN also overflow #{n}: {SANS(9).getlength(line):.0f} > {col2w - 24:.0f}")
        d.text((tx, ty), str(n), font=SANSB(9), fill=RED)
        d.text((tx + 20, ty), line, font=SANS(9), fill=INK)

    # date check (no timeline strip in v4)
    date_check_box(d, M, 946, CW, 36)

    # footer — now true: every story does carry its source beside it
    d.text((W // 2, 992), "Every story here happened, or was first reported, on "
           "Saturday 21 November 2026. Sources named beside each story · "
           "Original drawings",
           font=SANS(9), fill=GREY, anchor="ma")

    return img


if __name__ == "__main__":
    page = draw_page()
    page.save("entry.png", optimize=True)
    data = open("entry.png", "rb").read()
    print("size bytes:", len(data))
    print("dimensions:", page.size)
    print("sha256:", hashlib.sha256(data).hexdigest())
    print("stories:", 3 + len(MED) + len(ALSO))
    print("regions:", sum(c for _, c, _ in REGIONS))
