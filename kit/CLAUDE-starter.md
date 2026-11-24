# Ground rules for Claude in this folder

<!-- Claude reads a file called CLAUDE.md every time it starts in a folder.
     Save this as CLAUDE.md in your project folder and fill in the blanks
     (or ask Claude to fill them in with you). Keep it short. -->

## Who I am and how to work with me
- I'm a scientist, new to coding this way. Explain in plain words. One new term at a time, one sentence each.
- Do the typing yourself. Only hand me a command when it needs my password, a Duo approval or a browser sign-in.
- For anything bigger than a small change, tell me the plan in a few lines and wait for my OK.
- When something is finished, show me the result (the figure, the page, the numbers), not only a report that it worked.

## This project
- What it is: FILL IN (one or two sentences)
- Language: Python unless I say otherwise.
- Analyses are scripts in this folder, never one-off commands, so every figure can be made again.
- Figures go in `figures/`, tables in `results/`, notes in `notes/`.

## Git
- Save a checkpoint (commit) after each piece of work that runs, with a plain-words message.
- Ask before pushing to GitHub. Never put data, passwords or tokens in the repo.

## BU SCC
- I log in myself. Before any SCC command run `ssh -O check scc`. If it isn't open, stop and ask me to run `bash scc-door.sh open`. Never type my password, and never trigger or approve Duo.
- Login name: FILL IN. SCC project: FILL IN. Project space: `/projectnb/FILL_IN` (FILL IN what lives where).
- Reach it with `ssh scc '<command>'`. Copy with `rsync -av`.
- Looking is free: `ls`, `du`, `head`, `qstat`, reading logs. Ask me before you submit jobs (`qsub`), and before you delete, move or overwrite anything there.
- The login node is for light work only. Anything that computes for more than a minute goes through `qsub`.
- Test on one subject first. Show me its output. Only then run everyone, as an array job.
- Heavy data stays on the SCC. Bring back only small things: tables, figures, logs.

## Data
- Original data is read-only. Write outputs somewhere new.
- Nothing that could identify a participant (names, birth dates, raw headers, consent forms) gets read, copied to this computer, or pasted into chat.
- If a number surprises you, say so. Don't smooth it over.
