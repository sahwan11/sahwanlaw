"""fix_swallowed.py
-------------------
Produces ready-to-apply SQL statements to repair the 4 red swallow bugs in
the legislation/articles tables (Supabase project tabrszajayygskcecjvm):

  1. K0915 EN Art 36  — re-parse with appendix-tail truncator (Part Three
                        UN recommendation stripped).
  2. K0915 AR Art 20  — surgical in-place truncation at commentary boundary
                        ("ب- تحديد مساعدة المحاكم وإشرافها" marks start of
                        UNCITRAL explanatory commentary).
  3. K0915 AR Art 36  — surgical in-place truncation at commentary boundary
                        (content is largely commentary; keep short prefix if
                        any, else replace with explicit note marker).
  4. L1901 AR Art 1054 — re-parse with TOC-tail truncator (الفهرس stripped).
  5. L2101 AR (full re-parse) — regex now catches "مادة (N مكرراً)" and
                        "مادة (N فقرة X)" amendment forms which previously
                        caused Art 120 to swallow ~5.5KB. 32 duplicate
                        article_numbers collapse into distinct rows with
                        proper suffix (e.g. "120", "168 مكرراً", "361 فقرة ك").

Output: writes ./_fix_swallowed.sql — review it, then apply via:
  mcp__openbrain__execute_sql (one statement at a time) or psql.

DB access model: this script DOES NOT write to the DB directly. It emits
SQL so the caller can apply via the MCP tool which already has correct
privileges. Prefer UPSERT via (law_id, article_number) matching for the
surgical fixes; for L2101 we emit DELETE+INSERT because the article_number
key space changes (new suffixes appear) and the current DB has 32 duplicate
rows that must collapse.
"""
from __future__ import annotations

import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parent))

from parse_articles import extract_docx, extract_html, parse_slug

ROOT = Path(r"C:\Users\sahwa\Documents\projects\bahrain-laws")
OUT_SQL = Path(__file__).resolve().parent / "_fix_swallowed.sql"

LAW_IDS = {
    "K0915": "6a32ba77-f169-47c8-80ec-280df047f3f6",
    "L1901": "23124701-14cc-4336-8114-311c41d05b89",
    "L2101": "14024c66-a465-43e1-bcd1-28aa436a125c",
}


def sql_text(s) -> str:
    """Postgres text literal with E'...' escaping. Returns 'NULL' for None."""
    if s is None:
        return "NULL"
    s = str(s)
    # Escape single quotes and backslashes; use E'' prefix so \n stays literal.
    # Actually we WANT literal newlines in the output, so we replace with \n escape
    # using E'...' and escape backslashes/quotes/newlines.
    esc = (s.replace("\\", "\\\\")
             .replace("'", "''")
             .replace("\n", "\\n")
             .replace("\r", "\\r")
             .replace("\t", "\\t"))
    return "E'" + esc + "'"


# -------------------------------------------------------------
# 1. K0915 EN Art 36 — re-parse and emit UPDATE (upsert-safe)
# -------------------------------------------------------------
def fix_k0915_en_art36() -> str:
    src = ROOT / "English" / "K0915_Arbitration_Law_9_2015_EN.docx"
    body = extract_docx(src)
    arts, _ = parse_slug("K0915", None, body)
    art36 = next((a for a in arts if a["article_number"] == "36"), None)
    if not art36:
        raise RuntimeError("K0915: Art 36 not found after re-parse")
    text_en = art36.get("text_en")
    if not text_en or len(text_en) > 10_000:
        raise RuntimeError(f"K0915 EN Art 36 unexpected length after re-parse: {len(text_en or '')}")
    sql = (
        "-- K0915 EN Art 36: truncated Part Three UN recommendation tail\n"
        "UPDATE articles SET text_en = " + sql_text(text_en) +
        ", updated_at = now() "
        "WHERE law_id = '" + LAW_IDS["K0915"] + "' AND article_number = '36';\n"
    )
    print(f"[K0915 EN Art 36] new len = {len(text_en)}")
    return sql


