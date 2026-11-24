# vibin: notes for Claude working on this repo

This repo is the vibin’ website: a beginner's guide to coding with Claude, for scientists. (To lead a person through the guide, read `VIBIN.md` instead.)

- **The website is this repo on GitHub Pages**, from `main`, root: https://linglab.org/vibin/. One page, `index.html`, with `site/site.css` and `site/site.js`. No build step, no libraries. `.nojekyll` is there so `VIBIN.md` is served as plain text: keep it.
- **Three things say the same route and must stay in step:** `index.html` (for people), `VIBIN.md` (for a reader's Claude), and `kit/` (the files both point at). A change to a step goes into all three in the same commit.
- **Two files are generated.** After any change to `index.html`, `VIBIN.md` or `kit/`, run `python3 tools/make_kit.py` and commit `kit/PROMPTS.md` and `vibin-kit.zip` with it. Prompts are picked up from elements with a `data-title`.
- **Test the kit before pushing:** unzip `vibin-kit.zip` somewhere, run `make_toy_data.py`, `analyze_subject.py` on each subject, then `summarize.py`. `bash -n` the `.qsub` and `.sh` files. People download these and run them on a cluster: `main` must always work.
- **Readers are beginners.** Plain, short, present tense. One new word at a time, each with an everyday comparison. No step may assume something an earlier step didn't give them. Other people's names stay off the page.
- **Don't state SCC or Claude product details from memory.** Check BU's Research Computing pages and https://code.claude.com/docs before changing install commands, menu names, hostnames or scheduler options.
- Look: megaZINE's family, its own pair. Grape and highlighter lime on warm paper, Big Shoulders Display capitals, Courier Prime labels. Keep text on lime dark in both themes.
