#!/usr/bin/env python3
"""
prepare_portrait.py — turn a photo on a white background into a clean cut-out.

    python3 tools/prepare_portrait.py assets/img/portrait-source.png

The source is a studio shot on paper white, so the background is removed by a
flood fill from the border (white clothing or highlights *inside* the subject
are kept). A plain binary key is not enough: every anti-aliased edge pixel is a
blend of hair and white, so a straight mask leaves a pale halo around the head —
the "white outline" the page used to show against the night. This script

  1. keys the background,
  2. erodes the silhouette by `--erode` pixels so the halo falls outside it,
  3. rebuilds the removed rim band from pixel darkness, which keeps dark hair
     and skin but drops the white spill,
  4. un-composites white from the soft edge (F = (C - (1-a)·255) / a),
  5. feathers, trims and writes both WebP sizes.

    assets/img/portrait-cutout.webp      up to 1400px tall
    assets/img/portrait-cutout@800.webp  800px tall, for smaller screens

Requires Pillow and numpy. Nothing is uploaded anywhere.
"""
from __future__ import annotations

import argparse
import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SRC = ROOT / "assets" / "img" / "portrait-source.png"
DEFAULT_OUT = ROOT / "assets" / "img"


def background_mask(rgb: np.ndarray, tolerance: int) -> np.ndarray:
    """Pixels connected to the border that are close to paper white."""
    h, w, _ = rgb.shape
    mn = rgb.min(axis=2).astype(np.int16)
    mx = rgb.max(axis=2).astype(np.int16)
    # `mn` catches brightness, `mx - mn` rejects coloured skin and timber that
    # happen to be light. Both have to pass before a pixel can join the field.
    near_white = (mn >= 255 - tolerance) & ((mx - mn) <= max(14, tolerance))

    seen = np.zeros((h, w), dtype=bool)
    q: deque[tuple[int, int]] = deque()

    def push(y: int, x: int) -> None:
        if 0 <= y < h and 0 <= x < w and near_white[y, x] and not seen[y, x]:
            seen[y, x] = True
            q.append((y, x))

    for x in range(w):
        push(0, x)
        push(h - 1, x)
    for y in range(h):
        push(y, 0)
        push(y, w - 1)

    while q:
        y, x = q.popleft()
        push(y - 1, x)
        push(y + 1, x)
        push(y, x - 1)
        push(y, x + 1)
    return seen


def erode(mask: np.ndarray, radius: int) -> np.ndarray:
    """Shrink a boolean mask by `radius` pixels (square structuring element)."""
    if radius <= 0:
        return mask
    img = Image.fromarray((mask * 255).astype(np.uint8), mode="L")
    img = img.filter(ImageFilter.MinFilter(radius * 2 + 1))
    return np.asarray(img) > 127


def build_alpha(rgb: np.ndarray, bg: np.ndarray, radius: int, feather: float) -> np.ndarray:
    """Full-resolution alpha with the white halo rebuilt out of the silhouette.

    The studio backdrop bleeds two or three pixels into the hair. A binary mask
    keeps those pixels at alpha 255 and they composite as a bright outline. We
    therefore drop the outer `radius` band entirely, then give it back an alpha
    derived from how dark the pixel is: a dark strand survives, a near-white
    halo pixel does not. Skin at the jaw sits around 120–160 in its darkest
    channel and stays opaque.
    """
    solid = ~bg
    core = erode(solid, radius)
    rim = solid & ~core

    alpha = np.where(core, 1.0, 0.0).astype(np.float32)
    if radius > 0 and rim.any():
        mn = rgb.min(axis=2).astype(np.float32)
        # 255 -> 0 (pure backdrop), 180 and darker -> 1 (real subject)
        rim_a = np.clip((238.0 - mn) / 58.0, 0.0, 1.0)
        alpha = np.where(rim, rim_a, alpha)

    if feather > 0:
        soft = Image.fromarray((alpha * 255).astype(np.uint8), mode="L")
        soft = soft.filter(ImageFilter.GaussianBlur(feather))
        alpha = np.asarray(soft).astype(np.float32) / 255.0
    return alpha


