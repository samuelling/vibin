#!/usr/bin/env python3
"""Rebuild the two generated files: kit/PROMPTS.md (every prompt on the page,
in order) and vibin-kit.zip (the kit plus VIBIN.md, unpacking into vibin-kit/).

    python3 tools/make_kit.py

Run it after any change to index.html, VIBIN.md or kit/, and commit the result.
"""
import html
import os
import re
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIT = ["PROMPTS.md", "CLAUDE-starter.md", "first-demo.html", "ssh_config_scc", "scc-door.sh", "hello.qsub",
       "make_toy_data.py", "analyze_subject.py", "analysis.qsub", "summarize.qsub", "summarize.py"]


def prompts():
    page = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    found = re.findall(r'<(pre|li)\b[^>]*data-title="([^"]+)"[^>]*>(.*?)</\1>', page, flags=re.S)
    out, last = [], None
    for _, title, body in found:
        text = html.unescape(re.sub(r"<[^>]+>", "", body)).strip()
        if title != last:
            out.append(f"\n## {html.unescape(title)}\n")
            last = title
        out.append("> " + text.replace("\n", "\n> ") + "\n")
    return out


def main():
    body = ["# vibin’ for dummies (and PIs): every prompt, in order\n",
            "Things to say to Claude, from https://linglab.org/vibin/. Fill in anything in [brackets].",
            "Each block is one message. Send it, look at what comes back, then go on.\n"] + prompts()
    with open(os.path.join(ROOT, "kit", "PROMPTS.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(body))
    dest = os.path.join(ROOT, "vibin-kit.zip")
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
        for name, path in [("VIBIN.md", "VIBIN.md")] + [(k, os.path.join("kit", k)) for k in KIT]:
            info = zipfile.ZipInfo("vibin-kit/" + name, date_time=(2026, 11, 24, 0, 0, 0))  # fixed date: same bytes each run
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o755 if name.endswith((".sh", ".py")) else 0o644) << 16
            z.writestr(info, open(os.path.join(ROOT, path), "rb").read())
    print("wrote kit/PROMPTS.md and vibin-kit.zip")


if __name__ == "__main__":
    main()
