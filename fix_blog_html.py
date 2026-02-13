#!/usr/bin/env python3
"""
Fix footers and breadcrumbs in all blog HTML files.

1. Replace footer text logo with image logo
2. Replace "Insights" footer links with "Sijilat" external link
3. Fix breadcrumb "Insights" text to "Knowledge"
"""

import glob
import re
import os

blog_dir = "/tmp/sahwanlaw/blog"
files = sorted(glob.glob(os.path.join(blog_dir, "*.html")))

print(f"Found {len(files)} HTML files to process.\n")

for filepath in files:
    filename = os.path.basename(filepath)
    changes = []

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # ── 1. Replace footer text logo with image logo ──
    # Match both variants: with and without "text-white" class
    logo_pattern = r'<span class="font-serif text-2xl(?:\s+text-white)?">Sahwan Law</span>'
    logo_replacement = '<img src="../images/logo.png" alt="Sahwan Law" class="h-12 w-auto object-contain brightness-0 invert opacity-80">'

    # Only replace the one in the footer area, not content headings.
    # Strategy: find footer section and do replacement there.
    # We'll use a function-based replacement to only replace within <footer> tags.

    footer_match = re.search(r'(<footer[\s\S]*?</footer>)', content)
    if footer_match:
        footer_html = footer_match.group(1)
        new_footer = re.sub(logo_pattern, logo_replacement, footer_html)
        if new_footer != footer_html:
            content = content.replace(footer_html, new_footer)
            count = len(re.findall(logo_pattern, footer_html))
            changes.append(f"  [1] Replaced {count} footer text logo(s) with image logo")

    # ── 2. Replace "Insights" links in footer with "Sijilat" ──
    # Need to handle these patterns in footer:
    #   <a href="../knowledge.html" class="hover:text-gold">Insights</a>
    #   <a href="../index.html#insights" class="text-sm text-white/60 hover:text-white transition-colors">Insights</a>
    # Replace href and text, keep classes, add target="_blank" rel="noopener"

    footer_match = re.search(r'(<footer[\s\S]*?</footer>)', content)
    if footer_match:
        footer_html = footer_match.group(1)
        # Match any <a> with Insights text in footer
        insights_link_pattern = r'<a\s+href="[^"]*"(\s+class="[^"]*")\s*>Insights</a>'

        def replace_footer_insights(m):
            classes = m.group(1)
            return f'<a href="https://sijilat.sahwanlaw.vercel.app/" target="_blank" rel="noopener"{classes}>Sijilat</a>'

        new_footer = re.sub(insights_link_pattern, replace_footer_insights, footer_html)
        if new_footer != footer_html:
            count = len(re.findall(insights_link_pattern, footer_html))
            content = content.replace(footer_html, new_footer)
            changes.append(f"  [2] Replaced {count} footer 'Insights' link(s) with 'Sijilat'")

    # ── 3. Fix breadcrumb "Insights" text to "Knowledge" ──
    # Patterns found:
    #   <a href="../knowledge.html" class="text-navy/50 hover:text-gold">Insights</a>
    #   <a href="../knowledge.html" class="hover:text-gold">Insights</a>
    # Only in breadcrumb/nav area (NOT in footer). We already fixed footer above,
    # so we target non-footer occurrences.

    # To be safe, work on content outside footer.
    # Split content into before-footer and footer+after
    footer_start = content.find('<footer')
    if footer_start != -1:
        before_footer = content[:footer_start]
        after_footer_start = content[footer_start:]
    else:
        before_footer = content
        after_footer_start = ""

    breadcrumb_pattern = r'(<a\s+href="../knowledge\.html"\s+class="[^"]*">)Insights(</a>)'

    def replace_breadcrumb_insights(m):
        return m.group(1) + "Knowledge" + m.group(2)

    new_before = re.sub(breadcrumb_pattern, replace_breadcrumb_insights, before_footer)
    if new_before != before_footer:
        count = len(re.findall(breadcrumb_pattern, before_footer))
        content = new_before + after_footer_start
        changes.append(f"  [3] Replaced {count} breadcrumb 'Insights' text(s) with 'Knowledge'")

    # ── Write if changed ──
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"{filename}:")
        for c in changes:
            print(c)
        print()
    else:
        print(f"{filename}: No changes needed.\n")

print("Done.")