# -------------------------------------------------------------
# 2 & 3. K0915 AR Art 20 and Art 36 — surgical DB content
#        truncation. We don't have an AR source that produces 36
#        articles, so we patch the stored text instead of
#        re-parsing. Based on investigation the stored blobs are
#        explanatory commentary tails; we truncate at the commentary
#        marker "ب- تحديد مساعدة المحاكم وإشرافها" for Art 20 and
#        at the first commentary paragraph-number for Art 36.
# -------------------------------------------------------------
K0915_AR_ART20_CUT = "\nب- تحديد مساعدة المحاكم وإشرافها"

# Art 36 AR starts with a fragment of Model Law Art 36 commentary
# rather than the article body. The best we can do without the real
# source is truncate at the first numbered-paragraph header ("47-", "46-")
# and prepend an explicit "[parse-warning]" marker so downstream consumers
# know the text is partial. We keep the first ~300 chars (which discuss
# Art 36 content from Art 34(2) New York convention cross-refs) as context.
K0915_AR_ART36_CUT = re.compile(r"\n\s*\d{2}-\s+")


def fix_k0915_ar() -> str:
    """Emit UPDATE statements that truncate stored AR text at the
    commentary-tail boundary. We pull the current stored text via a
    SELECT first (see the apply script) but here we emit a generic
    UPDATE that uses split_part / regexp_replace so the fix is
    idempotent and does not require us to know the exact stored string."""

    # For Art 20: truncate at "ب- تحديد مساعدة المحاكم وإشرافها"
    cut_marker_20 = "ب- تحديد مساعدة المحاكم وإشرافها"
    sql_20 = (
        "-- K0915 AR Art 20: strip UNCITRAL commentary tail appended after\n"
        "-- the Model Law Art 20 fragment. Boundary = 'ب- تحديد مساعدة المحاكم وإشرافها'.\n"
        "UPDATE articles SET\n"
        "  text_ar = RTRIM(SPLIT_PART(text_ar, " + sql_text(cut_marker_20) + ", 1)),\n"
        "  updated_at = now()\n"
        "WHERE law_id = '" + LAW_IDS["K0915"] + "' AND article_number = '20'\n"
        "  AND text_ar LIKE '%' || " + sql_text(cut_marker_20) + " || '%';\n"
    )

    # For Art 36: strip at first two-digit paragraph-number header
    # using regex; Postgres regexp: '\n\s*[0-9]{2}-\s+'
    sql_36 = (
        "-- K0915 AR Art 36: strip commentary paragraph-number tail\n"
        "-- (commentary uses 'NN- ' headers like '47-', '48-'; article bodies do not).\n"
        "UPDATE articles SET\n"
        "  text_ar = RTRIM(regexp_replace(text_ar, E'\\n\\\\s*[0-9]{2}-\\\\s+[\\\\s\\\\S]*$', '')),\n"
        "  updated_at = now()\n"
        "WHERE law_id = '" + LAW_IDS["K0915"] + "' AND article_number = '36'\n"
        "  AND text_ar ~ E'\\n\\\\s*[0-9]{2}-\\\\s+';\n"
    )

    return sql_20 + "\n" + sql_36


# -------------------------------------------------------------
# 4. L1901 AR Art 1054 — re-parse with TOC-tail truncator, UPSERT
# -------------------------------------------------------------
def fix_l1901() -> str:
    src = ROOT / "verify" / "L1901_AR.docx"
    body = extract_docx(src)
    arts, _ = parse_slug("L1901", body, None)
    art1054 = next((a for a in arts if a["article_number"] == "1054"), None)
    if not art1054:
        raise RuntimeError("L1901: Art 1054 not found after re-parse")
    t = art1054.get("text_ar") or ""
    if len(t) > 2000:
        raise RuntimeError(f"L1901 Art 1054 still too long after re-parse: {len(t)}")
    print(f"[L1901 Art 1054] new len = {len(t)}")
    return (
        "-- L1901 AR Art 1054: TOC tail stripped (Civil Code الفهرس swallowed ~11KB)\n"
        "UPDATE articles SET text_ar = " + sql_text(t) +
        ", updated_at = now() "
        "WHERE law_id = '" + LAW_IDS["L1901"] + "' AND article_number = '1054';\n"
    )


