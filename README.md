# vibin’

You describe it. Claude types it. A step-by-step way into coding with Claude, for scientists who have never done it.

**The site: https://linglab.org/vibin/**

The route: set up → a first demo → the loop → save points (git) → put it online (GitHub Pages) → your own data → the SCC door → a first job → a whole analysis on practice data → your own question.

## Two ways to use it

- **Read the site** and paste the prompts into Claude as you go.
- **Hand it to your Claude.** Open Claude Code in an empty folder and say:

  > Read https://linglab.org/vibin/VIBIN.md and be my guide through it. I’m new to this. Start at step 2, go one step at a time, and wait for me before moving on.

## What’s here

| | |
|-|-|
| `index.html`, `site/` | The website |
| `VIBIN.md` | The whole guide, written for Claude to read and lead someone through |
| `kit/` | Everything the steps use: prompts, ground rules for Claude, the SSH door, job scripts, a practice analysis |
| `vibin-kit.zip` | The kit in one download (generated) |
| `tools/make_kit.py` | Rebuilds `kit/PROMPTS.md` and the zip |

The practice analysis runs anywhere with Python and numpy:

```
python3 make_toy_data.py
python3 analyze_subject.py data/sub-01.csv results/
python3 summarize.py results/ figures/
```

Free to copy, change and pass on.
