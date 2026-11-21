#!/usr/bin/env python3
"""
prepare_portrait.py — turn a photo on a white background into a clean cut-out.

    python3 tools/prepare_portrait.py assets/img/portrait-source.png

It flood-fills the white field from the image border (so white clothing or
highlights *inside* the subject are kept), feathers the edge, removes the white
fringe, trims to the subject and writes:

    assets/img/portrait-cutout.webp      (up to 1400px tall)
    assets/img/portrait-cutout@800.webp  (800px tall, for smaller screens)

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
    """Pixels connected to the border that are close to white."""
    h, w, _ = rgb.shape
    # whiteness: bright and low saturation
    mx = rgb.max(axis=2).astype(np.int16)
    mn = rgb.min(axis=2).astype(np.int16)
    near_white = (mn >= 255 - tolerance) & ((mx - mn) <= max(12, tolerance // 2))

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


def cut_out(img: Image.Image, tolerance: int, feather: float) -> Image.Image:
    img = img.convert("RGB")
    rgb = np.asarray(img, dtype=np.uint8)
    bg = background_mask(rgb, tolerance)

    alpha = np.where(bg, 0, 255).astype(np.uint8)
    alpha_img = Image.fromarray(alpha, mode="L")
    if feather > 0:
        alpha_img = alpha_img.filter(ImageFilter.GaussianBlur(feather))
    a = np.asarray(alpha_img, dtype=np.float32) / 255.0

    # decontaminate the white fringe: solve orig = fg*a + white*(1-a)
    fg = rgb.astype(np.float32)
    safe = np.clip(a, 1e-3, 1.0)[..., None]
    unpremult = (fg - 255.0 * (1.0 - safe)) / safe
    edge = ((a > 0.02) & (a < 0.98))[..., None]
    fg = np.where(edge, np.clip(unpremult, 0, 255), fg)

    out = np.dstack([fg, a * 255.0]).astype(np.uint8)
    return Image.fromarray(out, mode="RGBA")


def decontaminate(rgba: "Image.Image") -> "Image.Image":
    """Remove the white backdrop's contribution from soft edge pixels.

    A part-transparent pixel is the subject composited over white:
    C = a*F + (1-a)*255. Inverting that (F = (C - (1-a)*255) / a) recovers the
    subject's real colour there, which is what kills the pale halo you
    otherwise get around hair when the cut-out sits on a dark page.
    """
    arr = np.asarray(rgba).astype(np.float32)
    rgb = arr[..., :3]
    a = arr[..., 3:4] / 255.0
    safe = np.maximum(a, 1e-3)
    recovered = np.clip((rgb - (1.0 - safe) * 255.0) / safe, 0.0, 255.0)
    edge = (a > 0.004) & (a < 0.995)
    arr[..., :3] = np.where(edge, recovered, rgb)
    return Image.fromarray(arr.astype(np.uint8), mode="RGBA")


def main() -> int:
    ap = argparse.ArgumentParser(description="Remove a white background and write a portrait cut-out.")
    ap.add_argument("source", nargs="?", default=str(DEFAULT_SRC), help="input image (jpg/png/webp)")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="output directory")
    ap.add_argument("--tolerance", type=int, default=18, help="how close to white counts as background (0-60)")
    ap.add_argument("--feather", type=float, default=0.8, help="edge feather radius in pixels")
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

    rgba = decontaminate(cut_out(img, args.tolerance, args.feather))
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
    print("[i] The site switches to the cut-out when the file exists (html.has-photo).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
