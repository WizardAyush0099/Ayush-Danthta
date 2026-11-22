"""Rebuild the last two Kyoto cut-outs as Himachal material.

The deodar, the slate stones and the treeline are already Himalayan. Two pieces
of the near plane were still the ThreeUI library: a bank of Japanese silver
grass in full feathery plume (susuki), and a bare rounded Japanese hill.

Both are rebuilt here, and neither is invented from nothing:

  hill.webp       the crest curves are *measured* off assets/img/hp/ridge.webp,
                  the supplied Dhauladhar photograph — the same spurs, redrawn
                  as bedded slate with a forested fringe.
  tall-grass.webp a tussock bank of Himalayan grass: upright blades, wide
                  arching leaves, compact seed spikes (no plume), and a few
                  rust bracken fronds, i.e. the forest floor in forest.webp.

Every colour is sampled from the supplied photographs and then graded to the
page's night, so the cut-outs sit in the same ink as the rest of the scene.

The file names and pixel dimensions are deliberately unchanged, so the HTML
boxes, the aspect-ratio attributes and every CSS placement rule stay as they
were: the artwork is replaced, the layout is not touched.

    assets/kage/fg/tall-grass.webp   1717 x 916
    assets/kage/fg/hill.webp         1774 x 887

Run from the project root:  python3 tools/make_fg.py
"""

import colorsys
import math
import random
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
PHOTO = ROOT / "assets" / "img" / "hp"
OUT = ROOT / "assets" / "kage" / "fg"
ART = ROOT / "artifacts"

GRASS = OUT / "tall-grass.webp"
RIDGE = OUT / "hill.webp"
PROOF = ART / "fg-proof.png"

INK = (6, 10, 14)


