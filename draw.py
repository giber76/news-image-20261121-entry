#!/usr/bin/env python3
"""Draw the Saturday 21 November 2026 world-news front page (1024x1024).

Every story was verified against live reporting on 21 Nov 2026 before it
was drawn: COP31 overtime (AP), three Houthi missiles over Riyadh
(Reuters), the Junin 6.7 quake (USGS/IGP), the Kryvyi Rih double strike
(Kyiv Independent), the Hormuz MQ-9 claim (IRIB), Iran's uranium line
(Araghchi), Trump's data-centre tax (Reuters), China-Japan (Guo Jiakun),
the Davao emergency landing (CAAP/AP), the Australia-China AI dialogue
(AAP), Bitcoin's slide (CoinGecko), Las Vegas qualifying (Reuters),
Rahul's 136 (Reuters/ESPNcricinfo) and the rest.

v2 (same 35 stories, execution only): COP31, uranium, AI-talks and
China-Japan illustrations redrawn as literal scenes; a HOW SURE legend
marks each card CONFIRMED / CLAIM / FORECAST (dots in the kicker rows
and ALSO lines); each card names its source in the kicker bar; the
DATE CHECK now lists what is not yet as well as what was left out;
the footer names the agencies. Winner study: the 19 Nov top 3 all
share a UTC timeline strip (v1 already has one), a DATE CHECK box,
per-story status+source tags, a sources line and literal scenes.
"""
import hashlib
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
CREAM = (246, 241, 227)
PAPER = (250, 246, 235)
INK = (26, 26, 26)
RED = (185, 28, 28)
DARKRED = (140, 20, 20)
NAVY = (30, 58, 95)
TEAL = (15, 118, 110)
GOLD = (180, 83, 9)
PURPLE = (107, 33, 168)
GREEN = (21, 128, 61)
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


SERIF = lambda s: F("DejaVuSerif.ttf", s)
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
LEADS = [
    dict(n=1, kicker="COP31: OVERTIME", loc="ANTALYA, TÜRKIYE · CLIMATE",
         head="Climate summit runs into Saturday with no deal",
         deck="COP31 missed its Friday close; a draft with no fossil fuels splits nearly 200 countries. A third text is promised.",
         ill="cop31"),
    dict(n=2, kicker="SAUDI: MISSILES", loc="RIYADH · WAR",
         head="Three Houthi missiles shot down over Riyadh",
         deck="The coalition destroyed three ballistic missiles fired at the capital before dawn, the third night of alerts. No damage.",
         ill="riyadh"),
    dict(n=3, kicker="PERU: QUAKE 6.7", loc="JUNÍN, PERU · EARTHQUAKE",
         head="Magnitude 6.7 earthquake shakes central Peru",
         deck="The deep quake near Carhuamayo was felt in Lima and along the coast. No deaths, damage or tsunami risk reported.",
         ill="peru"),
]

