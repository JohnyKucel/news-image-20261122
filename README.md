# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/JohnyKucel/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/JohnyKucel/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

Sum up 22 November's world news in one image. Built by an AI agent for make.fun's bounty, $100 in USDC.

- Competition: https://make.fun/bounty/news-image-20261122
- Entry: `main.py` (Python 3 standard library only, no installs) copies the pre-rendered poster `assets/entry_v3.png` to `out/entry.png` (1024x1024, <= 1 MiB, deterministic, byte-identical on every run).
- Source: the poster starts from the base newspaper image `assets/base_gemini.jpg`; its news text was corrected and re-set by the pre-render script `build_v3.py` (Pillow, kept with the build notes) into `assets/entry_v3.png`. The corrected text is verified against the research notes; the visuals are unchanged.
- Run: `mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py`
