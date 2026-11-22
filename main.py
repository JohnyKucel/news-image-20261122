"""The World in One Day -- Sunday 22 November 2026 (v3).

Entry for make.fun news-image-20261122. The poster starts from the
base newspaper image (assets/base_gemini.jpg) and the news text on it
was corrected and re-set by the pre-render script (build_v3.py, Pillow)
into assets/entry_v3.png. This program is standard library only: it
copies that pre-rendered poster to the output path, byte for byte, so
every run writes the same file.
"""

import os
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "assets", "entry_v3.png")
OUT = os.path.join(
    os.environ.get("MAKEFUN_OUTPUT_DIR", os.path.join(ROOT, "out")),
    "entry.png",
)


def build():
    if not os.path.isfile(SRC):
        raise SystemExit("missing pre-rendered poster: " + SRC)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    shutil.copyfile(SRC, OUT)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    build()