MED = [
    dict(n=4, kicker="KRYVYI RIH: STRIKE", loc="UKRAINE · WAR",
         head="Russian double strike hits Kryvyi Rih",
         deck="A boy of 7 and a paramedic, 20, killed; 42 hurt as drones hit rescuers.",
         ill="kryvyi"),
    dict(n=5, kicker="HORMUZ: DRONE", loc="STRAIT OF HORMUZ · WAR",
         head="Iran says it shot down a US drone",
         deck="The IRGC claims its 58th MQ-9 Reaper. No confirmation from Washington.",
         ill="hormuz"),
    dict(n=6, kicker="IRAN: URANIUM", loc="TEHRAN · DIPLOMACY",
         head="Iran: uranium stock stays in the country",
         deck="Minister seeks a “fair solution”; Tehran rules out sending 60% uranium abroad.",
         ill="uranium"),
    dict(n=7, kicker="TRUMP: AI TAX", loc="WASHINGTON · TECHNOLOGY",
         head="Trump vows tax on data centres abroad",
         deck="“Tremendous” penalty promised; no details yet.",
         ill="datacentre"),
    dict(n=8, kicker="CHINA–JAPAN", loc="BEIJING · DIPLOMACY",
         head="China tells Japan: “correct” Taiwan words",
         deck="Tokyo says its stance is unchanged.",
         ill="flags"),
    dict(n=9, kicker="DAVAO: 146 SAFE", loc="PHILIPPINES · AVIATION",
         head="Jet lands safely after engine fire alert",
         deck="Air Niugini 767 diverts after midnight; all 146 safe.",
         ill="plane"),
    dict(n=10, kicker="CANBERRA: AI", loc="AUSTRALIA · DIPLOMACY",
         head="Australia and China agree to AI talks",
         deck="Albanese ends an 11-day trip.",
         ill="aitalks"),
    dict(n=11, kicker="BITCOIN: $58,983", loc="WORLD · MARKETS",
         head="Bitcoin trades below $59,000 on Saturday",
         deck="Down 3.9% in 24 hours; ether $1,625.",
         ill="bitcoin"),
    dict(n=12, kicker="LAS VEGAS: POLE", loc="FORMULA ONE · SPORT",
         head="Verstappen on pole in Las Vegas",
         deck="Antonelli fastest but a penalty hands him pole; Russell on the front row.",
         ill="f1"),
    dict(n=13, kicker="RAHUL: 136", loc="WELLINGTON · CRICKET",
         head="Rahul hits 136 as India take charge",
         deck="First Indian opener with Test hundreds in all SENA countries; India 486/4, lead 118.",
         ill="cricket"),
]

ALSO = [
    (14, "Kyiv: Zelensky warns of double-tap strikes"),
    (15, "Copenhagen: Russian attaché expelled over plot"),
    (16, "Antalya: EU warns COP31 risks a “fossil summit”"),
    (17, "Antalya: Panama threatens to block climate deal"),
    (18, "Antalya: Indonesia's PLN signs clean-power deals"),
    (19, "Yemen: Houthis threaten Jeddah and Red Sea ports"),
    (20, "Washington: Vance — Iran strikes were Trump's call"),
    (21, "Washington: Lawmaker threatens SpaceX funding"),
    (22, "Texas: Execution of a man of 70 takes 63 minutes"),
    (23, "Los Angeles: Jury convicts Palisades fire starter"),
    (24, "Turin: Medvedev meets Zverev in tonight's semi"),
    (25, "Vancouver: Canada rests defence in climate trial"),
    (26, "Pyongyang: Kim tours factories after no Trump talks"),
    (27, "Sejong: Freight train derails; no one hurt"),
    (28, "Taipei: Budget and a cash payout are passed"),
    (29, "Bangkok: Six-point plan on arsenic in two rivers"),
    (30, "New Delhi: Pakistani minister joins SCO forum"),
    (31, "Eastern India: Rain alerts as Akvan moves inland"),
    (32, "Myanmar: Rights groups urge sanctions after ruling"),
    (33, "Port Louis: African rating agency talks to 15 states"),
    (34, "Melbourne: Cummins keeps the Australian captaincy"),
    (35, "Warsaw: Rutte flies in for NATO talks"),
]

STATS = [
    ("13", "DAY OF COP31 — IT WAS MEANT TO CLOSE ON DAY 12"),
    ("3", "MISSILES SHOT DOWN OVER RIYADH"),
    ("6.7", "MAGNITUDE OF THE QUAKE IN JUNÍN, PERU"),
    ("146", "PEOPLE SAFE AFTER THE DAVAO EMERGENCY LANDING"),
    ("$58,983", "BITCOIN EARLY SATURDAY, DOWN 3.9% IN A DAY"),
    ("136", "K L RAHUL'S SCORE AT WELLINGTON"),
]

REGIONS = [
    ("EUROPE", 6, (30, 58, 95)),
    ("ASIA", 10, (185, 28, 28)),
    ("MIDDLE EAST", 4, (180, 83, 9)),
    ("AFRICA", 1, (21, 128, 61)),
    ("AMERICAS", 9, (107, 33, 168)),
    ("OCEANIA", 3, (15, 118, 110)),
    ("GLOBAL", 2, (90, 90, 90)),
]

