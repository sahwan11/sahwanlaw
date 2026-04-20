"""
test_parse_smoke.py
-------------------
Smoke test for parse_articles.py after folding in the 5 parse_phase2
improvements (2026-04-20). Opens 3 representative files from the
bahrain-laws/verify/ directory and parses them via the canonical script's
public functions. Prints per-file article count + first 3 article numbers.

Expected (from the Phase 2 agent's reported numbers):
    L1496_AR.docx  ~145 articles (standard numbering baseline)
    L0372_AR.docx  ~34  articles (schedule items captured post-patch)
    K3210.html     ~14  articles (HTML whitespace collapse + ordinal words)
"""
from __future__ import annotations

from pathlib import Path

# Reuse the canonical parser's public surface — no re-implementation here.
from parse_articles import (
    extract_docx,
    extract_html,
    parse_slug,
)

VERIFY = Path(r"C:\Users\sahwa\Documents\projects\bahrain-laws\verify")

# (slug, filename, lang, expected_count_approx)
CASES = [
    ("L1496", "L1496_AR.docx", "ar", 145),
    ("L0372", "L0372_AR.docx", "ar", 34),
    ("K3210", "K3210.html",   "ar", 14),
]


def parse_one(slug: str, fname: str, lang: str) -> tuple[int, list[str]]:
    path = VERIFY / fname
    if not path.exists():
        raise FileNotFoundError(path)
    if path.suffix.lower() == ".docx":
        body = extract_docx(path)
    else:
        body = extract_html(path)

    ar_text = body if lang == "ar" else None
    en_text = body if lang == "en" else None
    articles, _notes = parse_slug(slug, ar_text, en_text)
    nums = [a["article_number"] for a in articles[:3]]
    return len(articles), nums


def main() -> None:
    print(f"{'SLUG':<8} {'FILE':<20} {'COUNT':>6} {'EXPECTED':>9}   FIRST 3")
    print("-" * 78)
    all_ok = True
    for slug, fname, lang, expected in CASES:
        try:
            count, firsts = parse_one(slug, fname, lang)
        except Exception as exc:
            print(f"  {slug}  ERROR: {exc}")
            all_ok = False
            continue
        ok = abs(count - expected) <= max(3, expected // 10)  # ±10% or 3
        flag = "OK" if ok else "MISS"
        if not ok:
            all_ok = False
        print(f"{slug:<8} {fname:<20} {count:>6} {expected:>9}   {firsts}  [{flag}]")
    print("-" * 78)
    print("ALL OK" if all_ok else "one or more cases missed expected count")


if __name__ == "__main__":
    main()
