#!/usr/bin/env python3
"""Make a small practice dataset, so you can rehearse the whole pipeline
before touching real data.

It invents 8 subjects. Each one saw a grating at 7 contrasts, either attended
or unattended, 20 trials per cell. The "response" follows a contrast response
function (Naka-Rushton) plus noise. Attention shifts the curve left (a lower
c50) and lifts it a little.

Because the data are made up, the true answer is known. It is saved in
data/truth.json, and summarize.py checks the fits against it.

    python make_toy_data.py            # writes data/sub-01.csv ... sub-08.csv
    python make_toy_data.py 12 mydata  # 12 subjects, into mydata/
"""
import csv
import json
import os
import sys

import numpy as np

N_SUBJECTS = int(sys.argv[1]) if len(sys.argv) > 1 else 8
OUT = sys.argv[2] if len(sys.argv) > 2 else "data"
CONTRASTS = [0.03, 0.06, 0.12, 0.25, 0.5, 0.75, 1.0]
TRIALS = 20
NOISE = 0.25


def crf(c, base, rmax, c50, n):
    """Naka-Rushton: response as a function of contrast."""
    c = np.asarray(c, dtype=float)
    return base + rmax * c**n / (c**n + c50**n)


def main():
    rng = np.random.default_rng(2026)  # fixed seed: same data every time
    os.makedirs(OUT, exist_ok=True)
    truth = {}
    for s in range(1, N_SUBJECTS + 1):
        name = f"sub-{s:02d}"
        base = rng.normal(0.2, 0.05)
        rmax = rng.normal(2.0, 0.25)
        c50 = float(np.exp(rng.normal(np.log(0.25), 0.15)))
        n = rng.normal(2.0, 0.15)
        params = {
            "unattended": dict(base=base, rmax=rmax, c50=c50, n=n),
            # attention: curve moves left by about 30 percent, and up by about 10
            "attended": dict(base=base, rmax=rmax * rng.normal(1.10, 0.03),
                             c50=c50 * rng.normal(0.70, 0.05), n=n),
        }
        truth[name] = params
        with open(os.path.join(OUT, name + ".csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["subject", "condition", "contrast", "trial", "response"])
            for cond, p in params.items():
                for c in CONTRASTS:
                    r = crf(c, **p) + rng.normal(0, NOISE, TRIALS)
                    for t, value in enumerate(r, start=1):
                        w.writerow([name, cond, c, t, f"{value:.4f}"])
    with open(os.path.join(OUT, "truth.json"), "w") as f:
        json.dump(truth, f, indent=2)
    print(f"Wrote {N_SUBJECTS} subjects to {OUT}/ (and the true parameters to {OUT}/truth.json)")


if __name__ == "__main__":
    main()
