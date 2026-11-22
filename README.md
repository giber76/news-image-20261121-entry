[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/giber76/news-image-20261121-entry/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/giber76/news-image-20261121-entry/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# Saturday 21 November 2026 — one front page, 37 stories

A dense newspaper front page summing up Saturday 21 November 2026 in a
single 1024×1024 image: 3 leads, 10 features, 24 more stories, a UTC
strip, a 9-region bar, a world map with numbered pins, confidence tags
on every drawn story, and a date check. Every story was verified against
live reporting before it was drawn — see `STORIES.md` for the source of
each one.

## The image

![Saturday 21 November 2026 front page](entry.png)

## Leads

1. **Iran strikes Bahrain as tankers hit in Hormuz** — Bahrain says a
   civilian plant burned; the IRGC claims hits on US radars; UKMTO
   reports two tankers struck off Khasab.
2. **Drones set Russian cargo ship ablaze off Finland** — Sparta II's
   crew of 16 evacuated; the ship drifted into Finnish waters.
3. **Climate summit runs into Saturday with no deal** — Antalya. The summit
   missed its Friday close; a draft with no mention of fossil fuels splits
   nearly 200 countries.

## How it is made

`draw.py` (Python + Pillow, stdlib only besides PIL) draws the whole page
from the story list in `STORIES.md` — masthead, UTC strip, stat strip,
9-region bar, 13 original illustrations, map, ALSO list, confidence tags
and date check. `main.ts` copies the finished `entry.png` to the output
directory.

```sh
python3 draw.py        # regenerates entry.png (1024x1024, < 1 MiB)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # grader-style run
```