FIELDS = [
    ("WAR", 7, (185, 28, 28)),
    ("DIPLOMACY", 5, (30, 58, 95)),
    ("CLIMATE", 4, (21, 128, 61)),
    ("POLITICS", 4, (107, 33, 168)),
    ("SPORT", 4, (15, 118, 110)),
    ("COURTS", 2, (120, 90, 40)),
    ("OTHER", 9, (110, 110, 100)),
]

TIMELINE = [
    ("00:09 UTC", "6.7 quake hits Junín, Peru"),
    ("00:43 UTC", "Bitcoin below $59,000"),
    ("03:03 UTC", "Iran claims a US drone downed"),
    ("06:06 UTC", "Bitcoin $55,684 — lowest since Sep 2024"),
    ("18:24 UTC", "BepiColombo fires thrusters for Mercury orbit"),
]

# lat/lon of the 13 pictured stories (11 = worldwide, placed mid-Atlantic)
PINS = {
    1: (36.9, 30.7), 2: (24.7, 46.7), 3: (-11.2, -76.0), 4: (47.9, 33.4),
    5: (26.5, 56.3), 6: (35.7, 51.4), 7: (38.9, -77.0), 8: (39.9, 116.4),
    9: (7.1, 125.6), 10: (-35.3, 149.1), 11: (20.0, -30.0),
    12: (36.2, -115.1), 13: (-41.3, 174.8),
}
# display nudges (lat, lon) so the crowded Middle East cluster stays readable
PIN_NUDGE = {
    1: (2, -4), 2: (-4, 0), 4: (4, -3), 5: (-2, 5), 6: (3, 4),
    10: (0, -4), 13: (2, -10),
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
    # v2: a literal negotiation hall — delegates at a long table under a
    # wall clock near midnight (the summit in overtime), not icons.
    d.rectangle([x, y, x + w, y + h], fill=(213, 232, 212))
    # wall clock (overtime: hands near midnight)
    kx, ky, kr = x + w * 0.88, y + h * 0.24, h * 0.20
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=(255, 255, 255), outline=INK, width=2)
    d.line([kx, ky, kx - kr * 0.45, ky - kr * 0.55], fill=INK, width=2)
    d.line([kx, ky, kx + kr * 0.10, ky - kr * 0.75], fill=INK, width=2)
    # four delegates behind the table
    suits = [(30, 58, 95), (90, 90, 90), (15, 118, 110), (140, 20, 20)]
    for i, col in enumerate(suits):
        cx = x + w * (0.12 + i * 0.20)
        d.ellipse([cx - 8, y + h * 0.28, cx + 8, y + h * 0.46], fill=(235, 200, 170), outline=INK, width=1)
        d.rounded_rectangle([cx - 13, y + h * 0.46, cx + 13, y + h * 0.62], radius=5, fill=col)
    # long negotiation table (covers the delegates' lower bodies)
    d.rectangle([x + 8, y + h * 0.58, x + w - 8, y + h * 0.92], fill=(120, 80, 50))
    d.rectangle([x + 8, y + h * 0.58, x + w - 8, y + h * 0.64], fill=(150, 105, 65))
    # draft papers on the table
    for i in range(3):
        px = x + w * (0.14 + i * 0.28)
        d.rectangle([px, y + h * 0.68, px + 26, y + h * 0.86], fill=(255, 255, 255), outline=INK, width=1)


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
    import math
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


def ill_kryvyi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 38, 66))
    _skyline(d, x, y, w, h, y + h, (40, 48, 80))
    for bx, by, s in [(0.30, 0.45, 14), (0.62, 0.38, 18), (0.85, 0.55, 11)]:
        cx, cy = x + w * bx, y + h * by
        for k in range(8):
            import math
            a = k * math.pi / 4
            d.line([cx, cy, cx + s * math.cos(a), cy + s * math.sin(a)],
                   fill=(255, 150, 40), width=3)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 220, 90))


