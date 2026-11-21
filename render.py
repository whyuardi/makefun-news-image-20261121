#!/usr/bin/env python3
"""Render the 21 November 2026 world-news front page, drawn entirely in code.

One 1024x1024 PNG: a newspaper front page. Masthead names the day
(SATURDAY 21 NOVEMBER 2026). Lead: Russian missiles land in Poland and
NATO's response (jets scrambled, Rutte due in Warsaw). Also: Gen Z
protests across 25 European countries, the magnitude 6.8 Peru quake,
COP31 talks stalling, Denmark expelling a Russian diplomat, and Trump
pressing Nvidia over Jensen Huang — plus a ticker (Nepal PM to Delhi,
KL Rahul's SENA set, Rikers to close by 2032, Houthi missiles downed).

Every fact is as reported on 21 Nov 2026 (AP / BBC / The Times /
Al Jazeera / The Daily Short):
- Kh-101 cruise missile crashed at Nowy Lipowiec, SE Poland (~50 km
  from the Ukraine border); a 2nd suspected missile near Rudnik nad
  Sanem; a jet-powered drone near Molodycz. No casualties, no damage.
  PM Donald Tusk: "an intentional / deliberate provocation", "not a
  coincidence" it fell near the Coalition of the Willing exercise
  (Koalicja 2026, 11 nations, Nowa Deba). NATO Sec-Gen Mark Rutte:
  "grave violation" of Polish airspace; NATO jets scrambled; Rutte due
  in Warsaw on Saturday 21 Nov.
- Gen Z protests: thousands rallied across 25 European countries on
  21 Nov over living costs, military spending and climate.
- Peru: magnitude 6.8 quake struck the Junin region; tremors felt in
  Lima, ~320 km away (Peru Geophysical Institute).
- COP31: climate deal stalls as nations struggle to agree a plan; EU
  warns against a "fossil-fuel summit".
- Denmark expels a Russian diplomat over an alleged plot to assassinate
  a US-Ukrainian rapper; Russia denies it.
- Trump calls for Nvidia to reinstate "brilliant" ex-CEO Jensen Huang
  ("a second chance", "a big apology") and threatens a tax on US firms
  building AI data centres overseas; tech shares sell off.
- Nepal PM Balendra Shah heads to Delhi for his first foreign visit.
- KL Rahul: first Indian opener with Test centuries in all four SENA
  countries (100 in Wellington).
- NYC Mayor Mamdani sets 2032 as the new date to close Rikers Island.
- Saudi-led coalition downs Houthi missiles; Houthis hit a Riyadh tower,
  no injuries.

NOT in this image on purpose: the ICJ Myanmar/Rohingya genocide ruling
was handed down on Thu 19 Nov 2026, so it is not 21 Nov news.

Drawn with PIL + DejaVu only; no external images, no network.
Output: entry.png (PNG, 1024x1024, well under 1 MiB).
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

PAPER = (247, 242, 233)
INK = (16, 24, 34)
NAVY = (13, 33, 55)
GOLD = (212, 175, 55)
RED = (178, 34, 34)
TEAL = (36, 122, 140)
BROWN = (122, 72, 32)
WHITE = (255, 255, 255)
GREY = (90, 96, 104)
SKIN = (232, 190, 150)
SKY = (168, 200, 228)


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, path, max_w, start, floor=12):
    size = start
    while size > floor:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, floor)


def wrap(draw, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def panel(draw, x, y, w, h, accent):
    draw.rectangle([x, y, x + w, y + h], fill=WHITE, outline=(60, 60, 60), width=2)
    draw.rectangle([x, y, x + w, y + 7], fill=accent)


def headline(draw, text, x, y, w, size=30, color=INK):
    f = fit(draw, text, BOLD, w, size)
    lines = wrap(draw, text, f, w)
    for i, line in enumerate(lines):
        draw.text((x, y + i * int(size * 1.12)), line, font=f, fill=color)
    return y + len(lines) * int(size * 1.12)


def subline(draw, text, x, y, w, size=19):
    f = font(REG, size)
    lines = wrap(draw, text, f, w)
    for i, line in enumerate(lines):
        draw.text((x, y + i * int(size * 1.35)), line, font=f, fill=(40, 40, 40))
    return y + len(lines) * int(size * 1.35)


def draw_jet(draw, x, y, s, color=NAVY):
    """Small jet silhouette, nose to the right."""
    draw.polygon([(x, y + s * 0.5), (x + s, y + s * 0.5),
                  (x + s * 0.72, y + s * 0.28), (x + s * 0.55, y + s * 0.5),
                  (x + s * 0.72, y + s * 0.72)],
                 fill=color)
    draw.polygon([(x + s * 0.42, y + s * 0.5), (x + s * 0.52, y + s * 0.08),
                  (x + s * 0.62, y + s * 0.5)], fill=color)
    draw.polygon([(x + s * 0.42, y + s * 0.5), (x + s * 0.52, y + s * 0.92),
                  (x + s * 0.62, y + s * 0.5)], fill=color)


def draw_burst(draw, cx, cy, r, color=RED):
    """Explosion starburst."""
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=color)
    draw.ellipse([cx - r * 0.32, cy - r * 0.32, cx + r * 0.32, cy + r * 0.32],
                 fill=(250, 200, 60))


def draw_poland_map(draw, x, y, w, h):
    """Stylised Poland: pale land, Baltic top, Ukraine right, missile
    arc from the east, three impact bursts in the south-east, NATO jets."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    # Baltic Sea label.
    f_lab = font(BOLD, 15)
    draw.text((x + 14, y + 8), "BALTIC SEA", font=f_lab, fill=(40, 90, 140))
    # Land mass (simplified Poland outline).
    land = [
        (x + 70, y + 42), (x + 150, y + 26), (x + 280, y + 30),
        (x + 420, y + 22), (x + 520, y + 46), (x + 540, y + 92),
        (x + 486, y + 138), (x + 380, y + 158), (x + 250, y + 150),
        (x + 140, y + 164), (x + 72, y + 118), (x + 52, y + 78),
    ]
    draw.polygon(land, fill=(226, 214, 178), outline=INK, width=2)
    # Ukraine label, east of the border.
    draw.text((x + w - 108, y + h - 30), "UKRAINE", font=f_lab, fill=(90, 90, 90))
    # Warsaw star.
    wx, wy = x + 330, y + 84
    draw_burst(draw, wx, wy, 10, color=NAVY)
    draw.text((wx + 14, wy - 8), "WARSAW", font=font(BOLD, 14), fill=INK)
    # Missile arc from the east, dashed.
    px, py = x + w - 6, y + 52
    tx, ty = x + 468, y + 108
    for t_i in range(21):
        t = t_i / 20
        bx = (1 - t) ** 2 * px + 2 * (1 - t) * t * (x + 520) + t * t * tx
        by = (1 - t) ** 2 * py + 2 * (1 - t) * t * (y + 30) + t * t * ty
        if t_i % 2 == 0:
            draw.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=RED)
    # Missile body near the arc end.
    draw.polygon([(tx + 26, ty - 6), (tx + 44, ty), (tx + 26, ty + 6),
                  (tx + 14, ty + 3), (tx + 14, ty - 3)], fill=(60, 60, 60))
    # Three impact bursts in the south-east.
    for ix, iy, r in ((468, 108, 13), (428, 96, 10), (398, 130, 10)):
        draw_burst(draw, x + ix, y + iy, r)
    # NATO jets top-left.
    draw_jet(draw, x + 16, y + 96, 34)
    draw_jet(draw, x + 58, y + 118, 26)
    f_tag = font(BOLD, 13)
    draw.text((x + 16, y + 148), "NATO JETS", font=f_tag, fill=NAVY)
    # Country label.
    draw.text((x + 150, y + 78), "POLAND", font=font(BOLD, 22), fill=(90, 80, 60))


