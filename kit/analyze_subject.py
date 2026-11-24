#!/usr/bin/env python3
"""Fit a contrast response function to ONE subject, once per condition.

    python analyze_subject.py data/sub-01.csv results/

Reads a CSV with the columns: subject, condition, contrast, trial, response.
Writes results/sub-01.json with the fitted parameters for each condition.

One subject per run is the shape the cluster likes: the same script, run many
times side by side, one task per subject (see analysis.qsub).

Needs only numpy. The fit tries a grid of (c50, n) pairs and, for each pair,
solves for baseline and rmax exactly (they are linear), then keeps the best.
"""
import csv
import json
import os
import sys

import numpy as np

C50_GRID = np.exp(np.linspace(np.log(0.02), np.log(1.0), 120))
N_GRID = np.linspace(0.8, 5.0, 85)


def fit_crf(contrast, response):
    """Least-squares Naka-Rushton fit. Returns a dict of parameters and r2."""
    c = np.asarray(contrast, dtype=float)
    y = np.asarray(response, dtype=float)
    best = None
    for n in N_GRID:
        cn = c**n
        for c50 in C50_GRID:
            shape = cn / (cn + c50**n)
            design = np.column_stack([np.ones_like(shape), shape])
            coef, *_ = np.linalg.lstsq(design, y, rcond=None)
            sse = float(np.sum((design @ coef - y) ** 2))
            if best is None or sse < best[0]:
                best = (sse, coef[0], coef[1], c50, n)
    sse, base, rmax, c50, n = best
    sst = float(np.sum((y - y.mean()) ** 2))
    return {"base": float(base), "rmax": float(rmax), "c50": float(c50),
            "n": float(n), "r2": 1 - sse / sst if sst > 0 else float("nan")}


def main():
    if len(sys.argv) < 3:
        sys.exit("usage: python analyze_subject.py data/sub-01.csv results/")
    path, outdir = sys.argv[1], sys.argv[2]
    rows = list(csv.DictReader(open(path, newline="")))
    if not rows:
        sys.exit(f"{path} has no rows")
    subject = rows[0]["subject"]
    out = {"subject": subject, "source": path, "n_trials": len(rows), "conditions": {}}
    for cond in sorted({r["condition"] for r in rows}):
        sel = [r for r in rows if r["condition"] == cond]
        c = np.array([float(r["contrast"]) for r in sel])
        y = np.array([float(r["response"]) for r in sel])
        fit = fit_crf(c, y)
        levels = sorted(set(c.tolist()))
        fit["contrasts"] = levels
        fit["mean_response"] = [float(y[c == lv].mean()) for lv in levels]
        fit["n_trials"] = len(sel)
        out["conditions"][cond] = fit
        print(f"{subject} {cond:11s} c50={fit['c50']:.3f} rmax={fit['rmax']:.2f} "
              f"n={fit['n']:.2f} base={fit['base']:.2f} r2={fit['r2']:.3f} ({len(sel)} trials)")
    os.makedirs(outdir, exist_ok=True)
    dest = os.path.join(outdir, subject + ".json")
    with open(dest, "w") as f:
        json.dump(out, f, indent=2)
    print("wrote", dest)


if __name__ == "__main__":
    main()