# --------------------------------------------------------------- colour
def median_rgb(img, box):
    """The middle colour of a region: the supplied photograph, unposed."""
    crop = img.crop(box).convert("RGB").resize((48, 48), Image.LANCZOS)
    raw = crop.tobytes()
    px = [tuple(raw[i:i + 3]) for i in range(0, len(raw), 3)]
    px.sort(key=lambda c: c[0] * 0.299 + c[1] * 0.587 + c[2] * 0.114)
    return px[len(px) // 2]


def tone(rgb, value, sat):
    """Push a photographed colour down to the night the page is lit by.

    Hue is kept exactly — that is the part that says Himalaya rather than
    Kyoto — while the value is set outright, because a photograph's daylight
    brightness has no meaning in a scene lit by one moon.
    """
    r, g, b = (c / 255 for c in rgb)
    h, s, _ = colorsys.rgb_to_hsv(r, g, b)
    r, g, b = colorsys.hsv_to_rgb(h, min(1.0, s * sat), value)
    return tuple(max(0, min(255, round(c * 255))) for c in (r, g, b))


def jitter(rgb, rnd, amount=7):
    d = rnd.randint(-amount, amount)
    return tuple(max(0, min(255, c + d)) for c in rgb)


def ink_wash(canvas, top, bottom, alpha_top, alpha_bottom, colour=INK):
    """A vertical wash of page ink, so a base dissolves into the scene."""
    top, bottom = int(top), int(bottom)
    if bottom <= top:
        return
    band = Image.new("RGBA", (canvas.width, bottom - top), (0, 0, 0, 0))
    d = ImageDraw.Draw(band)
    for y in range(band.height):
        u = y / max(1, band.height - 1)
        a = round(alpha_top + (alpha_bottom - alpha_top) * u)
        d.line([(0, y), (canvas.width, y)], fill=colour + (a,))
    canvas.alpha_composite(band, (0, top))


# --------------------------------------------------------------- ridge
def _median(a, k):
    half = k // 2
    out = []
    for i in range(len(a)):
        w = sorted(a[max(0, i - half): i + half + 1])
        out.append(w[len(w) // 2])
    return out


def _smooth(a, k):
    pre = [0.0]
    for v in a:
        pre.append(pre[-1] + v)
    half = k // 2
    out = []
    for i in range(len(a)):
        lo, hi = max(0, i - half), min(len(a), i + half + 1)
        out.append((pre[hi] - pre[lo]) / (hi - lo))
    return out


def crest_from_photo(img, y_start, thresh):
    """Where the sky ends, column by column, measured in the photograph.

    A wide median pass throws away the thin transmission tower and the odd
    cloud edge; the moving average after it leaves a crest that is a ridge and
    not a plot of noise.
    """
    g = img.convert("L")
    w, h = g.size
    px = g.load()
    rows = []
    for x in range(w):
        y = h - 1
        for yy in range(y_start, h):
            if px[x, yy] < thresh:
                y = yy
                break
        rows.append(y)
    rows = _smooth(_median(rows, 51), 61)
    # height above the base of the frame, normalised so the highest spur is 1
    prof = [(h - y) / h for y in rows]
    hi = max(prof)
    return [p / hi if hi else 0.0 for p in prof]


def resample(prof, n):
    out = []
    last = len(prof) - 1
    for i in range(n):
        u = i / n * last
        i0 = int(math.floor(u))
        i1 = min(last, i0 + 1)
        f = u - i0
        out.append(prof[i0] * (1 - f) + prof[i1] * f)
    return out


def smoothstep(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def envelope(points, u):
    """The composition: a dominant spur left of centre, shoulders to the right.

    The photographed crest supplies the shape of each ridge; this supplies the
    framing, so the copy on the right of the chapter keeps its sky.
    """
    for i in range(len(points) - 1):
        u0, v0 = points[i]
        u1, v1 = points[i + 1]
        if u0 <= u <= u1:
            return v0 + (v1 - v0) * smoothstep((u - u0) / (u1 - u0))
    return points[-1][1]


def tufts(d, crest, x0, x1, rnd, colour, scale=1.0, alpha=225):
    """A conifer fringe on a crest line: the ridge is wooded, not bare stone."""
    x = x0
    while x < x1:
        y = crest[min(len(crest) - 1, int(x))]
        # stands with gaps between them, not a comb along the whole skyline
        if rnd.random() < 0.22:
            x += rnd.uniform(9, 26) * scale
            continue
        h = rnd.choice((3, 4, 5, 6, 8, 9, 12, 16, 21)) * scale
        w = max(1.6, h * rnd.uniform(0.30, 0.46))
        # a deodar silhouette: a spire with two stepped shoulders
        d.polygon(
            [(x, y - h),
             (x - w * 0.55, y - h * 0.42),
             (x - w * 0.30, y - h * 0.40),
             (x - w * 0.72, y + 1.5),
             (x + w * 0.72, y + 1.5),
             (x + w * 0.30, y - h * 0.40),
             (x + w * 0.55, y - h * 0.42)],
            fill=colour + (alpha,),
        )
        if h > 9 and rnd.random() < 0.5:
            d.line([(x, y + 1), (x, y + h * 0.55)], fill=colour + (alpha,), width=1)
        x += rnd.uniform(5.0, 13.0) * scale


def ridge_layer(canvas, prof, env_pts, base_y, amp, tint, hi, lo, fringe,
                rnd, flip=False, shift=0.0, below=1.02, strata=True, phase=0.0,
                soft=0.0):
    """One spur: a slate mass under a measured crest, bedded, fringed, hazed."""
    W, H = canvas.size
    n = len(prof)
    src = prof[::-1] if flip else prof

    def at(t):
        """Sample the skyline, mirrored at both ends.

        Each spur reads a different stretch of the photographed crest so the
        ridges cross instead of nesting in parallel. The wrap has to be a
        mirror and not a jump: a modular wrap leaves a vertical seam in the
        silhouette exactly where the profile restarts.
        """
        pos = (t % 1.0) * (2 * (n - 1))
        i = int(pos)
        if i >= n - 1:
            i = 2 * (n - 1) - i - 1
        return src[max(0, min(n - 1, i))]

    crest = []
    for x in range(W):
        u = x / (W - 1)
        p = at(u + shift)
        # A slow swell, so no crest runs dead flat along the frame edge. The
        # photograph's profile goes to zero in the hazy valleys, and without
        # this those stretch of skyline become ruled horizontals.
        swell = (1.0
                 + 0.060 * math.sin(u * 5.1 + phase)
                 + 0.042 * math.sin(u * 9.7 + phase * 2.3)
                 + 0.026 * math.sin(u * 17.3 + phase * 0.7))
        y = base_y - amp * envelope(env_pts, u) * (0.32 + 0.68 * p) * swell
        # keep every point inside the frame: a crest that dips below the bottom
        # edge turns the fill polygon inside out and leaves a vertical crease
        crest.append(min(H - 0.5, y))
    crest = _smooth(crest, 9)

    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    md.polygon([(0, H)] + [(x, crest[x]) for x in range(0, W, 2)] + [(W, H)], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(0.7))

    rock = Image.new("RGBA", (W, H), tint + (255,))

    # A faint vertical fall-off inside the mass: slate light at the crest, the
    # valley floor in shadow. Flat fill is what makes a cut-out read as paper.
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    top = min(crest)
    span = max(1.0, H - top)
    for y in range(max(0, int(math.floor(top))), H):
        a = round(90 * max(0.0, (y - top) / span) ** 0.8)
        sd.line([(0, y), (W, y)], fill=(0, 0, 0, a))
    rock.alpha_composite(shade)

    if strata:
        # Bedded slate, seen from across a valley: short joints and the odd
        # pale ledge, never a ruled contour across the whole spur.
        d = ImageDraw.Draw(rock)
        crest_mean = sum(crest) / len(crest)
        for _ in range(90):
            y = rnd.uniform(crest_mean + 10, H * below)
            k = rnd.uniform(0.24, 0.66)
            pale = rnd.random() < 0.45
            col = (hi if pale else lo) + (rnd.randint(4, 9) if pale else rnd.randint(14, 26),)
            x = rnd.randint(-30, W - 10)
            run = rnd.randint(int(W * 0.03), int(W * 0.13))
            wob = rnd.uniform(-2.0, 2.0)
            pts = [(xx, y + k * (crest[min(W - 1, xx)] - crest_mean)
                    + wob * math.sin(xx / 210.0))
                   for xx in range(max(0, x), min(W, x + run), 6)]
            if len(pts) > 1:
                d.line(pts, fill=col, width=rnd.choice((1, 1, 2)))

    rock.putalpha(ImageChops.multiply(rock.getchannel("A"), mask))
    if soft:
        rock = rock.filter(ImageFilter.GaussianBlur(soft))
    canvas.alpha_composite(rock)

    # the moon catches the crest, one thin line and nothing more
    rim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rim)
    rd.line([(x, crest[x] + 1.6) for x in range(0, W, 2)], fill=(112, 128, 124, 22), width=2)
    rim.putalpha(ImageChops.multiply(rim.getchannel("A"), mask))
    canvas.alpha_composite(rim)

    if fringe:
        fr = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        tufts(ImageDraw.Draw(fr), crest, -6, W + 6, rnd, fringe, scale=1.0)
        canvas.alpha_composite(fr)


def build_ridge():
    W, H = 1774, 887
    photo = Image.open(PHOTO / "ridge.webp")
    rnd = random.Random(20261122)

    # the near, dark spurs and the mid spurs, both read straight off the photo
    near = crest_from_photo(photo, 250, 132)
    mid = crest_from_photo(photo, 150, 176)
    far = crest_from_photo(photo, 120, 198)

    near = resample(_smooth(near, 25), W)
    mid = resample(_smooth(mid, 25), W)
    far = resample(_smooth(far, 25), W)

    # slate sampled from the shadowed ridge of the same photograph, and the
    # wood tint from the deodar belt, so the ridge belongs to both
    slate_src = median_rgb(photo, (1080, 350, 1600, 500))
    forest_src = median_rgb(Image.open(PHOTO / "forest.webp"), (0, 420, 452, 678))

    FAR = tone(slate_src, 0.196, 0.62)
    MID = tone(slate_src, 0.146, 0.58)
    NEAR = tone(slate_src, 0.104, 0.52)
    WOOD = tone(forest_src, 0.048, 0.50)
    WOOD_FAR = tone(forest_src, 0.075, 0.44)
    HI = tone(slate_src, 0.300, 0.30)

    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    # --- the far spur, almost throat: the snow line's foothills
    ridge_layer(canvas, near, [(0, 0.52), (0.18, 0.94), (0.42, 0.80),
                               (0.66, 0.66), (1.0, 0.58)],
                base_y=H * 0.92, amp=H * 0.50, tint=FAR, hi=HI, lo=(0, 0, 0),
                fringe=WOOD_FAR, rnd=rnd, flip=True, shift=0.18, phase=0.4,
                below=0.98, soft=1.1)
    ink_wash(canvas, H * 0.46, H * 0.92, 0, 104)

    # --- the mid spur, carrying most of the silhouette
    ridge_layer(canvas, near, [(0, 0.66), (0.12, 1.00), (0.30, 0.94),
                               (0.54, 0.76), (0.78, 0.62), (1.0, 0.52)],
                base_y=H * 1.02, amp=H * 0.60, tint=MID, hi=HI, lo=(0, 0, 0),
                fringe=WOOD_FAR, rnd=rnd, flip=False, shift=0.63, phase=2.1,
                below=1.0, soft=0.45)
    ink_wash(canvas, H * 0.58, H, 0, 100)

    # --- the near foreshortened spur, dark enough to read as silhouette
    ridge_layer(canvas, mid, [(0, 0.78), (0.10, 1.04), (0.26, 0.98),
                              (0.48, 0.82), (0.72, 0.66), (1.0, 0.56)],
                base_y=H * 1.22, amp=H * 0.80, tint=NEAR, hi=HI, lo=(0, 0, 0),
                fringe=WOOD, rnd=rnd, flip=True, shift=0.42, phase=3.7, below=1.0)

    ink_wash(canvas, H * 0.80, H, 0, 210)

    RIDGE.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(RIDGE, "WEBP", quality=87, method=6)
    print(f"wrote {RIDGE.relative_to(ROOT)} — {RIDGE.stat().st_size:,} bytes, {canvas.size}")
    return canvas


# --------------------------------------------------------------- grass
def mix(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def blade(d, x0, y0, hgt, lean, bend, w0, col, rim=None, tip=None, steps=16):
    """One tapering blade: a quadratic spine with width falling to the tip.

    The upper half is drawn again in a lighter tone, which is what a blade
    actually does — it turns its face to the sky and catches the light — and
    what stops a dense bank from reading as a bundle of sticks.
    """
    xt, yt = x0 + lean, y0 - hgt
    cx, cy = x0 + lean * 0.30 + bend, y0 - hgt * 0.56
    left, right = [], []
    for i in range(steps + 1):
        t = i / steps
        mt = 1 - t
        x = mt * mt * x0 + 2 * mt * t * cx + t * t * xt
        y = mt * mt * y0 + 2 * mt * t * cy + t * t * yt
        dx = 2 * mt * (cx - x0) + 2 * t * (xt - cx)
        dy = 2 * mt * (cy - y0) + 2 * t * (yt - cy)
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L, dx / L
        w = w0 * (1 - t) ** 0.72
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    d.polygon(left + right[::-1], fill=col)
    if tip:
        j = max(2, int(steps * 0.46))
        poly = left[j:] + right[j:][::-1]
        if len(poly) > 2:
            d.polygon(poly, fill=tip + (108,))
    if rim:
        d.line(left[3:], fill=rim, width=max(1, int(round(w0 * 0.26))))


def seed_head(d, x0, y0, hgt, lean, droop, col, tip_col, rnd):
    """A compact spike, not a plume.

    Pampas/susuki hangs a feather off its stem; the grasses of the deodar belt
    hold a short, tight spike of seed with a few angled bristles.
    """
    xt, yt = x0 + lean, y0 - hgt
    cx, cy = x0 + lean * 0.4, y0 - hgt * 0.62
    pts = []
    for i in range(19):
        t = i / 18
        mt = 1 - t
        pts.append((mt * mt * x0 + 2 * mt * t * cx + t * t * xt,
                    mt * mt * y0 + 2 * mt * t * cy + t * t * yt))
    d.line(pts, fill=col, width=5)
    # the spike occupies the top of the stem; barbs alternate down it
    ang = math.atan2(pts[-1][1] - pts[-2][1], pts[-1][0] - pts[-2][0])
    n = rnd.randint(7, 11)
    for i in range(n):
        t = i / (n - 1)
        px, py = pts[-1 - int(round(t * 4))]
        side = 1 if i % 2 == 0 else -1
        ln = (10 + 13 * (1 - t)) * rnd.uniform(0.7, 1.1)
        a = ang + side * (0.72 + 0.35 * rnd.random()) + droop * 0.35
        d.line([(px, py), (px + math.cos(a) * ln, py + math.sin(a) * ln)],
               fill=col, width=4)
        if i % 3 == 1:
            d.line([(px, py), (px + math.cos(a + 0.5) * ln * 0.5,
                               py + math.sin(a + 0.5) * ln * 0.5)],
                   fill=tip_col, width=3)
    d.line(pts[-5:], fill=tip_col, width=5)


def frond(d, x0, y0, hgt, lean, bend, col, tip, rnd, steps=19):
    """A bracken frond: a rachis carrying paired pinnae.

    Bracken is the real cover under the deodar belt, and it is the honest
    answer to what the feathery plume was doing in the composition — it fills
    the upper band of the bank without borrowing anything from Kyoto.
    """
    xt, yt = x0 + lean, y0 - hgt
    cx, cy = x0 + lean * 0.25 + bend, y0 - hgt * 0.64
    spine = []
    for i in range(steps + 1):
        t = i / steps
        mt = 1 - t
        spine.append((mt * mt * x0 + 2 * mt * t * cx + t * t * xt,
                      mt * mt * y0 + 2 * mt * t * cy + t * t * yt))
    d.line(spine, fill=col, width=max(2, round(hgt * 0.010)))
    L = hgt * 0.105
    for i in range(1, steps):
        t = i / steps
        px, py = spine[i]
        a = math.atan2(spine[i + 1][1] - spine[i - 1][1],
                       spine[i + 1][0] - spine[i - 1][0])
        # pinnae are longest past the base and shorten towards the curled tip
        ln = L * math.sin(math.pi * (0.16 + 0.80 * t)) ** 0.55
        for side in (-1, 1):
            aa = a + side * (0.66 + rnd.uniform(-0.16, 0.16))
            ex, ey = px + math.cos(aa) * ln, py + math.sin(aa) * ln
            nx, ny = -math.sin(aa) * ln * 0.13, math.cos(aa) * ln * 0.13
            d.polygon([(px, py),
                       ((px + ex) / 2 - nx, (py + ey) / 2 - ny),
                       (ex, ey),
                       ((px + ex) / 2 + nx, (py + ey) / 2 + ny)],
                      fill=col)
    d.line(spine[-5:], fill=tip, width=max(2, round(hgt * 0.009)))


def build_grass():
    W, H = 1717, 916
    SS = 3
    cw, ch = W * SS, H * SS
    rnd = random.Random(20261122)

    floor = Image.open(PHOTO / "forest.webp")
    needles = Image.open(PHOTO / "fir.webp")
    ridge_photo = Image.open(PHOTO / "ridge.webp")
    forest_src = median_rgb(floor, (0, 400, 452, 678))     # lit understory
    needle_src = median_rgb(needles, (60, 120, 400, 520))  # deodar needles
    dry_src = median_rgb(floor, (0, 300, 452, 360))        # leaf litter
    slate_src = median_rgb(ridge_photo, (1080, 350, 1600, 500))

    DEEP = tone(forest_src, 0.070, 0.55)
    MID = tone(forest_src, 0.112, 0.58)
    LIT = tone(needle_src, 0.160, 0.52)
    RIM = tone(needle_src, 0.250, 0.40)
    MOON = tone(slate_src, 0.250, 0.34)
    DRY = tone(dry_src, 0.135, 0.62)
    STRAW = tone(dry_src, 0.195, 0.52)

    def field(x):
        """A soft density field: clumps and gaps, so the bank is not a lawn."""
        u = x / cw
        return (0.62
                + 0.26 * math.sin(u * 11.3 + 0.7)
                + 0.16 * math.sin(u * 23.1 + 2.1)
                + 0.10 * math.sin(u * 41.7 + 4.4))

    def clumped_x():
        """Blades grow in tufts; uniform scatter is what looks planted."""
        if rnd.random() < 0.5:
            return rnd.gauss(rnd.uniform(0, cw), cw * 0.028)
        return rnd.uniform(-50, cw + 50)

    canvas = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))

    # --- the sward: the mass every blade grows out of, so the bank has a floor
    #     instead of showing the page through the gaps between stems
    sward = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    sw = ImageDraw.Draw(sward)
    edge = []
    for x in range(-20, cw + 20, 10):
        u = x / cw
        edge.append((x, ch * 0.982
                     - ch * 0.020 * (0.5 + 0.5 * math.sin(u * 17.0))
                     - ch * 0.012 * (0.5 + 0.5 * math.sin(u * 43.0 + 1.3))
                     - ch * 0.009 * (0.5 + 0.5 * math.sin(u * 97.0 + 2.6))
                     - rnd.uniform(0, ch * 0.009)))
    sw.polygon(edge + [(cw + 20, ch), (-20, ch)],
               fill=tone(forest_src, 0.048, 0.5) + (244,))
    canvas.alpha_composite(sward)

    # Four depth passes. Each is drawn on its own sheet, softened by its own
    # amount, and laid down in order: the bank takes its density from overlap
    # and its depth from the fog between the passes, not from wider strokes.
    passes = (
        # count, h0, h1, w0, w1, v0, v1, blur, sat
        (2400, 0.05, 0.19, 3.0, 6.5, 0.042, 0.070, 3.0, 0.40),
        (3000, 0.12, 0.32, 4.0, 8.5, 0.058, 0.098, 1.5, 0.50),
        (2300, 0.20, 0.40, 5.0, 10.0, 0.076, 0.128, 0.5, 0.56),
        (1050, 0.28, 0.52, 5.5, 11.5, 0.090, 0.152, 0.0, 0.58),
    )
    for pi, (count, h0, h1, w0, w1, v0, v1, blur, sat) in enumerate(passes):
        sheet = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        d = ImageDraw.Draw(sheet)
        for _ in range(count):
            x = clumped_x()
            f = max(0.24, field(x))
            hgt = ch * rnd.uniform(h0, h1) * f
            lean = rnd.uniform(-0.34, 0.40) * hgt
            bend = rnd.uniform(-0.26, 0.26) * hgt
            width = rnd.uniform(w0, w1) * SS / 3
            roll = rnd.random()
            if roll < 0.085:
                col = jitter(DRY, rnd, 7)                  # bracken, gone rust
                tip = mix(col, STRAW, 0.60)
            elif roll < 0.50:
                col = jitter(tone(forest_src, rnd.uniform(v0, v1), sat), rnd, 6)
                tip = mix(col, LIT, 0.34)
            elif roll < 0.86:
                col = jitter(DEEP, rnd, 4)
                tip = mix(col, MID, 0.50)
            else:
                col = jitter(LIT, rnd, 6)
                tip = mix(col, MOON, 0.34)
            blade(d, x, ch + rnd.uniform(0, ch * 0.07), hgt, lean, bend, width,
                  col, tip=tip)
        if blur:
            sheet = sheet.filter(ImageFilter.GaussianBlur(blur))
        canvas.alpha_composite(sheet)
        if pi < len(passes) - 1:
            ink_wash(canvas, ch * (0.50 - 0.05 * pi), ch, 0, 20 + 9 * pi)

    # --- broad arching leaves: the one shape that keeps the bank from reading
    #     as lawn, and the shape the old plume was carrying
    top = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    td = ImageDraw.Draw(top)
    for _ in range(24):
        x = rnd.uniform(cw * 0.01, cw * 0.99)
        hgt = ch * rnd.uniform(0.17, 0.33)
        col = jitter(tone(dry_src, rnd.uniform(0.105, 0.135), 0.55), rnd, 5)
        # bracken arches over rather than standing up like an umbrella
        frond(td, x, ch + rnd.uniform(0, ch * 0.03), hgt,
              rnd.uniform(-0.46, 0.46) * hgt, rnd.uniform(-0.52, 0.52) * hgt,
              col, mix(col, STRAW, 0.45), rnd)

    for _ in range(130):
        x = rnd.uniform(cw * 0.02, cw * 0.98)
        hgt = ch * rnd.uniform(0.20, 0.42)
        width = rnd.uniform(20.0, 34.0) * SS / 3
        lean = rnd.uniform(-0.38, 0.38) * hgt
        col = jitter(MID, rnd, 5) if rnd.random() < 0.7 else jitter(DRY, rnd, 7)
        blade(td, x, ch + rnd.uniform(0, 10), hgt, lean,
              rnd.uniform(-0.18, 0.18) * hgt, width, col,
              tip=mix(col, MOON, 0.22), rim=jitter(RIM, rnd, 6), steps=18)

    # --- seed heads: upright spikes over the mat, a few of them drooping
    for _ in range(22):
        x = rnd.uniform(cw * 0.02, cw * 0.98)
        hgt = ch * rnd.uniform(0.46, 0.68)
        seed_head(td, x, ch + rnd.uniform(0, ch * 0.04), hgt,
                  rnd.uniform(-0.20, 0.20) * hgt,
                  rnd.uniform(-1.0, 1.0),
                  jitter(STRAW, rnd, 6), jitter(mix(STRAW, MOON, 0.5), rnd, 8), rnd)
    canvas.alpha_composite(top)

    canvas = canvas.resize((W, H), Image.LANCZOS)
    ink_wash(canvas, H * 0.72, H, 0, 176)

    GRASS.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(GRASS, "WEBP", quality=87, method=6)
    print(f"wrote {GRASS.relative_to(ROOT)} — {GRASS.stat().st_size:,} bytes, {canvas.size}")
    return canvas


def proof(ridge, grass):
    """A dark-ground proof at roughly page scale.

    The panel renders transparency on white, which would hide every mistake in
    a night silhouette, so both cut-outs are checked against the page ink.
    """
    W, H = 1280, 760
    canvas = Image.new("RGBA", (W, H), (7, 11, 15, 255))
    d = ImageDraw.Draw(canvas)
    for y in range(H):
        u = y / H
        d.line([(0, y), (W, y)], fill=(7 + round(6 * u), 11 + round(8 * u),
                                       15 + round(10 * u), 255))
    r = ridge.resize((1180, round(1180 * ridge.height / ridge.width)), Image.LANCZOS)
    canvas.alpha_composite(r, (10, H - r.height + 40))
    g = grass.resize((680, round(680 * grass.height / grass.width)), Image.LANCZOS)
    canvas.alpha_composite(g, (W - g.width + 60, H - g.height + 30))
    ART.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(PROOF)
    print(f"wrote {PROOF.relative_to(ROOT)}")

    # each piece alone, at the size the page draws it, on the same ink
    solo = Image.new("RGBA", (1180, 620), (7, 11, 15, 255))
    solo.alpha_composite(r, (10, 620 - r.height + 30))
    solo.convert("RGB").save(ART / "fg-ridge.png")
    solo = Image.new("RGBA", (700, 460), (7, 11, 15, 255))
    solo.alpha_composite(grass.resize((700, round(700 * grass.height / grass.width)),
                                      Image.LANCZOS), (0, 460 - 340))
    solo.convert("RGB").save(ART / "fg-grass.png")
    print(f"wrote {ART.relative_to(ROOT)}/fg-ridge.png, fg-grass.png")


if __name__ == "__main__":
    proof(build_ridge(), build_grass())
