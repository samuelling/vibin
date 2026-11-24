#!/usr/bin/env python3
"""Gather every subject's fit into one table and one figure.

    python summarize.py results/ figures/

Reads results/sub-*.json (from analyze_subject.py). Writes:
    results/group_summary.csv   one row per subject and condition
    figures/group_crf.png       the group contrast response functions

Prints the numbers behind the figure, so you can check them by eye.
If data/truth.json exists (practice data), it also reports how close the
fits came to the true values: a known-answer check.
"""
import csv
import glob
import json
import os
import sys

import numpy as np


def crf(c, base, rmax, c50, n):
    c = np.asarray(c, dtype=float)
    return base + rmax * c**n / (c**n + c50**n)


def main():
    resdir = sys.argv[1] if len(sys.argv) > 1 else "results"
    figdir = sys.argv[2] if len(sys.argv) > 2 else "figures"
    files = sorted(glob.glob(os.path.join(resdir, "sub-*.json")))
    if not files:
        sys.exit(f"no sub-*.json files in {resdir}/. Run analyze_subject.py first.")
    subjects = [json.load(open(f)) for f in files]
    conds = sorted({c for s in subjects for c in s["conditions"]})
    print(f"{len(subjects)} subjects, conditions: {', '.join(conds)}\n")

    table = os.path.join(resdir, "group_summary.csv")
    with open(table, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["subject", "condition", "c50", "rmax", "n", "base", "r2", "n_trials"])
        for s in subjects:
            for cond in conds:
                p = s["conditions"].get(cond)
                if p:
                    w.writerow([s["subject"], cond] + [f"{p[k]:.4f}" for k in ("c50", "rmax", "n", "base", "r2")] + [p["n_trials"]])
    print("wrote", table)

    print(f"\n{'condition':12s} {'c50':>14s} {'rmax':>14s} {'r2':>8s}")
    for cond in conds:
        ps = [s["conditions"][cond] for s in subjects if cond in s["conditions"]]
        c50 = np.array([p["c50"] for p in ps]); rmax = np.array([p["rmax"] for p in ps])
        r2 = np.array([p["r2"] for p in ps])
        print(f"{cond:12s} {c50.mean():8.3f} ±{c50.std(ddof=1):.3f} {rmax.mean():8.2f} ±{rmax.std(ddof=1):.2f} {r2.mean():8.3f}")

    # Paired comparison, if there are exactly two conditions in every subject
    both = [s for s in subjects if all(c in s["conditions"] for c in conds)]
    if len(conds) == 2 and len(both) >= 3:
        a, b = conds
        d = np.array([np.log(s["conditions"][a]["c50"]) - np.log(s["conditions"][b]["c50"]) for s in both])
        t = d.mean() / (d.std(ddof=1) / np.sqrt(len(d)))
        print(f"\nc50, {a} relative to {b}: ratio {np.exp(d.mean()):.2f} "
              f"(paired t on log c50 = {t:.2f}, df = {len(d) - 1}, {int((d < 0).sum())} of {len(d)} subjects lower)")

    # Known-answer check against the practice data's true values
    truth_path = os.path.join("data", "truth.json")
    if os.path.exists(truth_path):
        truth = json.load(open(truth_path))
        errs = [abs(np.log(s["conditions"][c]["c50"] / truth[s["subject"]][c]["c50"]))
                for s in subjects if s["subject"] in truth for c in conds if c in truth[s["subject"]]]
        if errs:
            print(f"\nKnown-answer check: fitted c50 is within {100 * (np.exp(np.median(errs)) - 1):.0f}% of the truth "
                  f"for the median fit, {100 * (np.exp(max(errs)) - 1):.0f}% for the worst.")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("\nmatplotlib is not installed, so no figure. The table above is complete.")
        return
    os.makedirs(figdir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(5, 4))
    xs = np.exp(np.linspace(np.log(0.02), 0, 200))
    colors = {"attended": "#5B34D6", "unattended": "#8A8792"}
    for i, cond in enumerate(conds):
        ps = [s["conditions"][cond] for s in subjects if cond in s["conditions"]]
        levels = ps[0]["contrasts"]
        means = np.array([p["mean_response"] for p in ps if p["contrasts"] == levels])
        col = colors.get(cond, f"C{i}")
        curves = np.array([crf(xs, p["base"], p["rmax"], p["c50"], p["n"]) for p in ps])
        ax.plot(xs, curves.mean(0), color=col, lw=2, label=cond)
        sem = means.std(0, ddof=1) / np.sqrt(len(means)) if len(means) > 1 else np.zeros(len(levels))
        ax.errorbar(levels, means.mean(0), yerr=sem, fmt="o", color=col, ms=5, capsize=0)
    ax.set_xscale("log")
    ax.set_xlabel("Contrast")
    ax.set_ylabel("Response (a.u.)")
    ax.set_title(f"Group contrast response, n = {len(subjects)}")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False)
    fig.tight_layout()
    dest = os.path.join(figdir, "group_crf.png")
    fig.savefig(dest, dpi=200)
    print("\nwrote", dest)


if __name__ == "__main__":
    main()
