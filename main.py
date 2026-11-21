#!/usr/bin/env python3
"""news-image-20261121 round-2 entrypoint (stdlib only).

Copies the pre-rendered entry.png next to this file into the grader's
output directory and verifies the copy byte for byte. No third-party
packages, no network, no fonts, no image libraries: the PNG bytes are
already final, this program only moves them.
"""
import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "71211c55987ad33f28a7cf88bdb250e4494b429faf4f25594936bb0ee9c42f44"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
NAME = "entry.png"


def here():
    root = os.environ.get("MAKEFUN_BOT_DIR")
    if root:
        return root
    return os.path.dirname(os.path.abspath(__file__))


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    src = os.path.join(here(), NAME)
    if not os.path.isfile(src):
        print("missing " + NAME + " next to main.py", file=sys.stderr)
        return 1
    with open(src, "rb") as f:
        head = f.read(len(PNG_SIGNATURE))
    if head != PNG_SIGNATURE:
        print(NAME + " is not a PNG", file=sys.stderr)
        return 1
    digest = sha256_of(src)
    if digest != EXPECTED_SHA256:
        print(NAME + " sha256 mismatch", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, NAME)
    shutil.copyfile(src, dst)
    if sha256_of(dst) != EXPECTED_SHA256:
        print("copy sha256 mismatch", file=sys.stderr)
        return 1
    if os.path.getsize(dst) != os.path.getsize(src):
        print("copy size mismatch", file=sys.stderr)
        return 1
    if os.path.getsize(dst) == 0:
        print("copy is empty", file=sys.stderr)
        return 1
    print("wrote " + dst + " (" + str(os.path.getsize(dst)) + " bytes, sha256 "
          + EXPECTED_SHA256[:16] + ")")
    return 0


if __name__ == "__main__":
    sys.exit(main())
