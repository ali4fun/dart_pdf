#!/usr/bin/env python3
"""Turn a flat 2D product photo into a "3D photo".

The script takes a single still image (local path or URL), estimates a simple
depth map and uses depth-image-based rendering (DIBR) to synthesise new camera
viewpoints. From those viewpoints it produces three "3D" deliverables:

* a red/cyan **anaglyph** (view with red-cyan glasses),
* a cross-eyed **stereo pair** (side-by-side left/right image),
* an animated **wiggle GIF** that rocks between viewpoints so the subject
  visibly pops out of the background (no glasses required).

It is tuned for the common e-commerce case of a single object photographed on
a bright, near-uniform background: the foreground subject is segmented from the
background and given a rounded, "closer to the camera" depth so it parallaxes
against the flat backdrop. The code falls back to gradient-based cues for
photos that do not match that assumption, so it still works on arbitrary
images.

Usage:
    python3 make_3d_photo.py SOURCE [--out-dir DIR] [--max-shift PX]
                                     [--frames N] [--fps F]

SOURCE may be a local file path or an http(s) URL.
"""

from __future__ import annotations

import argparse
import io
import sys
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage


def load_image(source: str) -> Image.Image:
    """Load an image from a local path or an http(s) URL."""
    if source.startswith(("http://", "https://")):
        req = urllib.request.Request(source, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
        return Image.open(io.BytesIO(data)).convert("RGB")
    return Image.open(source).convert("RGB")


def estimate_depth(rgb: np.ndarray) -> np.ndarray:
    """Estimate a normalised depth map (0 = far background, 1 = near subject).

    Strategy: detect a near-uniform background colour from the image corners,
    build a foreground mask of everything that differs from it, clean the mask
    and turn it into a rounded depth bump using a distance transform so the
    subject reads as a solid object sitting in front of the backdrop. If no
    clear background is found we fall back to brightness/centre cues.
    """
    h, w, _ = rgb.shape
    img = rgb.astype(np.float32)

    # Sample the four corners to guess the background colour.
    cs = max(4, min(h, w) // 20)
    corners = np.concatenate(
        [
            img[:cs, :cs].reshape(-1, 3),
            img[:cs, -cs:].reshape(-1, 3),
            img[-cs:, :cs].reshape(-1, 3),
            img[-cs:, -cs:].reshape(-1, 3),
        ]
    )
    bg_color = np.median(corners, axis=0)
    bg_std = corners.std(axis=0).mean()

    # Distance of every pixel from the background colour.
    dist = np.linalg.norm(img - bg_color, axis=2)

    # If the corners are reasonably uniform we trust the segmentation path.
    uniform_bg = bg_std < 25
    thr = max(28.0, float(np.percentile(dist, 60)) * 0.5)
    mask = dist > thr

    if uniform_bg and mask.mean() > 0.01:
        # Clean up the foreground mask.
        mask = ndimage.binary_opening(mask, iterations=2)
        mask = ndimage.binary_closing(mask, iterations=4)
        mask = ndimage.binary_fill_holes(mask)
        # Keep only the largest connected component (the main subject).
        labels, n = ndimage.label(mask)
        if n > 1:
            sizes = ndimage.sum(np.ones_like(labels), labels, range(1, n + 1))
            mask = labels == (int(np.argmax(sizes)) + 1)

        # Rounded depth: pixels deep inside the subject sit closer than edges,
        # giving the object volume instead of a flat cut-out.
        edt = ndimage.distance_transform_edt(mask)
        if edt.max() > 0:
            roundness = np.sqrt(edt / edt.max())
        else:
            roundness = np.zeros_like(edt)
        depth = np.where(mask, 0.45 + 0.55 * roundness, 0.0)
    else:
        # Fallback: brighter + more central pixels read as closer.
        gray = img.mean(axis=2) / 255.0
        yy, xx = np.mgrid[0:h, 0:w]
        cy, cx = (h - 1) / 2.0, (w - 1) / 2.0
        radial = 1.0 - np.sqrt(((yy - cy) / cy) ** 2 + ((xx - cx) / cx) ** 2) / np.sqrt(2)
        depth = 0.6 * gray + 0.4 * np.clip(radial, 0, 1)

    # Smooth so displacement transitions are gradual, then normalise.
    depth = ndimage.gaussian_filter(depth, sigma=max(1.0, min(h, w) / 300.0))
    depth -= depth.min()
    if depth.max() > 0:
        depth /= depth.max()
    return depth


def synthesize_view(rgb: np.ndarray, depth: np.ndarray, shift: float) -> np.ndarray:
    """Render a new viewpoint by horizontally displacing pixels by depth.

    A positive ``shift`` moves the virtual camera to one side. Nearer pixels
    (higher depth) move more than far ones, which is what produces parallax.
    Uses forward warping with a painter's algorithm (far drawn first, near last)
    and horizontal hole-filling for the small gaps that disocclusion opens up.
    """
    h, w, _ = rgb.shape
    xs = np.arange(w)[None, :].repeat(h, axis=0)
    # Centre the displacement so the mid-depth plane stays put.
    disp = shift * (depth - 0.5)
    dst_x = np.round(xs + disp).astype(np.int64)

    valid = (dst_x >= 0) & (dst_x < w)
    ys = np.arange(h)[:, None].repeat(w, axis=1)

    flat_depth = depth[valid]
    order = np.argsort(flat_depth, kind="stable")  # far -> near

    out = np.zeros_like(rgb)
    filled = np.zeros((h, w), dtype=bool)

    dy = ys[valid][order]
    dx = dst_x[valid][order]
    sy = ys[valid][order]
    sx = xs[valid][order]
    out[dy, dx] = rgb[sy, sx]
    filled[dy, dx] = True

    # Fill disocclusion holes by carrying the nearest filled pixel along rows.
    out = _fill_holes_horizontal(out, filled)
    return out


def _fill_holes_horizontal(img: np.ndarray, filled: np.ndarray) -> np.ndarray:
    """Fill unfilled pixels using the nearest filled neighbour in the same row."""
    h, w, _ = img.shape
    out = img.copy()
    # Forward pass: copy previous filled pixel rightwards.
    for x in range(1, w):
        hole = ~filled[:, x]
        out[hole, x] = out[hole, x - 1]
        filled_prev = filled[:, x] | filled[:, x - 1]
        filled[:, x] = filled_prev
    # Backward pass fixes leading holes at the left edge.
    for x in range(w - 2, -1, -1):
        hole = ~filled[:, x]
        out[hole, x] = out[hole, x + 1]
        filled[:, x] = filled[:, x] | filled[:, x + 1]
    return out


def make_anaglyph(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    """Combine a stereo pair into a red/cyan anaglyph."""
    out = np.zeros_like(left)
    out[..., 0] = left[..., 0]      # red channel from the left eye
    out[..., 1] = right[..., 1]     # green from the right eye
    out[..., 2] = right[..., 2]     # blue from the right eye
    return out


def build_outputs(source: str, out_dir: Path, max_shift: float, frames: int, fps: int) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    image = load_image(source)
    rgb = np.asarray(image, dtype=np.uint8)
    depth = estimate_depth(rgb)

    # Save a depth preview.
    depth_img = Image.fromarray((depth * 255).astype(np.uint8))
    depth_img.save(out_dir / "depth_map.png")

    # Stereo pair: shift symmetrically for left and right eyes.
    left = synthesize_view(rgb, depth, +max_shift / 2.0)
    right = synthesize_view(rgb, depth, -max_shift / 2.0)

    Image.fromarray(make_anaglyph(left, right)).save(out_dir / "3d_anaglyph.jpg", quality=95)

    stereo = np.concatenate([left, right], axis=1)
    Image.fromarray(stereo).save(out_dir / "3d_stereo_pair.jpg", quality=95)

    # Wiggle animation: sweep the virtual camera smoothly back and forth.
    # Frames are downscaled and palette-quantised to keep the GIF web-friendly.
    h, w, _ = rgb.shape
    gif_w = min(w, 720)
    gif_size = (gif_w, round(h * gif_w / w))
    phases = np.sin(np.linspace(0, 2 * np.pi, frames, endpoint=False))
    wiggle = [
        Image.fromarray(synthesize_view(rgb, depth, max_shift * p))
        .resize(gif_size, Image.LANCZOS)
        .convert("P", palette=Image.ADAPTIVE, colors=128)
        for p in phases
    ]
    wiggle[0].save(
        out_dir / "3d_wiggle.gif",
        save_all=True,
        append_images=wiggle[1:],
        duration=int(1000 / fps),
        loop=0,
        optimize=True,
    )

    print("Wrote:")
    for name in ("depth_map.png", "3d_anaglyph.jpg", "3d_stereo_pair.jpg", "3d_wiggle.gif"):
        p = out_dir / name
        print(f"  {p}  ({p.stat().st_size} bytes)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a 3D photo from a flat image.")
    parser.add_argument("source", help="Image path or http(s) URL")
    parser.add_argument("--out-dir", default=str(Path(__file__).resolve().parent), help="Output directory")
    parser.add_argument("--max-shift", type=float, default=22.0, help="Max parallax shift in pixels")
    parser.add_argument("--frames", type=int, default=24, help="Number of wiggle frames")
    parser.add_argument("--fps", type=int, default=18, help="Wiggle frames per second")
    args = parser.parse_args(argv)

    build_outputs(args.source, Path(args.out_dir), args.max_shift, args.frames, args.fps)
    return 0


if __name__ == "__main__":
    sys.exit(main())
