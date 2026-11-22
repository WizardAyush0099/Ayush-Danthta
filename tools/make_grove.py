"""Build the deodar treeline cut-out used along the foot of the chapters.

The single specimen in assets/kage/fg/deodar-tree.webp is a clean, complete
tree on a transparent field. Rather than generate a second forest (and a
second set of needles that does not match), the band is composited from that
same specimen: two rows at different heights and hues, flipped and scaled
apart, with the bases sunk into a dark haze so the row reads as distance
rather than as the one tree pasted eleven times.

Run from the project root:  python3 tools/make_grove.py
"""

from pathlib import Path
from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "kage" / "fg" / "deodar-tree.webp"
OUT = ROOT / "assets" / "kage" / "fg" / "deodar-grove.webp"
PREVIEW = ROOT / "artifacts" / "grove-preview.png"

W, H = 2600, 820
BACK = (152, 168, 164)          # farther wood: cooler, lighter with distance
FRONT = (106, 124, 114)         # nearer wood: deeper, the silhouette that reads

src = Image.open(SRC).convert("RGBA")
tree = src.crop(src.getchannel("A").getbbox())


def stamp(canvas, height, cx, baseline, tint, flip=False):
    w = max(1, round(tree.width * height / tree.height))
    t = tree.resize((w, height), Image.LANCZOS)
    if flip:
        t = t.transpose(Image.FLIP_LEFT_RIGHT)
    t = ImageChops.multiply(t, Image.new("RGBA", t.size, tint + (255,)))
    canvas.alpha_composite(t, (round(cx - w / 2), round(baseline - height)))


def haze(canvas, top, bottom, alpha_top, alpha_bottom):
    """A vertical ink wash, so trunks dissolve into the page's night."""
    band = Image.new("RGBA", (W, bottom - top), (0, 0, 0, 0))
    d = ImageDraw.Draw(band)
    for y in range(band.height):
        u = y / max(1, band.height - 1)
        a = round(alpha_top + (alpha_bottom - alpha_top) * u)
        d.line([(0, y), (W, y)], fill=(6, 10, 14, a))
    canvas.alpha_composite(band, (0, top))


canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))

# the far row: overlapping, so the crown line stays unbroken like a real
# hillside belt rather than reading as eleven separate specimens
back = [(120, 350), (330, 372), (540, 338), (755, 366), (965, 346),
        (1175, 378), (1385, 340), (1595, 368), (1805, 348), (2015, 374),
        (2225, 342), (2440, 362), (2620, 350)]
for i, (cx, h) in enumerate(back):
    stamp(canvas, h, cx, H - 40 + (i % 3) * 16, BACK, flip=bool(i % 2))

haze(canvas, H - 300, H - 100, 0, 96)
haze(canvas, H - 110, H, 96, 210)

# the near row: fewer, taller, their bases off the bottom edge
front = [(90, 600), (470, 540), (870, 645), (1290, 560), (1700, 620),
         (2120, 545), (2520, 612)]
for i, (cx, h) in enumerate(front):
    stamp(canvas, h, cx, H + 8 + (i % 2) * 18, FRONT, flip=bool(i % 2))

# a breath of fog between the rows and over the whole base
haze(canvas, H - 210, H, 26, 150)

OUT.parent.mkdir(parents=True, exist_ok=True)
canvas.save(OUT, "WEBP", quality=86, method=6)
print(f"wrote {OUT.relative_to(ROOT)} — {OUT.stat().st_size:,} bytes, {canvas.size}")

# a dark-ground proof, because the panel renders transparency on white
PREVIEW.parent.mkdir(parents=True, exist_ok=True)
proof = Image.new("RGBA", canvas.size, (7, 11, 15, 255))
proof.alpha_composite(canvas)
proof.convert("RGB").save(PREVIEW)
print(f"wrote {PREVIEW.relative_to(ROOT)}")