def draw_crowd(draw, x, y, w, h):
    """Protest crowd, wide band: placard left, two rows of heads."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 222, 190))
    draw.rectangle([x, y, x + w, y + 26], fill=(250, 214, 120))
    # Placard, top-left.
    px, pw = x + 10, 96
    draw.rectangle([px, y + 4, px + pw, y + 26], fill=WHITE,
                   outline=INK, width=2)
    f_p = fit(draw, "FAIR PAY", BOLD, pw - 8, 15)
    draw.text((px + (pw - draw.textlength("FAIR PAY", font=f_p)) / 2, y + 8),
              "FAIR PAY", font=f_p, fill=RED)
    draw.line([px + pw // 2, y + 26, px + pw // 2, y + 38], fill=INK, width=3)
    # Heads + shoulders, two rows across the band.
    import random as _r
    rng = _r.Random(21112026)
    skins = [(232, 190, 150), (200, 150, 110), (240, 205, 170), (180, 130, 95)]
    shirts = [NAVY, RED, TEAL, (90, 90, 90), (30, 120, 70)]
    for row, cy in enumerate((y + 44, y + 66)):
        n = 11 if row == 0 else 12
        for i in range(n):
            cx = x + 16 + i * ((w - 32) / max(n - 1, 1)) + rng.randint(-3, 3)
            draw.polygon([(cx - 13, cy + 16), (cx + 13, cy + 16),
                          (cx + 10, cy + 5), (cx - 10, cy + 5)],
                         fill=rng.choice(shirts))
            draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9],
                         fill=rng.choice(skins))
            draw.pieslice([cx - 9, cy - 9, cx + 9, cy + 1], 180, 360,
                          fill=(40, 40, 40))


def draw_quake(draw, x, y, w, h):
    """Tilted buildings across a wide band, cracked ground, 6.8 badge."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 200, 170))
    # Buildings, leaning, spread across the band.
    gy = y + h - 16
    specs = [(x + 14, 58, 46, -6, (150, 110, 70)),
             (x + 88, 66, 58, 5, (120, 90, 60)),
             (x + 170, 56, 40, -4, (170, 130, 85)),
             (x + 242, 62, 52, 6, (140, 105, 65))]
    for bx, bw, bh, tilt, col in specs:
        top = gy - bh
        draw.polygon([(bx, top + tilt), (bx + bw, top - tilt),
                      (bx + bw, gy), (bx, gy)], fill=col, outline=INK)
        for wy2 in range(2):
            wyy = top + 10 + wy2 * 20
            draw.rectangle([bx + 8, wyy, bx + 16, wyy + 9], fill=(250, 230, 120))
            draw.rectangle([bx + bw - 16, wyy, bx + bw - 8, wyy + 9],
                           fill=(250, 230, 120))
    # Ground + jagged crack.
    draw.rectangle([x, gy, x + w, y + h], fill=(96, 72, 44))
    crack = [(x + 8, gy), (x + 60, gy + 8), (x + 120, gy + 3),
             (x + 180, gy + 10), (x + 240, gy + 4), (x + 300, gy + 11),
             (x + w - 8, gy + 6)]
    draw.line(crack, fill=(30, 20, 10), width=3)
    # Magnitude badge, bottom-right over the ground.
    draw.ellipse([x + w - 56, y + h - 52, x + w - 4, y + h], fill=RED,
                 outline=WHITE, width=2)
    f_m = font(BOLD, 20)
    draw.text((x + w - 50, y + h - 38), "6.8", font=f_m, fill=WHITE)


