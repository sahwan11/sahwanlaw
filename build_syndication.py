#!/usr/bin/env python3
"""
Regenerate sitemap.xml and feed.xml from the article cards in knowledge.html.

The knowledge.html page is the canonical list of published content on the
site. Each article card carries data-lang, data-type, data-tag, and
data-date attributes, plus an href, a category pill, a headline, and a
summary — everything needed to build a sitemap entry and an Atom entry.

Running this script after adding a new card (or editing an existing one)
keeps sitemap.xml and feed.xml in sync without hand-maintenance drift.

Usage:
    python build_syndication.py

Writes (overwrites):
    sitemap.xml
    feed.xml

Non-article URLs that belong in sitemap.xml but are not articles
(homepage, ar/, knowledge.html, lawyer profile, practice-areas landing)
are carried in the STATIC_URLS list below — edit there if the site
structure changes.

The script is intentionally dependency-free (stdlib only) so it can run
on any machine with a Python 3.8+ interpreter. No Jinja, no lxml, no
externals.
"""

from __future__ import annotations

import html
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE_URL = "https://www.sahwanlaw.com"
KNOWLEDGE = ROOT / "knowledge.html"
SITEMAP_OUT = ROOT / "sitemap.xml"
FEED_OUT = ROOT / "feed.xml"

# ---------------------------------------------------------------------------
# Static (non-article) URLs that should be in sitemap.xml
# Edit this list when site structure changes.
# ---------------------------------------------------------------------------
STATIC_URLS: list[tuple[str, str, str, str]] = [
    # (loc_path, lastmod, changefreq, priority)
    ("/",                            "",         "weekly",  "1.0"),
    ("/ar/",                         "",         "weekly",  "0.9"),
    ("/knowledge.html",              "",         "weekly",  "0.8"),
    ("/lawyer/abdulla-sahwan/",      "2025-01-24", "monthly", "0.8"),
    ("/ar/blog/",                    "",         "weekly",  "0.8"),
]


# ---------------------------------------------------------------------------
# Card extraction
# ---------------------------------------------------------------------------
CARD_OPEN = re.compile(
    r'<a\s+href="([^"]+)"[^>]*class="article-card[^"]*"'
    r'[^>]*data-lang="(en|ar)"'
    r'[^>]*data-type="([a-z]+)"'
    r'[^>]*data-tag="([a-z]+)"'
    r'[^>]*data-date="(\d{4}-\d{2}-\d{2})"',
    re.DOTALL,
)
H2_RE = re.compile(
    r'<h2[^>]*class="font-serif text-xl[^"]*"[^>]*>(.*?)</h2>',
    re.DOTALL,
)
PARA_RE = re.compile(
    r'<p[^>]*class="text-navy/50 text-sm font-light[^"]*"[^>]*>(.*?)</p>',
    re.DOTALL,
)


def strip_tags(s: str) -> str:
    """Strip HTML tags and collapse whitespace."""
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    return " ".join(s.split())


def extract_cards(html_text: str) -> list[dict]:
    """
    Walk the HTML and return one dict per article card, in document order.

    We split on the opening <a ... class="article-card" ...> anchor and then
    look inside each slice for the headline (h2) and summary (p) that belong
    to that card.
    """
    cards: list[dict] = []
    matches = list(CARD_OPEN.finditer(html_text))
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(html_text)
        slice_ = html_text[start:end]
        h2 = H2_RE.search(slice_)
        para = PARA_RE.search(slice_)
        cards.append({
            "href": m.group(1),
            "lang": m.group(2),
            "type": m.group(3),
            "tag": m.group(4),
            "date": m.group(5),
            "title": strip_tags(h2.group(1)) if h2 else "",
            "summary": strip_tags(para.group(1)) if para else "",
        })
    return cards


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def to_abs_url(href: str) -> str:
    """Resolve a card href (relative) to an absolute URL."""
    if href.startswith("http"):
        return href
    if href.startswith("/"):
        return BASE_URL + href
    return f"{BASE_URL}/{href}"


def xml_escape(s: str) -> str:
    """XML-safe escape for text content (NOT CDATA)."""
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace('"', "&quot;")
    )


