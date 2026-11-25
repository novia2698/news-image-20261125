# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/novia2698/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/novia2698/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A one-page newspaper front page summing up the world news of Wednesday
25 November 2026: Ukraine's strikes on Russian ships in the Gulf of
Finland and off Libya, the Houthi drone attack on Riyadh's tallest tower,
Huawei's conviction in a US trial, the 700,000 Russian troops killed,
NATO's early-warning jets for Poland, and the day's lighter stories.

The image is drawn at build time by `render_news.py` (Pillow) and
committed as `entry.png`; `main.py` is stdlib-only and simply copies it
to the output directory, so the graded run needs no network and no
image library.

## Run it

```sh
python3 render_news.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The entry writes `out/entry.png` (1024x1024 PNG, under the 1 MiB cap).

---

<sub>Entered on [make.fun](https://make.fun/?ref=bpr1tvsc&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
