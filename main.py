#!/usr/bin/env python3
"""Entrypoint for the news-image-20261125 entry (Python 3.13, stdlib only).

The graded run has no network and no image library installed, so this
program does no rendering at all: it copies the entry.png image that was
drawn at build time by render_news.py and committed to this repository
into the output directory. The copy is byte for byte identical on
every run.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
TARGET = "entry.png"


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, TARGET)
    shutil.copyfile(SOURCE, dest)
    size = os.path.getsize(dest)
    with open(dest, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    with open(SOURCE, "rb") as fh:
        source_digest = hashlib.sha256(fh.read()).hexdigest()
    if digest != source_digest:
        print("error: copied file differs from committed entry.png",
              file=sys.stderr)
        return 1
    print(f"wrote {dest} ({size} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