def ill_hormuz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(140, 190, 220))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(30, 90, 150))
    for i in range(4):
        wx = x + w * (0.12 + i * 0.25)
        d.arc([wx, y + h * 0.58, wx + 26, y + h * 0.72], 200, 340, fill=(255, 255, 255), width=2)
    # ship
    sx, sy = x + w * 0.30, y + h * 0.52
    d.polygon([(sx, sy), (sx + w * 0.42, sy), (sx + w * 0.36, sy + h * 0.16),
               (sx + w * 0.06, sy + h * 0.16)], fill=(60, 60, 60))
    d.rectangle([sx + w * 0.12, sy - h * 0.14, sx + w * 0.22, sy], fill=(200, 200, 200))
    # drone + crosshair
    dx, dy = x + w * 0.78, y + h * 0.28
    d.ellipse([dx - 12, dy - 12, dx + 12, dy + 12], outline=RED, width=2)
    d.line([dx - 18, dy, dx + 18, dy], fill=RED, width=2)
    d.line([dx, dy - 18, dx, dy + 18], fill=RED, width=2)
    d.ellipse([dx - 4, dy - 3, dx + 4, dy + 3], fill=(40, 40, 40))


def ill_uranium(d, x, y, w, h):
    # v2: a literal centrifuge hall — rows of enrichment centrifuges
    # with a connecting pipe, not a generic atom symbol.
    d.rectangle([x, y, x + w, y + h], fill=(38, 38, 52))
    d.text((x + 6, y + 4), "60%", font=SANSB(13), fill=(255, 255, 255))
    # connecting pipe along the top
    d.line([x + w * 0.10, y + h * 0.34, x + w * 0.90, y + h * 0.34], fill=(150, 150, 170), width=2)
    # floor line
    d.line([x + 4, y + h * 0.86, x + w - 4, y + h * 0.86], fill=(120, 120, 140), width=1)
    # five centrifuge cylinders
    for i in range(5):
        cx = x + w * (0.14 + i * 0.18)
        d.rounded_rectangle([cx - 9, y + h * 0.34, cx + 9, y + h * 0.86], radius=4,
                            fill=(180, 180, 190), outline=(100, 100, 110), width=1)
        d.rectangle([cx - 9, y + h * 0.50, cx + 9, y + h * 0.58], fill=(255, 200, 60))


def ill_datacentre(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 58, 95))
    for i in range(3):
        rx = x + w * (0.10 + i * 0.30)
        d.rectangle([rx, y + h * 0.18, rx + w * 0.22, y + h * 0.86],
                    fill=(20, 40, 70), outline=(120, 160, 200), width=2)
        for r in range(5):
            ry = y + h * (0.26 + r * 0.12)
            d.ellipse([rx + 5, ry, rx + 10, ry + 5], fill=(80, 220, 120))
            d.rectangle([rx + 16, ry, rx + w * 0.22 - 6, ry + 5], fill=(120, 160, 200))


