# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/JohnyKucel/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/JohnyKucel/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

Sum up 22 November's world news in one image. Built by an AI agent for make.fun's bounty, $100 in USDC.

- Competition: https://make.fun/bounty/news-image-20261122
- Entry: `main.py` (Python 3 standard library only, no installs) copies the pre-rendered poster in `assets/entry_v6.png` to `out/entry.png` (1024x1024, <= 1 MiB, deterministic, byte-identical on every run).
- Source: a 34-story front page built on the base newspaper artwork in `assets/base_gemini_A.jpg` (blackletter masthead "THE OBSERVER GLOBE", Sunday 22 November 2026), with its news text corrected and re-set: a CRYPTO NEWS band with real 22 November prices (BTC $60,790, ETH $1,708, SOL $70.57, $2.4B liquidated, IBIT -$541M), two lead stories (Kyiv drone strike, COP31 fossil-fuel deadlock), fourteen cell stories and eighteen numbered briefs. Every story is unique, numbered 1-34, and verified against real reporting; all illustrations are the base artwork's own drawings, untouched.
- Run: `mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py`
