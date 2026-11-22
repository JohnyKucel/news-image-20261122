"""The World in One Day -- Sunday 22 November 2026 (v6).

Entry for make.fun news-image-20261122. The front page is the base
newspaper artwork in assets/base_gemini_A.jpg with its news text
corrected and re-set into the pre-rendered poster in
assets/entry_v6.png. This program uses only the Python standard
library: it writes that poster to the output path unchanged, so
repeated runs produce an identical file.
"""

import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
POSTER = os.path.join(HERE, "assets", "entry_v6.png")


def output_path():
    dest = os.environ.get("MAKEFUN_OUTPUT_DIR", os.path.join(HERE, "out"))
    return os.path.join(dest, "entry.png")


def digest_of(path):
    total = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(65536)
            if not chunk:
                break
            total.update(chunk)
    return total.hexdigest()


def main():
    if not os.path.isfile(POSTER):
        raise SystemExit("missing pre-rendered poster: " + POSTER)
    target = output_path()
    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copyfile(POSTER, target)
    wanted = digest_of(POSTER)
    got = digest_of(target)
    if wanted != got:
        raise SystemExit("copy mismatch: " + target)
    print("wrote", target, os.path.getsize(target), "bytes", got)


if __name__ == "__main__":
    main()