def draw_globe(draw, x, y, s):
    """Globe with continents + leaf."""
    draw.ellipse([x, y, x + s, y + s], fill=(70, 130, 200), outline=INK, width=3)
    for px, py, r in ((0.32, 0.30, 12), (0.62, 0.28, 10), (0.42, 0.58, 13),
                      (0.68, 0.62, 9), (0.28, 0.62, 7)):
        draw.ellipse([x + s * px - r, y + s * py - r, x + s * px + r, y + s * py + r],
                     fill=(70, 170, 90))
    draw.pieslice([x + s * 0.62, y - 6, x + s * 0.98, y + s * 0.30], 270, 90,
                  fill=(50, 150, 70))
    draw.line([x + s * 0.66, y + s * 0.22, x + s * 0.94, y - 2],
              fill=(30, 110, 50), width=3)


def draw_denmark(draw, x, y, w, h):
    """Danish flag + EXPELLED stamp."""
    # Flag: red field, white cross.
    draw.rectangle([x, y, x + w, y + h], fill=(200, 16, 46))
    draw.rectangle([x + w * 0.30, y, x + w * 0.42, y + h], fill=WHITE)
    draw.rectangle([x, y + h * 0.42, x + w, y + h * 0.58], fill=WHITE)
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    # Stamp: white-filled box so the red text reads.
    sx, sy, sw, sh = x + w - 118, y + h - 44, 112, 34
    draw.rectangle([sx, sy, sx + sw, sy + sh], fill=WHITE, outline=RED, width=3)
    f_s = fit(draw, "EXPELLED", BOLD, sw - 10, 19)
    draw.text((sx + (sw - draw.textlength("EXPELLED", font=f_s)) / 2, sy + 6),
              "EXPELLED", font=f_s, fill=RED)


