#!/usr/bin/env python3
"""Build-time renderer for the news-image-20261125 entry.

Draws a one-page newspaper front page summing up the world news of
Wednesday 25 November 2026, and writes it to entry.png (1024x1024).

The picture is rendered locally with Pillow at build time and committed
to the repository; main.py only copies the committed file to the output
directory, so the graded run needs no network and no Pillow.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

PAPER = (246, 241, 230)
INK = (20, 20, 24)
NAVY = (18, 34, 62)
NAVY2 = (28, 52, 92)
GOLD = (232, 182, 76)
RED = (178, 34, 34)
TEAL = (14, 94, 94)
SAND = (233, 220, 196)
SKY = (214, 228, 240)
GREY = (226, 228, 232)
RULE = (120, 110, 95)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, fill, max_w, leading=6):
    lines = wrap(draw, text, fnt, max_w)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def centre(draw, cx, y, text, fnt, fill):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text,
              font=fnt, fill=fill)
    return y + fnt.size


def kicker(draw, x, y, text, fill):
    f = font(SANS_B, 21)
    draw.text((x, y), text, font=f, fill=fill)
    return y + 30


def panel(draw, box, fill, outline=INK, width=2):
    draw.rounded_rectangle(box, radius=10, fill=fill, outline=outline,
                           width=width)


def ship_scene(draw, x0, y0, x1, y1):
    """A cargo ship on the sea with a drone strike bursting above it."""
    sea = (36, 78, 122)
    draw.rectangle([x0, y0, x1, y1], fill=(158, 196, 224))
    horizon = y0 + int((y1 - y0) * 0.52)
    draw.rectangle([x0, horizon, x1, y1], fill=sea)
    for i, yy in enumerate(range(horizon + 14, y1 - 6, 26)):
        w = 60 if i % 2 == 0 else 90
        xx = x0 + 18 + (i * 53) % (x1 - x0 - 110)
        draw.arc([xx, yy, xx + w, yy + 12], 0, 180, fill=(210, 232, 245),
                 width=3)
    # hull
    hx0, hx1 = x0 + 26, x1 - 26
    hy = horizon + 26
    draw.polygon([(hx0, hy), (hx1, hy), (hx1 - 26, hy + 42),
                  (hx0 + 34, hy + 42)], fill=(52, 52, 58))
    draw.rectangle([hx0 + 8, hy - 34, hx0 + 120, hy], fill=(88, 88, 96))
    draw.rectangle([hx0 + 128, hy - 52, hx0 + 158, hy], fill=(178, 34, 34))
    for wx in range(hx0 + 20, hx0 + 112, 22):
        draw.rectangle([wx, hy - 26, wx + 12, hy - 12], fill=(232, 182, 76))
    # smoke from the funnel
    for i, r in enumerate((16, 12, 9)):
        cx = hx0 + 143 + i * 16
        cy = hy - 62 - i * 16
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 120, 124))
    # explosion starburst above the bow
    ex, ey = x1 - 78, y0 + 52
    for ang in range(0, 360, 30):
        import math
        r1, r2 = 14, 44
        a = math.radians(ang)
        a2 = math.radians(ang + 15)
        draw.polygon([
            (ex + r1 * math.cos(a), ey + r1 * math.sin(a)),
            (ex + r2 * math.cos(a2), ey + r2 * math.sin(a2)),
            (ex + r1 * math.cos(math.radians(ang + 30)),
             ey + r1 * math.sin(math.radians(ang + 30))),
        ], fill=(240, 140, 40))
    draw.ellipse([ex - 18, ey - 18, ex + 18, ey + 18], fill=(250, 210, 90))


def tower_scene(draw, x0, y0, x1, y1):
    """A tall tower with a smoke plume from its crown (box-relative)."""
    s = (x1 - x0) / 160.0
    cx = (x0 + x1) // 2
    base = y1 - 4
    top = y0 + int(34 * s) + 8
    w = 52 * s
    draw.polygon([(cx - w, base), (cx - w * 0.58, top), (cx + w * 0.58, top),
                  (cx + w, base)], fill=(96, 96, 104))
    draw.rectangle([cx - 4 * s, top - 26 * s, cx + 4 * s, top],
                   fill=(96, 96, 104))
    draw.ellipse([cx - 6 * s, top - 34 * s, cx + 6 * s, top - 22 * s],
                 fill=(178, 34, 34))
    for row in range(4):
        yy = top + 14 * s + row * 20 * s
        for col in range(3):
            xx = cx - 30 * s + col * 22 * s + (row % 2) * 4 * s
            draw.rectangle([xx, yy, xx + 12 * s, yy + 10 * s],
                           fill=(232, 182, 76))
    # smoke plume curling from the crown
    for i, r in enumerate((10, 14, 18)):
        sx = cx + 22 * s + i * 16 * s
        sy = top - 30 * s - i * 14 * s
        rr = r * s
        draw.ellipse([sx - rr, sy - rr, sx + rr, sy + rr],
                     fill=(150, 150, 156))


def scales_scene(draw, x0, y0, x1, y1):
    """Scales of justice (box-relative)."""
    s = (x1 - x0) / 160.0
    cx = (x0 + x1) // 2
    base = y1 - 6
    top = y0 + 18 * s
    draw.rectangle([cx - 3 * s, top + 8 * s, cx + 3 * s, base],
                   fill=(52, 52, 58))
    draw.rectangle([cx - 56 * s, base, cx + 56 * s, base + 8 * s],
                   fill=(52, 52, 58))
    draw.line([cx - 62 * s, top + 16 * s, cx + 62 * s, top + 16 * s],
              fill=(52, 52, 58), width=max(2, int(6 * s)))
    draw.ellipse([cx - 8 * s, top, cx + 8 * s, top + 16 * s],
                 fill=(178, 34, 34))
    for side in (-1, 1):
        px = cx + side * 62 * s
        draw.line([px, top + 16 * s, px, top + 56 * s], fill=(52, 52, 58),
                  width=max(2, int(3 * s)))
        draw.polygon([(px - 34 * s, top + 56 * s), (px + 34 * s, top + 56 * s),
                      (px, top + 86 * s)], fill=(232, 182, 76),
                     outline=(52, 52, 58))


def radar_scene(draw, x0, y0, x1, y1):
    """Radar arcs with a jet silhouette (box-relative)."""
    s = (x1 - x0) / 160.0
    cx, cy = (x0 + x1) // 2, y1 - 10
    for r in (26, 46, 66):
        rr = r * s
        draw.arc([cx - rr, cy - rr, cx + rr, cy + rr], 180, 360,
                 fill=(14, 94, 94), width=max(2, int(4 * s)))
    jx, jy = cx + 34 * s, cy - 66 * s
    draw.polygon([(jx - 22 * s, jy), (jx + 22 * s, jy), (jx, jy - 10 * s)],
                 fill=(20, 20, 24))
    draw.polygon([(jx - 5 * s, jy), (jx + 5 * s, jy), (jx + 2 * s, jy + 10 * s),
                  (jx - 2 * s, jy + 10 * s)], fill=(20, 20, 24))

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 154], fill=GOLD)
    centre(d, W // 2, 16, "THE WORLD IN ONE DAY",
           font(SERIF_B, 62), (250, 248, 242))
    centre(d, W // 2, 92, "WEDNESDAY  ·  25 NOVEMBER 2026",
           font(SANS_B, 30), GOLD)

    # ---- Lead story: Ukraine strikes Russian ships ----------------------
    panel(d, [24, 168, 1000, 500], (232, 238, 244))
    ship_scene(d, 560, 186, 984, 482)
    kicker(d, 48, 186, "UKRAINE  •  WAR AT SEA", RED)
    y = draw_wrapped(d, 48, 224, "UKRAINE SINKS RUSSIAN WARSHIP",
                     font(SERIF_B, 48), INK, 490, leading=4)
    draw_wrapped(d, 48, y + 12,
                 "Kyiv confirms strikes on two Russian vessels: "
                 "one sunk off Libya, one hit in the Gulf of Finland.",
                 font(SANS, 23), (40, 40, 44), 490, leading=6)

    # ---- Row 2 ----------------------------------------------------------
    panel(d, [24, 516, 500, 716], SAND)
    tower_scene(d, 372, 524, 488, 622)
    kicker(d, 44, 532, "MIDDLE EAST", RED)
    y = draw_wrapped(d, 44, 566, "DRONE HITS RIYADH TOWER",
                     font(SERIF_B, 34), INK, 320, leading=2)
    draw_wrapped(d, 44, y + 8,
                 "Houthi strike wounds 11 at the capital's tallest tower.",
                 font(SANS, 21), (40, 40, 44), 440, leading=4)

    panel(d, [524, 516, 1000, 716], SKY)
    scales_scene(d, 872, 524, 988, 622)
    kicker(d, 544, 532, "UNITED STATES  •  COURTS", RED)
    y = draw_wrapped(d, 544, 566, "HUAWEI CONVICTED",
                     font(SERIF_B, 34), INK, 320, leading=2)
    draw_wrapped(d, 544, y + 8,
                 "US jury finds the tech giant guilty over its Iran business.",
                 font(SANS, 21), (40, 40, 44), 440, leading=4)

    # ---- Row 3 ----------------------------------------------------------
    panel(d, [24, 732, 500, 884], (244, 228, 224))
    kicker(d, 44, 748, "THE WAR'S TOLL", RED)
    d.text((44, 782), "700,000", font=font(SERIF_B, 58), fill=RED)
    draw_wrapped(d, 44, 846 - 6,
                 "Russian troops killed, a new analysis finds.",
                 font(SANS, 20), (40, 40, 44), 440, leading=4)

    panel(d, [524, 732, 1000, 884], (222, 236, 228))
    radar_scene(d, 872, 740, 988, 838)
    kicker(d, 544, 748, "EUROPE  •  SECURITY", RED)
    y = draw_wrapped(d, 544, 782, "NATO JETS FOR POLAND",
                     font(SERIF_B, 34), INK, 320, leading=2)
    draw_wrapped(d, 544, y + 8,
                 "Plus: EU adds new Russia sanctions.",
                 font(SANS, 21), (40, 40, 44), 440, leading=4)

    # ---- Bottom strip ---------------------------------------------------
    d.rectangle([24, 900, 1000, 1000], fill=NAVY)
    centre(d, W // 2, 912, "ALSO TODAY", font(SANS_B, 22), GOLD)
    centre(d, W // 2, 944,
           "Trump pardons turkeys Freedom & Feathers  •  GTA VI still No. 1  •  "
           "Tanker blasts in Hormuz",
           font(SANS, 20), (240, 238, 232))

    img.save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT} {W}x{H} {size} bytes")
    assert size <= 1048576, "image over the 1 MiB cap"


if __name__ == "__main__":
    build()