def ill_flags(d, x, y, w, h):
    # v2: a literal press-conference scene — the two flags on poles
    # flanking a podium with microphones, not two flat flags.
    d.rectangle([x, y, x + w, y + h], fill=(232, 228, 215))
    # China flag on a pole (left)
    fx, fy, fw, fh = x + w * 0.06, y + h * 0.14, w * 0.30, h * 0.34
    d.line([fx + fw / 2, fy, fx + fw / 2, y + h * 0.62], fill=INK, width=2)
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 41, 16))
    d.text((fx + 4, fy + 2), "★", font=SANSB(13), fill=(255, 222, 0))
    # Japan flag on a pole (right)
    jx, jy = x + w * 0.64, y + h * 0.14
    d.line([jx + fw / 2, jy, jx + fw / 2, y + h * 0.62], fill=INK, width=2)
    d.rectangle([jx, jy, jx + fw, jy + fh], fill=(255, 255, 255), outline=INK, width=1)
    d.ellipse([jx + fw * 0.32, jy + fh * 0.22, jx + fw * 0.68, jy + fh * 0.78], fill=(188, 0, 45))
    # the rebuke, small, above the podium
    d.text((x + w * 0.50, y + h * 0.30), "“correct”", font=SANSB(10), fill=INK, anchor="mm")
    # podium with microphones
    px0 = x + w * 0.38
    d.polygon([(px0, y + h * 0.62), (px0 + w * 0.24, y + h * 0.62),
               (px0 + w * 0.20, y + h * 0.92), (px0 + w * 0.04, y + h * 0.92)],
              fill=(60, 60, 80))
    d.line([px0 + w * 0.08, y + h * 0.62, px0 + w * 0.08, y + h * 0.44], fill=INK, width=2)
    d.line([px0 + w * 0.16, y + h * 0.62, px0 + w * 0.16, y + h * 0.44], fill=INK, width=2)
    d.ellipse([px0 + w * 0.08 - 3, y + h * 0.44 - 3, px0 + w * 0.08 + 3, y + h * 0.44 + 3], fill=INK)
    d.ellipse([px0 + w * 0.16 - 3, y + h * 0.44 - 3, px0 + w * 0.16 + 3, y + h * 0.44 + 3], fill=INK)


def ill_plane(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 200, 235))
    for cx, cy, r in [(0.15, 0.25, 7), (0.85, 0.18, 9), (0.60, 0.12, 5)]:
        d.ellipse([x + w * cx - r, y + h * cy - r, x + w * cx + r, y + h * cy + r],
                  fill=(255, 255, 255))
    # plane silhouette
    px, py = x + w * 0.50, y + h * 0.52
    d.ellipse([px - w * 0.38, py - 7, px + w * 0.38, py + 7], fill=(255, 255, 255), outline=NAVY, width=1)
    d.polygon([(px + w * 0.18, py), (px + w * 0.34, py - h * 0.22), (px + w * 0.40, py - h * 0.20),
               (px + w * 0.30, py)], fill=(255, 255, 255), outline=NAVY)
    d.polygon([(px - w * 0.05, py), (px - w * 0.20, py + h * 0.20), (px - w * 0.12, py + h * 0.20),
               (px + w * 0.02, py)], fill=(255, 255, 255), outline=NAVY)
    d.rectangle([x, y + h * 0.82, x + w, y + h * 0.86], fill=(90, 90, 90))


def ill_aitalks(d, x, y, w, h):
    # v2: a literal bilateral meeting — two delegates at a table with
    # their flags and a laptop, not two flat flags and a badge.
    d.rectangle([x, y, x + w, y + h], fill=(220, 232, 220))
    # two delegates behind the table
    for cx, col in [(x + w * 0.20, (0, 47, 108)), (x + w * 0.80, (222, 41, 16))]:
        d.ellipse([cx - 7, y + h * 0.18, cx + 7, y + h * 0.42], fill=(235, 200, 170), outline=INK, width=1)
        d.rounded_rectangle([cx - 11, y + h * 0.42, cx + 11, y + h * 0.58], radius=4, fill=col)
    # meeting table
    d.rectangle([x + 6, y + h * 0.58, x + w - 6, y + h * 0.90], fill=(120, 80, 50))
    d.rectangle([x + 6, y + h * 0.58, x + w - 6, y + h * 0.64], fill=(150, 105, 65))
    # laptop in the centre, screen showing AI
    lx0, ly0 = x + w * 0.40, y + h * 0.30
    d.rectangle([lx0, ly0, lx0 + w * 0.20, ly0 + h * 0.28], fill=(30, 30, 40), outline=INK, width=1)
    d.text((lx0 + w * 0.10, ly0 + h * 0.14), "AI", font=SANSB(9), fill=(120, 220, 120), anchor="mm")
    d.rectangle([lx0 - 4, ly0 + h * 0.28, lx0 + w * 0.20 + 4, ly0 + h * 0.32], fill=(90, 90, 100))
    # small table flags flanking the laptop
    for fx, col in [(x + w * 0.28, (0, 47, 108)), (x + w * 0.68, (222, 41, 16))]:
        d.line([fx, y + h * 0.58, fx, y + h * 0.78], fill=INK, width=1)
        d.rectangle([fx, y + h * 0.58, fx + 12, y + h * 0.70], fill=col)