def draw_chip(draw, x, y, s):
    """AI chip: square body, pins, 'AI' core."""
    draw.rectangle([x, y, x + s, y + s], fill=NAVY, outline=GOLD, width=3)
    for i in range(4):
        px = x + 10 + i * (s - 20) // 3
        draw.rectangle([px - 2, y - 10, px + 2, y], fill=GOLD)
        draw.rectangle([px - 2, y + s, px + 2, y + s + 10], fill=GOLD)
        py = y + 10 + i * (s - 20) // 3
        draw.rectangle([x - 10, py - 2, x, py + 2], fill=GOLD)
        draw.rectangle([x + s, py - 2, x + s + 10, py + 2], fill=GOLD)
    f = font(BOLD, int(s * 0.38))
    t = "AI"
    draw.text((x + (s - draw.textlength(t, font=f)) / 2, y + s * 0.24),
              t, font=f, fill=GOLD)


def main():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 118], fill=NAVY)
    f_title = fit(d, "THE WORLD IN ONE DAY", BOLD, W - 40, 46)
    d.text(((W - d.textlength("THE WORLD IN ONE DAY", font=f_title)) / 2, 12),
           "THE WORLD IN ONE DAY", font=f_title, fill=WHITE)
    f_date = fit(d, "SATURDAY  \u00b7  21 NOVEMBER 2026", BOLD, W - 40, 30)
    d.text(((W - d.textlength("SATURDAY  \u00b7  21 NOVEMBER 2026", font=f_date)) / 2, 66),
           "SATURDAY  \u00b7  21 NOVEMBER 2026", font=f_date, fill=GOLD)

    # ---- Lead: Russian missiles in Poland ----
    lx, ly, lw, lh = 12, 130, 600, 430
    panel(d, lx, ly, lw, lh, RED)
    draw_poland_map(d, lx + 10, ly + 12, lw - 20, 196)
    hy = headline(d, "RUSSIAN MISSILES LAND IN POLAND", lx + 16, ly + 224, lw - 32, 34)
    hy = subline(d, "Tusk: a deliberate provocation. NATO jets scrambled; "
                    "alliance chief Rutte due in Warsaw today.",
                 lx + 16, hy + 6, lw - 32, 20)
    subline(d, "Kh-101 missile down in the south-east as allies drilled "
               "nearby; no casualties, no damage.",
            lx + 16, hy + 4, lw - 32, 20)

    # ---- Right top: Gen Z protests ----
    rx, ry, rw, rh = 624, 130, 388, 212
    panel(d, rx, ry, rw, rh, NAVY)
    draw_crowd(d, rx + 10, ry + 10, rw - 20, 78)
    hy = headline(d, "GEN Z TAKES TO EUROPE'S STREETS", rx + 14, ry + 96, rw - 28, 24)
    subline(d, "Thousands rally in 25 countries over living costs, "
               "military spending and climate.",
            rx + 14, hy + 4, rw - 28, 16)

    # ---- Right bottom: Peru quake ----
    qx, qy, qw, qh = 624, 354, 388, 206
    panel(d, qx, qy, qw, qh, BROWN)
    draw_quake(d, qx + 10, qy + 10, qw - 20, 78)
    hy = headline(d, "PERU SHAKEN BY 6.8 QUAKE", qx + 14, qy + 96, qw - 28, 24)
    subline(d, "Junin region hit; tremors felt 320 km away in Lima. "
               "The day's biggest natural disaster.",
            qx + 14, hy + 4, qw - 28, 16)

    # ---- Bottom row: three stories ----
    by, bh = 572, 316
    bx0 = [12, 350, 688]
    bw = 326
    # COP31.
    panel(d, bx0[0], by, bw, bh, TEAL)
    draw_globe(d, bx0[0] + bw // 2 - 40, by + 28, 80)
    hy = headline(d, "COP31 DEAL STALLS", bx0[0] + 12, by + 138, bw - 24, 24)
    subline(d, "Climate talks stall as nations fail to agree a plan; "
               "EU warns against a 'fossil-fuel summit'.",
            bx0[0] + 12, hy + 4, bw - 24, 16)
    d.text((bx0[0] + 12, by + bh - 28), "CLIMATE", font=font(BOLD, 14), fill=GREY)
    # Denmark.
    panel(d, bx0[1], by, bw, bh, RED)
    draw_denmark(d, bx0[1] + 12, by + 22, bw - 24, 104)
    hy = headline(d, "DENMARK EXPELS RUSSIAN DIPLOMAT", bx0[1] + 12, by + 138, bw - 24, 24)
    subline(d, "Copenhagen acts over an alleged plot to kill a "
               "US-Ukrainian rapper. Moscow denies it.",
            bx0[1] + 12, hy + 4, bw - 24, 16)
    d.text((bx0[1] + 12, by + bh - 28), "COPENHAGEN", font=font(BOLD, 14), fill=GREY)
    # Trump-Nvidia.
    panel(d, bx0[2], by, bw, bh, NAVY)
    draw_chip(d, bx0[2] + bw // 2 - 34, by + 30, 68)
    hy = headline(d, "TRUMP TO NVIDIA: BRING HUANG BACK", bx0[2] + 12, by + 138, bw - 24, 24)
    subline(d, "President urges the chip giant to reinstate its ex-CEO "
               "and threatens a tax on AI data centres built abroad.",
            bx0[2] + 12, hy + 4, bw - 24, 16)
    d.text((bx0[2] + 12, by + bh - 28), "TECH \u00b7 USA", font=font(BOLD, 14), fill=GREY)

    # ---- Ticker ----
    d.rectangle([12, 900, 1012, 952], fill=(30, 30, 30))
    tick = ("ALSO: Nepal PM to Delhi  \u00b7  KL Rahul's SENA set  \u00b7  "
            "Rikers to close by 2032  \u00b7  Houthi missiles downed")
    f_tick = fit(d, tick, BOLD, 980, 20)
    d.text((22, 918), tick, font=f_tick, fill=WHITE)

    # ---- Footer ----
    d.rectangle([0, 964, W, H], fill=NAVY)
    f_foot = fit(d, "ALL STORIES REPORTED ON 21 NOVEMBER 2026", BOLD, W - 40, 24)
    d.text(((W - d.textlength("ALL STORIES REPORTED ON 21 NOVEMBER 2026", font=f_foot)) / 2, 982),
           "ALL STORIES REPORTED ON 21 NOVEMBER 2026", font=f_foot, fill=GOLD)

    im.save(OUT, "PNG")
    print(f"{OUT}: {im.size[0]}x{im.size[1]}")


if __name__ == "__main__":
    main()
