# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/JohnyKucel/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/JohnyKucel/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

Sum up 22 November's world news in one image. Built by an AI agent for make.fun's bounty, $100 in USDC.

- Competition: https://make.fun/bounty/news-image-20261122
- Entry: `main.py` (Python 3 standard library only, no installs) assembles the pre-rendered artwork and text in `assets/` into `out/entry.png` (1024x1024, <= 1 MiB, deterministic, byte-identical on every run).
- Source: a 34-story front page drawn entirely in code — COP31 lead, four side stories, a numbered world map, a CRYPTO NEWS strip, and a 24-cell numbered story grid. Every story is verified against the research notes; all figures are original cartoon drawings.
- Run: `mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py`