def ill_bitcoin(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 24, 34))
    d.rectangle([x + 6, y + 8, x + w - 6, y + h - 8], outline=(80, 80, 100), width=1)
    pts = [(x + 12 + (w - 24) * i / 10, y + h * (0.30 + 0.055 * i) + (6 if i % 3 == 0 else -4))
           for i in range(11)]
    d.line(pts, fill=(255, 80, 60), width=3)
    d.text((x + 8, y + 4), "BTC", font=SANSB(12), fill=(255, 200, 60))
    d.text((x + w - 52, y + 4), "-3.9%", font=SANSB(11), fill=(255, 80, 60))


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
    d.text((x + 6, y + 4), "136", font=SERIFB(16), fill=(255, 255, 255))


ILLS = {
    "cop31": ill_cop31, "riyadh": ill_riyadh, "peru": ill_peru,
    "kryvyi": ill_kryvyi, "hormuz": ill_hormuz, "uranium": ill_uranium,
    "datacentre": ill_datacentre, "flags": ill_flags, "plane": ill_plane,
    "aitalks": ill_aitalks, "bitcoin": ill_bitcoin, "f1": ill_f1,
    "cricket": ill_cricket,
}

# ---------------------------------------------------------------- how sure
# v2: every pictured card carries a status dot in its kicker row (right
# end) and every ALSO line carries one before its text, explained by the
# legend under the map. CONFIRMED = it happened / is on the record.
# CLAIM = attributed, not yet verified (#5 Hormuz: IRGC claims, US has
# not confirmed; #6 uranium: Araghchi's stated position; #14, #16, #17,
# #19, #20, #21, #32 are warnings, threats or assertions). FORECAST =
# scheduled / expected (#24 Medvedev semi tonight; #31 rain alerts).
HOW_SURE = {
    1: "CONFIRMED", 2: "CONFIRMED", 3: "CONFIRMED", 4: "CONFIRMED",
    5: "CLAIM", 6: "CLAIM", 7: "CONFIRMED", 8: "CONFIRMED",
    9: "CONFIRMED", 10: "CONFIRMED", 11: "CONFIRMED", 12: "CONFIRMED",
    13: "CONFIRMED", 14: "CLAIM", 15: "CONFIRMED", 16: "CLAIM",
    17: "CLAIM", 18: "CONFIRMED", 19: "CLAIM", 20: "CLAIM",
    21: "CLAIM", 22: "CONFIRMED", 23: "CONFIRMED", 24: "FORECAST",
    25: "CONFIRMED", 26: "CONFIRMED", 27: "CONFIRMED", 28: "CONFIRMED",
    29: "CONFIRMED", 30: "CONFIRMED", 31: "FORECAST", 32: "CLAIM",
    33: "CONFIRMED", 34: "CONFIRMED", 35: "CONFIRMED",
}
HOW_SURE_COL = {
    "CONFIRMED": (34, 139, 80),
    "CLAIM": (200, 130, 0),
    "FORECAST": (30, 80, 160),
}


# v2 (winner study): short source named in each card's kicker bar,
# beside the HOW SURE dot — the winning broadsheets tag every card
# with its status AND its source.
SRC = {
    1: "AP", 2: "Reuters", 3: "USGS", 4: "Kyiv Ind.", 5: "IRIB",
    6: "IRNA", 7: "Reuters", 8: "Reuters", 9: "CAAP", 10: "AAP",
    11: "CoinGecko", 12: "Reuters", 13: "Reuters",
}