# ---------------------------------------------------------------------------
# sitemap.xml
# ---------------------------------------------------------------------------
def write_sitemap(cards: list[dict]) -> None:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']

    # Static URLs
    for path, lastmod, cf, prio in STATIC_URLS:
        lines.append("  <url>")
        lines.append(f"    <loc>{BASE_URL}{path}</loc>")
        lines.append(f"    <lastmod>{lastmod or today}</lastmod>")
        lines.append(f"    <changefreq>{cf}</changefreq>")
        lines.append(f"    <priority>{prio}</priority>")
        lines.append("  </url>")

    # Article URLs (from knowledge.html)
    for c in cards:
        loc = to_abs_url(c["href"])
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        lines.append(f"    <lastmod>{c['date']}</lastmod>")
        lines.append(f"    <changefreq>monthly</changefreq>")
        # Pillar guides (type=guide) are higher-priority landing pages;
        # individual articles/updates are a notch lower.
        priority = "0.8" if c["type"] == "guide" else "0.7"
        # Newest article bumped to 0.8.
        if c["date"] == max(x["date"] for x in cards):
            priority = "0.8"
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")

    lines.append("</urlset>")
    SITEMAP_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {SITEMAP_OUT.name}: {len(STATIC_URLS)} static + {len(cards)} articles")


# ---------------------------------------------------------------------------
# feed.xml (Atom 1.0)
# ---------------------------------------------------------------------------
def write_feed(cards: list[dict]) -> None:
    # Sort by date desc
    cards_sorted = sorted(cards, key=lambda c: c["date"], reverse=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    out: list[str] = []
    out.append('<?xml version="1.0" encoding="utf-8"?>')
    out.append('<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en">')
    out.append("  <title>Sahwan Law — Legal Knowledge</title>")
    out.append("  <subtitle>Commercial, corporate, and regulatory legal insights from Bahrain since 1975.</subtitle>")
    out.append(f'  <link href="{BASE_URL}/feed.xml" rel="self" type="application/atom+xml"/>')
    out.append(f'  <link href="{BASE_URL}/knowledge.html" rel="alternate" type="text/html"/>')
    out.append(f"  <id>{BASE_URL}/</id>")
    out.append(f"  <updated>{now}</updated>")
    out.append(f'  <icon>{BASE_URL}/images/favicon-32x32.png</icon>')
    out.append(f'  <logo>{BASE_URL}/images/logo.png</logo>')
    out.append("  <rights>© 2026 Salman A. Sahwan Attorneys &amp; Legal Consultants. All rights reserved.</rights>")
    out.append(f'  <generator uri="{BASE_URL}">Sahwan Law Publishing</generator>')
    out.append("  <author>")
    out.append("    <name>Sahwan Law</name>")
    out.append(f"    <uri>{BASE_URL}</uri>")
    out.append("    <email>info@sahwanlaw.com</email>")
    out.append("  </author>")
    out.append("")

    for c in cards_sorted:
        loc = to_abs_url(c["href"])
        date = c["date"]
        iso = f"{date}T00:00:00Z"
        entry_author = "عبدالله سهوان" if c["lang"] == "ar" else "Abdulla Sahwan"
        # Firm-authored pillar guides use the firm name on the AR side.
        if c["lang"] == "ar" and c["type"] == "guide":
            entry_author = "مكتب سهوان للمحاماة"
        out.append(f'  <entry xml:lang="{c["lang"]}">')
        out.append(f"    <title>{xml_escape(c['title'])}</title>")
        out.append(f'    <link href="{loc}" rel="alternate" type="text/html"/>')
        out.append(f"    <id>{loc}</id>")
        out.append(f"    <updated>{iso}</updated>")
        out.append(f"    <published>{iso}</published>")
        out.append(f"    <author><name>{xml_escape(entry_author)}</name></author>")
        out.append(f'    <category term="{c["tag"]}"/>')
        out.append(f'    <category term="{c["type"]}"/>')
        out.append(f'    <summary type="text">{xml_escape(c["summary"])}</summary>')
        out.append("  </entry>")
        out.append("")

    out.append("</feed>")
    FEED_OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Wrote {FEED_OUT.name}: {len(cards_sorted)} entries")


# ---------------------------------------------------------------------------
def main() -> None:
    html_text = KNOWLEDGE.read_text(encoding="utf-8")
    cards = extract_cards(html_text)
    if not cards:
        raise SystemExit("ERROR: no article cards found in knowledge.html — regex may be out of date")
    print(f"Extracted {len(cards)} cards from {KNOWLEDGE.name}")
    write_sitemap(cards)
    write_feed(cards)
    print("Done.")


if __name__ == "__main__":
    main()
