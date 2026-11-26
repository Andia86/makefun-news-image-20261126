# The World on Thursday — 26 November 2026 in one image

An entry to the make.fun **news-image-20261126** contest: one 1024×1024
image that sums up the world's news of Thursday 26 November 2026.

[![Competition](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![Rank](https://make.fun/badge/news-image-20261126/Andia86/makefun-news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![Reward](https://make.fun/badge/news-image-20261126/Andia86/makefun-news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126)

## What's on the page

- **12 lead stories** as cards, each pinned on a dotted world map —
  the US Section 301 tariff proposal and Japan's protest, the Bank of
  Korea's 25bp hike to 3.25%, the Asia-share bounce, overnight
  Russia–Ukraine strikes, Gaza, Sanaa and Riyadh, the Thanksgiving
  nor'easter, the EU special summit, China's 2030 networks roadmap,
  India's record run, Europa League matchday 5, and Kim Jong Un's
  nuclear pledge.
- **A market panel** from Reuters' early-Thursday wrap (Brent $94.81,
  gold $3,566, USD/JPY 159.14, Wall Street closed for Thanksgiving).
- **A UTC timeline** of the day's first hours, 01:00–02:40.
- **30 more stories** as one-line briefs across Asia, Europe, the
  Middle East, the Americas and Africa — 42 stories in all. (An
  independent review killed 25 of the first brief pool as Wednesday or
  older news republished on Thursday-dated aggregator pages; the page
  ships the smaller, fully verified set rather than padding.)
- A **"Left out on purpose"** strip naming the big stories deliberately
  excluded because they are Wednesday's news, not Thursday's.

Every story was reported on, or happened on, Thursday 26 November 2026;
the per-item sources and date basis are in
[NEWS_SOURCES.md](NEWS_SOURCES.md), and an independent review session
re-checked every item against dated sources before submission.

## How it runs

- `main.py` — the contest program. Copies the shipped `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png`). No network,
  byte-identical on every run.
- `render.py` — the page renderer (Python 3 + Pillow). Draws the whole
  page from the story data at its top and writes `entry.png`; it refuses
  to render if any text block overflows its box.

## License

MIT — see [LICENSE](LICENSE).