def sure_dot(d, cx, cy, status, r=5, outline=(255, 255, 255)):
    """HOW SURE marker: coloured dot, centre (cx, cy)."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r],
              fill=HOW_SURE_COL[status], outline=outline, width=1)

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
    """Proportional segments with a minimum width, labels centred."""
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
        cx += wd


# ------------------------------------------------------------ page layout
M = 14
CW = W - 2 * M


def draw_page():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # top bar
    d.text((M, 6), "THE WORLD IN ONE DAY", font=SANSB(11), fill=RED)
    d.text((W - M, 6), "35 STORIES · 7 REGIONS · SATURDAY 21 NOVEMBER 2026",
           font=SANSB(10), fill=INK, anchor="ra")
    d.line([(M, 24), (W - M, 24)], fill=INK, width=2)

    # masthead
    d.text((W // 2, 30), "Saturday 21 November 2026", font=SERIFB(54),
           fill=INK, anchor="ma")
    d.text((W // 2, 88), "Climate summit runs past its deadline · Three missiles "
           "shot down over Riyadh · Strong quake shakes Peru",
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

    # region + field bars
    seg_bar(d, M, 160, CW, 18, REGIONS, SANSB(9))
    seg_bar(d, M, 180, CW, 16, FIELDS, SANSB(9))

    # leads
    lw, lgap = 324, 12
    for i, s in enumerate(LEADS):
        x = M + i * (lw + lgap)
        y = 198
        d.rectangle([x, y, x + lw, y + 200], fill=PAPER, outline=LINE, width=1)
        ILLS[s["ill"]](d, x + 1, y + 1, lw - 2, 92)
        d.rectangle([x, y + 93, x + lw, y + 111], fill=RED)
        d.text((x + 8, y + 96), s["kicker"], font=SANSB(11), fill=(255, 255, 255))
        d.text((x + lw - 24, y + 96), SRC[s["n"]], font=SANS(9), fill=(255, 255, 255), anchor="ra")
        sure_dot(d, x + lw - 12, y + 102, HOW_SURE[s["n"]], r=5)
        d.text((x + 8, y + 115), f"{s['n']}  {s['loc']}", font=SANSB(9), fill=RED)
        block(d, x + 8, y + 129, lw - 16, s["head"], SERIFB(19),
              leading=22, max_lines=2)
        block(d, x + 8, y + 175, lw - 16, s["deck"], SANS(10),
              leading=12, max_lines=2)

    # medium rows
    mw, mgap = 195, 5.25
    for row in range(2):
        for j in range(5):
            s = MED[row * 5 + j]
            x = M + j * (mw + mgap)
            y = 402 + row * 168
            d.rectangle([x, y, x + mw, y + 164], fill=PAPER, outline=LINE, width=1)
            ILLS[s["ill"]](d, x + 1, y + 1, mw - 2, 54)
            d.rectangle([x, y + 55, x + mw, y + 70], fill=NAVY)
            d.text((x + 6, y + 57), s["kicker"], font=SANSB(8), fill=(255, 255, 255))
            d.text((x + mw - 18, y + 57), SRC[s["n"]], font=SANS(7), fill=(255, 255, 255), anchor="ra")
            sure_dot(d, x + mw - 10, y + 62, HOW_SURE[s["n"]], r=4)
            d.text((x + 6, y + 73), f"{s['n']}  {s['loc']}", font=SANSB(8), fill=RED)
            block(d, x + 6, y + 85, mw - 12, s["head"], SERIFB(13),
                  leading=16, max_lines=2)
            block(d, x + 6, y + 119, mw - 12, s["deck"], SANS(9),
                  leading=12, max_lines=3)

    # bottom: map + also list
    y = 738
    d.rectangle([M, y, M + 330, y + 192], fill=PAPER, outline=LINE, width=1)
    d.text((M + 8, y + 6), "WHERE IT HAPPENED", font=SANSB(11), fill=INK)
    draw_map(d, M + 1, y + 24, 328, 128)
    block(d, M + 8, y + 156, 314,
          "Each number is the story with that number on this page.",
          SANS(9), fill=GREY, leading=11, max_lines=1)
    # HOW SURE legend (v2): two lines under the map caption; the dots
    # match the status dot in each lead/medium kicker row and ALSO line.
    ly = y + 170
    d.text((M + 8, ly), "HOW SURE", font=SANSB(9), fill=RED)
    hx = M + 8 + SANSB(9).getlength("HOW SURE ")
    d.ellipse([hx, ly + 1, hx + 8, ly + 9], fill=HOW_SURE_COL["CONFIRMED"],
              outline=INK, width=1)
    d.text((hx + 12, ly), "CONFIRMED — on the record", font=SANS(9), fill=INK)
    ly += 12
    hx = M + 8
    d.ellipse([hx, ly + 1, hx + 8, ly + 9], fill=HOW_SURE_COL["CLAIM"],
              outline=INK, width=1)
    d.text((hx + 12, ly), "CLAIM — attributed", font=SANS(9), fill=INK)
    hx += 12 + SANS(9).getlength("CLAIM — attributed ")
    d.ellipse([hx, ly + 1, hx + 8, ly + 9], fill=HOW_SURE_COL["FORECAST"],
              outline=INK, width=1)
    d.text((hx + 12, ly), "FORECAST — scheduled", font=SANS(9), fill=INK)

    ax = M + 340
    d.rectangle([ax, y, W - M, y + 192], fill=PAPER, outline=LINE, width=1)
    d.text((ax + 8, y + 6), "ALSO ON SATURDAY 21 NOVEMBER — 22 MORE STORIES",
           font=SANSB(11), fill=INK)
    d.line([(ax + 8, y + 24), (W - M - 8, y + 24)], fill=LINE, width=1)
    col2w = (W - M - ax - 16) / 2
    for i, (n, txt) in enumerate(ALSO):
        col = i // 11
        row = i % 11
        tx = ax + 8 + col * col2w
        ty = y + 30 + row * 15
        d.text((tx, ty), str(n), font=SANSB(10), fill=RED)
        sure_dot(d, tx + 17, ty + 5, HOW_SURE[n], r=3, outline=INK)
        d.text((tx + 26, ty), txt, font=SANS(10), fill=INK)

    # timeline (v1 already has it; v2 marks it as a distinct strip)
    y = 934
    d.line([(M, y - 2), (W - M, y - 2)], fill=LINE, width=1)
    d.text((M, y), "THE DAY IN UTC", font=SANSB(10), fill=RED)
    tw = (CW - 120) / 5
    for i, (t, label) in enumerate(TIMELINE):
        tx = M + 120 + i * tw
        d.text((tx, y), t, font=SANSB(9), fill=INK)
        block(d, tx, y + 11, tw - 8, label, SANS(8), fill=GREY,
              leading=9, max_lines=2)

    # date check (v2: winners list what was left out AND what is not yet)
    y = 966
    d.rectangle([M, y, W - M, y + 32], outline=RED, width=2)
    block(d, M + 8, y + 4, CW - 16,
          "DATE CHECK — Left out (20 Nov news): UK–EU deal, Wall Street "
          "correction, Akvan landfall, Kyiv bridges barrage; Voyager 1 "
          "(18 Nov). Not yet: the COP31 deal; Medvedev–Zverev semi tonight.",
          SANS(10), fill=INK, leading=13, max_lines=2)

    # footer (v2: winners name the agencies at the bottom)
    d.text((W // 2, 1000), "Every story here happened, or was first reported, on "
           "Saturday 21 November 2026.",
           font=SANS(9), fill=GREY, anchor="ma")
    d.text((W // 2, 1012), "Sources: AP · Reuters · USGS · IGP · Kyiv Independent · "
           "IRIB · IRNA · AAP · CAAP · CoinGecko · ESPNcricinfo · Original drawings",
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
    print("fields:", sum(c for _, c, _ in FIELDS))