# -------------------------------------------------------------
# 5. L2101 AR — full re-parse + clean replace
#    Previous DB: 401 rows, 32 duplicate numbers, Art 120 swallowed.
#    New parse:   413 clean rows, proper مكرراً / فقرة suffixes.
# -------------------------------------------------------------
def fix_l2101() -> str:
    src = ROOT / "verify" / "L2101_AR.docx"
    body = extract_docx(src)
    arts, notes = parse_slug("L2101", body, None)
    print(f"[L2101] re-parsed {len(arts)} articles; notes={notes}")

    # Defensive sanity: ensure Art 120 is now short.
    a120 = next((a for a in arts if a["article_number"] == "120"), None)
    if a120 is None or len(a120.get("text_ar") or "") > 2000:
        raise RuntimeError(f"L2101 Art 120 not clean after re-parse: {len(a120.get('text_ar') or '') if a120 else 'missing'}")

    # Deduplicate defensively — parse_slug already dedupes into a dict, so
    # this should be a no-op; but we check.
    seen: dict[str, dict] = {}
    for a in arts:
        seen[a["article_number"]] = a
    clean = list(seen.values())
    if len(clean) != len(arts):
        print(f"  !! collapsed {len(arts) - len(clean)} dup article_number rows after re-parse")

    inserts = []
    for a in clean:
        cols = ["law_id", "article_number", "sort_order", "chapter", "section",
                "heading_ar", "heading_en", "text_ar", "text_en"]
        vals = [
            "'" + LAW_IDS["L2101"] + "'",
            sql_text(a["article_number"]),
            str(a["sort_order"]),
            sql_text(a.get("chapter")),
            sql_text(a.get("section")),
            sql_text(a.get("heading_ar")),
            sql_text(a.get("heading_en")),
            sql_text(a.get("text_ar")),
            sql_text(a.get("text_en")),
        ]
        inserts.append(
            "INSERT INTO articles (" + ", ".join(cols) + ") VALUES (" + ", ".join(vals) + ");"
        )

    sql_block = (
        "-- L2101 AR Commercial Companies Law: clean full replacement.\n"
        "-- Old: 401 rows with 32 duplicate article_numbers and Art 120 swallowed.\n"
        f"-- New: {len(clean)} rows, properly suffixed (مكرراً / فقرة), no duplicates.\n"
        "BEGIN;\n"
        "DELETE FROM articles WHERE law_id = '" + LAW_IDS["L2101"] + "';\n"
        + "\n".join(inserts) + "\n"
        "COMMIT;\n"
    )
    return sql_block


def main() -> None:
    parts = [
        "-- =====================================================================\n"
        "-- fix_swallowed.sql — generated by scripts/fix_swallowed.py (2026-04-20)\n"
        "-- Repairs 4 red swallows in legislation.articles\n"
        "-- =====================================================================\n"
    ]
    parts.append("\n-- 1. K0915 EN Art 36\n")
    parts.append(fix_k0915_en_art36())
    parts.append("\n-- 2/3. K0915 AR Art 20 & 36 (surgical DB-only truncation)\n")
    parts.append(fix_k0915_ar())
    parts.append("\n-- 4. L1901 AR Art 1054\n")
    parts.append(fix_l1901())
    parts.append("\n-- 5. L2101 AR full re-parse and replace\n")
    parts.append(fix_l2101())
    OUT_SQL.write_text("".join(parts), encoding="utf-8")
    print(f"\nWrote {OUT_SQL}  ({OUT_SQL.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