def despill(rgb: np.ndarray, alpha: np.ndarray) -> np.ndarray:
    """Recover the subject colour from a pixel that was composited over white.

    C = a·F + (1-a)·255  =>  F = (C - (1-a)·255) / a. Applied once, to the
    transition band only, so no second pass can darken the edge.
    """
    out = rgb.astype(np.float32).copy()
    a = alpha[..., None]
    edge = (alpha > 0.02) & (alpha < 0.985)
    if edge.any():
        safe = np.clip(a, 1e-3, 1.0)
        un = (out - 255.0 * (1.0 - safe)) / safe
        out = np.where(edge[..., None], np.clip(un, 0.0, 255.0), out)
    return out


def drop_specks(alpha: np.ndarray, min_area: int = 24) -> np.ndarray:
    """Remove isolated flecks of backdrop left inside the hair."""
    solid = alpha > 0.08
    h, w = solid.shape
    seen = np.zeros((h, w), dtype=bool)
    out = alpha.copy()
    for y0 in range(h):
        for x0 in range(w):
            if not solid[y0, x0] or seen[y0, x0]:
                continue
            q = deque([(y0, x0)])
            seen[y0, x0] = True
            pixels = []
            while q:
                y, x = q.popleft()
                pixels.append((y, x))
                for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                    if 0 <= ny < h and 0 <= nx < w and solid[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        q.append((ny, nx))
            if len(pixels) < min_area:
                ys, xs = zip(*pixels)
                out[ys, xs] = 0.0
    return out


def cut_out(img: Image.Image, tolerance: int, radius: int, feather: float) -> Image.Image:
    img = img.convert("RGB")
    rgb = np.asarray(img, dtype=np.uint8)
    bg = background_mask(rgb, tolerance)
    alpha = build_alpha(rgb, bg, radius, feather)
    alpha = drop_specks(alpha)
    colour = despill(rgb, alpha)
    out = np.dstack([colour, alpha * 255.0]).astype(np.uint8)
    return Image.fromarray(out, mode="RGBA")


def main() -> int:
    ap = argparse.ArgumentParser(description="Remove a white background and write a portrait cut-out.")
    ap.add_argument("source", nargs="?", default=str(DEFAULT_SRC), help="input image (jpg/png/webp)")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="output directory")
    ap.add_argument("--tolerance", type=int, default=26, help="how close to white counts as background (0-60)")
    ap.add_argument("--erode", type=int, default=2, help="pixels of white halo to drop at the silhouette")
    ap.add_argument("--feather", type=float, default=0.9, help="edge feather radius in pixels")
    ap.add_argument("--height", type=int, default=1400, help="maximum output height")
    args = ap.parse_args()

    src = Path(args.source)
    if not src.exists():
        print(f"[x] Source not found: {src}", file=sys.stderr)
        print("    Put the original photo there, then run this again.", file=sys.stderr)
        return 1

    img = Image.open(src)
    img = img.convert("RGB")
    if max(img.size) > 2600:  # keep the flood fill quick, still plenty of detail
        scale = 2600 / max(img.size)
        img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)

    rgba = cut_out(img, args.tolerance, args.erode, args.feather)
    alpha = np.asarray(rgba.getchannel("A"))
    removed = float((alpha < 8).mean())

    if removed > 0.94:
        print(f"[x] {removed:.0%} of the image became transparent — tolerance is probably too high.", file=sys.stderr)
        return 2
    if removed < 0.02:
        print(f"[x] Almost nothing was removed ({removed:.1%}). Is the background actually white?", file=sys.stderr)
        return 2

    bbox = rgba.getbbox()
    if bbox:
        pad = round(max(rgba.size) * 0.01)
        bbox = (
            max(0, bbox[0] - pad),
            max(0, bbox[1] - pad),
            min(rgba.width, bbox[2] + pad),
            min(rgba.height, bbox[3] + pad),
        )
        rgba = rgba.crop(bbox)

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    def save(im: Image.Image, path: Path) -> None:
        im.save(path, "WEBP", quality=90, method=6)
        print(f"[+] {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path} "
              f"— {im.width}×{im.height}, {path.stat().st_size // 1024} KB")

    full = rgba
    if full.height > args.height:
        ratio = args.height / full.height
        full = full.resize((round(full.width * ratio), args.height), Image.LANCZOS)
    save(full, outdir / "portrait-cutout.webp")

    small = rgba
    if small.height > 800:
        ratio = 800 / small.height
        small = small.resize((round(small.width * ratio), 800), Image.LANCZOS)
    save(small, outdir / "portrait-cutout@800.webp")

    print(f"[i] background removed: {removed:.0%}  ·  subject {rgba.width}×{rgba.height}")
    print("[i] The site reads the cut-out at assets/img/portrait-cutout@800.webp.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
