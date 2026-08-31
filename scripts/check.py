#!/usr/bin/env python3
"""Pre-commit scan for the FLAIRS-40 track site.

Run from the repository root:

    python scripts/check.py

Exit code 0 means clean. Exit code 1 means at least one finding, each
printed as file:line: message. The scan is intentionally strict about
public-facing text:

  * no em-dashes, en-dashes, curly quotes, or ellipsis characters
  * none of the words in BANNED_WORDS (whole-word, case-insensitive)
  * every in-page anchor (href="#id") points to an id that exists
  * every external link uses https
  * a few facts that must never silently disappear from the page

Standard library only, so it runs with any Python 3.8 or later.
"""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

# Files scanned for characters and vocabulary.
TEXT_FILES = ["index.html", "README.md"]

# The HTML file checked for anchors, links, and required facts.
HTML_FILE = "index.html"

BANNED_CHARS = {
    "\u2013": "en dash",
    "\u2014": "em dash",
    "\u2018": "left single curly quote",
    "\u2019": "right single curly quote",
    "\u201c": "left double curly quote",
    "\u201d": "right double curly quote",
    "\u2026": "ellipsis character",
}

# Whole words only. Robotics vocabulary such as "navigation" is not here
# on purpose; keep it that way.
BANNED_WORDS = [
    "robust", "robustness", "robustly",
    "leverage", "leverages", "leveraged", "leveraging",
    "seamless", "seamlessly",
    "delve", "delves", "delved", "delving",
    "harness", "harnesses", "harnessed", "harnessing",
    "moreover", "furthermore", "additionally",
    "cutting-edge", "state-of-the-art",
    "holistic", "synergy", "synergies", "paradigm", "paradigms",
    "transformative", "groundbreaking", "pivotal", "testament", "tapestry",
    "realm", "realms", "embark", "embarks", "embarking",
    "elevate", "elevates", "elevating",
    "streamline", "streamlines", "streamlined", "streamlining",
    "underscore", "underscores", "underscoring",
    "utilize", "utilizes", "utilized", "utilizing",
    "showcase", "showcases", "showcasing",
    "multifaceted", "game-changing",
    "unlock", "unlocks", "unlocking",
    "empower", "empowers", "empowering",
    "foster", "fosters", "fostering",
    "landscape", "landscapes",
]

# Strings that must be present in index.html. If one goes missing, the
# page has lost a fact that authors depend on.
REQUIRED_IN_HTML = [
    "easychair.org/conferences/?conf=flairs40",
    "January 22, 2027",
    "February 1, 2027",
    "May 24-27, 2027",
    "msilaghi@fit.edu",
    "msyed2011@my.fit.edu",
]

WORD_RE = re.compile(
    r"(?<![\w-])(" + "|".join(re.escape(w) for w in BANNED_WORDS) + r")(?![\w-])",
    re.IGNORECASE,
)
ID_RE = re.compile(r'\bid="([^"]+)"')
ANCHOR_RE = re.compile(r'href="#([^"]+)"')
HTTP_RE = re.compile(r'href="http://')


def scan_text(path: pathlib.Path) -> list[str]:
    findings: list[str] = []
    rel = path.relative_to(ROOT)
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        for ch, name in BANNED_CHARS.items():
            count = line.count(ch)
            if count:
                findings.append(f"{rel}:{lineno}: {name} ({count})")
        for match in WORD_RE.finditer(line):
            findings.append(f"{rel}:{lineno}: banned word '{match.group(1)}'")
    return findings


def scan_html(path: pathlib.Path) -> list[str]:
    findings: list[str] = []
    rel = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8")
    ids = set(ID_RE.findall(text))
    for lineno, line in enumerate(text.splitlines(), 1):
        for target in ANCHOR_RE.findall(line):
            if target not in ids:
                findings.append(f"{rel}:{lineno}: anchor #{target} has no matching id")
        if HTTP_RE.search(line):
            findings.append(f"{rel}:{lineno}: link uses http, not https")
    for needle in REQUIRED_IN_HTML:
        if needle not in text:
            findings.append(f"{rel}: required text missing: {needle}")
    return findings


def main() -> int:
    findings: list[str] = []
    lines_scanned = 0
    for name in TEXT_FILES:
        path = ROOT / name
        if not path.exists():
            findings.append(f"{name}: file not found")
            continue
        lines_scanned += len(path.read_text(encoding="utf-8").splitlines())
        findings.extend(scan_text(path))
    html_path = ROOT / HTML_FILE
    if html_path.exists():
        findings.extend(scan_html(html_path))
    if findings:
        for finding in findings:
            print(finding)
        print(f"\n{len(findings)} finding(s) in {lines_scanned} lines. Fix and rerun.")
        return 1
    print(f"OK: {lines_scanned} lines scanned across {len(TEXT_FILES)} files, no findings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
