#!/usr/bin/env python3
"""Re-encode site images to WebP at display-appropriate sizes.
Run from repo root: python3 tools/optimize-images.py
Source PNGs are removed once their .webp twin exists (favicons/og keep PNG).
"""
import os, sys
from PIL import Image

# (dir, target_width, quality, keep_alpha)
JOBS = [
    ("BrandLogo/*.png", 96, 82, False),
    ("images-testimoni/*.png", 640, 80, False),
    ("img-logo/KW-icon.png", 128, 88, True),
    ("img-logo/KW-3D.png", 160, 88, True),
]
OG_KEEP = {"img-logo/kwtumbnail.png", "img-logo/KW-appicon.png", "img-logo/KW-icon.png"}


def convert(path, width, quality, keep_alpha):
    im = Image.open(path)
    if im.width > width:
        h = round(im.height * width / im.width)
        im = im.resize((width, h), Image.Resampling.LANCZOS)
    out = os.path.splitext(path)[0] + ".webp"
    if keep_alpha and (im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)):
        im = im.convert("RGBA")
    else:
        im = im.convert("RGB")
    im.save(out, "WEBP", quality=quality, method=6)
    return out


def main():
    import glob
    total_before = total_after = 0
    for pattern, width, quality, alpha in JOBS:
        for path in sorted(glob.glob(pattern)):
            before = os.path.getsize(path)
            out = convert(path, width, quality, alpha)
            after = os.path.getsize(out)
            total_before += before
            total_after += after
            if path not in OG_KEEP:
                os.remove(path)
    print(f"converted: {total_before/1048576:.1f}MB -> {total_after/1048576:.1f}MB")


if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    main()
