#!/usr/bin/env python3
"""Entry for make.fun news-image-20261118.

Writes the 18 November 2026 world-news summary image to the output
directory. The image itself is entry.png beside this file; this program
copies it, checks it is a whole PNG of at most 1024x1024 pixels and at
most 1 MiB, and writes the same bytes on every run. Standard library only,
no network.
"""
import hashlib
import os
import shutil
import struct
import sys

SOURCE = "entry.png"
MAX_BYTES = 1048576
MAX_SIDE = 1024


def png_size(path):
    with open(path, "rb") as f:
        header = f.read(33)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("entry.png is not a PNG file")
    if header[12:16] != b"IHDR":
        raise ValueError("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SOURCE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    size = os.path.getsize(src)
    if size > MAX_BYTES:
        raise ValueError(f"entry.png is {size} bytes, over the 1 MiB limit")
    width, height = png_size(src)
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError(f"entry.png is {width}x{height}, over 1024x1024")
    shutil.copyfile(src, dst)
    digest = hashlib.sha256(open(dst, "rb").read()).hexdigest()
    print(f"wrote {dst}: {width}x{height}, {size} bytes, sha256 {digest[:16]}...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
