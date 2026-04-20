#!/usr/bin/env python3
"""
build_laws.py
=============
Sahwan Law Legal Library — static site builder.

Fetches every `legislation` row with published=true (plus its articles) from
the OpenBrain Supabase project via PostgREST, then renders:

  laws/<slug>.html          — English instrument page (LTR)
  ar/laws/<slug>.html       — Arabic mirror (RTL)
  laws/index.html           — bilingual index of published laws
  ar/laws/index.html        — Arabic index

Each instrument page has: bilingual header, breadcrumbs, amendment timeline,
plain-English summary (if any), articles grouped by chapter, client-side
in-page search, LegalDocument JSON-LD, disclaimer block, and a language toggle.

No external deps. Uses urllib + html.escape only. Runs offline against the
public Supabase URL with the anon key (read-only, enforced by RLS).

Usage:
    python build_laws.py
"""
from __future__ import annotations

import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path


# --- Arabic normalization (Lucene-ISRI style) ---
# Equates hamza-bearing alef/ya/waw, ta marbuta vs ha, alef maksura vs ya, strips
# tashkeel + tatweel. Lowercases non-Arabic so mixed queries still match.
_AR_TASHKEEL = re.compile(r'[\u064B-\u065F\u0670\u0640]')
def normalize_ar(s: str) -> str:
    if not s:
        return ''
    s = _AR_TASHKEEL.sub('', s)
    s = re.sub(r'[\u0622\u0623\u0625]', '\u0627', s)  # آ أ إ → ا
    s = s.replace('\u0649', '\u064A')                 # ى → ي (alef maksura → ya)
    s = s.replace('\u0629', '\u0647')                 # ة → ه
    s = s.replace('\u0624', '\u0648')                 # ؤ → و
    s = s.replace('\u0626', '\u064A')                 # ئ → ي
    return s.lower()

REPO_ROOT = Path(__file__).resolve().parent
SUPABASE_URL = "https://tabrszajayygskcecjvm.supabase.co"
SUPABASE_ANON = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    ".eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRhYnJzemFqYXl5Z3NrY2VjanZtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQwMTgyMzAsImV4cCI6MjA4OTU5NDIzMH0"
    ".HiVArtnFAMTNqyEPjQUnKS83lBkE-2LTBNfQjLGKA1k"
)

DISCLAIMER_EN = (
    "This library is a working reference compiled by Sahwan Law from publicly-"
    "available sources, principally the Legislation and Legal Opinion "
    "Commission (legalaffairs.gov.bh). The official Arabic text as published "
    "in the Official Gazette of the Kingdom of Bahrain is the sole "
    "authoritative source of the law. While we endeavour to reflect the law "
    "and all amendments current as of {as_of}, we make no representation or "
    "warranty of completeness, accuracy, or timeliness. This resource does "
    "not constitute legal advice, and no lawyer-client relationship is "
    "created by its use. For binding legal opinion on any specific matter, "
    "please contact Sahwan Law. Use at your own risk."
)

DISCLAIMER_AR = (
    "هذه المكتبة مرجع عملي جمعته سهوان للمحاماة من مصادر علنية، على "
    "رأسها هيئة التشريع والرأي القانوني (legalaffairs.gov.bh). النص العربي "
    "الرسمي المنشور في الجريدة الرسمية لمملكة البحرين هو المصدر الوحيد المعتمد "
    "للقانون. وعلى الرغم من سعينا لبيان القانون وجميع تعديلاته السارية حتى "
    "{as_of}، فإننا لا نُقدِّم أي ضمان بالكمال أو الدقة أو التحديث. ولا يُعدُّ "
    "هذا المرجع استشارة قانونية، ولا تنشأ عنه علاقة موكّل-محامٍ. لاستفسار "
    "ملزم بشأن واقعة محددة يُرجى التواصل مع سهوان للمحاماة. الاستخدام "
    "على مسؤولية المستخدم."
)


# =====================================================================
# Data fetch
# =====================================================================

def fetch(path: str, params: dict[str, str] | None = None) -> list[dict]:
    qs = ("?" + urllib.parse.urlencode(params)) if params else ""
    url = f"{SUPABASE_URL}/rest/v1/{path}{qs}"
    req = urllib.request.Request(
        url,
        headers={
            "apikey": SUPABASE_ANON,
            "Authorization": f"Bearer {SUPABASE_ANON}",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_all_published() -> list[dict]:
    laws = fetch(
        "legislation",
        {"select": "*", "published": "eq.true", "order": "category.asc,title_en.asc"},
    )
    # Fetch articles for each
    for law in laws:
        law["articles"] = fetch(
            "articles",
            {
                "select": "*",
                "law_id": f"eq.{law['id']}",
                "order": "sort_order.asc",
            },
        )
    return laws


# =====================================================================
# Rendering helpers — mirror sahwanlaw blog chrome (Tailwind CDN)
# =====================================================================

def render_nav(lang: str, relpath: str) -> str:
    # Match knowledge.html nav exactly. For /laws/*.html relpath='' and /ar/laws/*.html relpath='../' — everything else resolves through ../ prefix.
    root = f"{relpath}../" if lang == "en" else f"{relpath}../../"
    if lang == "ar":
        return f"""
    <nav class="fixed top-0 left-0 right-0 z-40 bg-white/95 backdrop-blur-md py-4 shadow-sm border-b border-gray-100" dir="rtl">
      <div class="container mx-auto px-6 md:px-12 flex items-center justify-between">
        <a href="{root}index.html" class="flex items-center gap-4 relative z-50 group">
          <img src="{root}images/logo.png" alt="سهوان للمحاماة" class="h-14 md:h-16 w-auto object-contain">
        </a>
        <div class="hidden lg:flex items-center gap-10">
          <ul class="flex gap-8">
            <li><a href="{root}index.html" class="text-xs font-sans uppercase tracking-widest text-navy/60 hover:text-navy py-2 relative group">الرئيسية<span class="absolute bottom-0 right-0 h-px bg-gold w-0 group-hover:w-full transition-all duration-300"></span></a></li>
            <li><a href="{root}index.html#services" class="text-xs font-sans uppercase tracking-widest text-navy/60 hover:text-navy py-2 relative group">الخدمات<span class="absolute bottom-0 right-0 h-px bg-gold w-0 group-hover:w-full transition-all duration-300"></span></a></li>
            <li><a href="{root}index.html#legacy" class="text-xs font-sans uppercase tracking-widest text-navy/60 hover:text-navy py-2 relative group">من نحن<span class="absolute bottom-0 right-0 h-px bg-gold w-0 group-hover:w-full transition-all duration-300"></span></a></li>
            <li><a href="https://sijilat.sahwanlaw.com/" target="_blank" rel="noopener" class="text-xs font-sans uppercase tracking-widest text-navy/60 hover:text-navy py-2 relative group">سجلات<span class="absolute bottom-0 right-0 h-px bg-gold w-0 group-hover:w-full transition-all duration-300"></span></a></li>
            <li><a href="{root}ar/blog/" class="text-xs font-sans uppercase tracking-widest text-navy font-medium py-2 relative">المعرفة<span class="absolute bottom-0 right-0 h-px w-full bg-gold"></span></a></li>
            <li><a href="{root}index.html#contact" class="text-xs font-sans uppercase tracking-widest text-navy/60 hover:text-navy py-2 relative group">الوظائف<span class="absolute bottom-0 right-0 h-px bg-gold w-0 group-hover:w-full transition-all duration-300"></span></a></li>
          </ul>
          <div class="flex items-center gap-4">
            <a href="https://sas-team.vercel.app" target="_blank" rel="noopener" class="text-navy/30 hover:text-gold transition-colors duration-300" title="بوابة الموظفين">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
            </a>
            <a href="{root}index.html#contact" class="text-[10px] font-bold uppercase tracking-[0.2em] px-6 py-3 bg-navy text-white hover:bg-gold transition-colors duration-300">تواصل</a>
            <a href="{root}laws/{{EN_SLUG}}.html" class="text-[10px] font-medium uppercase tracking-[0.2em] px-3 py-2 border border-navy/20 text-navy/60 hover:text-gold hover:border-gold transition-colors duration-300">EN</a>
          </div>
        </div>
        <!-- Mobile: Language toggle + hamburger (AR page) -->
        <div class="flex items-center gap-4 lg:hidden">
          <a href="{root}laws/{{EN_SLUG}}.html" class="text-[10px] font-bold uppercase tracking-widest text-navy hover:text-gold border border-navy/20 px-2 py-1 rounded">EN</a>
          <button id="mobile-menu-btn" class="text-navy focus:outline-none" aria-label="فتح القائمة">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
          </button>
        </div>
      </div>
      <div id="mobile-menu" class="hidden lg:hidden bg-white border-t border-gray-100 absolute w-full inset-x-0 top-full shadow-lg" dir="rtl">
        <ul class="flex flex-col p-6 space-y-4">
          <li><a href="{root}index.html" class="block text-sm font-medium text-navy/60 hover:text-navy">الرئيسية</a></li>
          <li><a href="{root}index.html#services" class="block text-sm font-medium text-navy/60 hover:text-navy">الخدمات</a></li>
          <li><a href="{root}index.html#legacy" class="block text-sm font-medium text-navy/60 hover:text-navy">من نحن</a></li>
          <li><a href="https://sijilat.sahwanlaw.com/" target="_blank" rel="noopener" class="block text-sm font-medium text-navy/60 hover:text-navy">سجلات</a></li>
          <li><a href="{root}ar/blog/" class="block text-sm font-medium text-navy hover:text-gold">المعرفة</a></li>
          <li><a href="{root}index.html#contact" class="block text-sm font-medium text-navy/60 hover:text-navy">تواصل</a></li>
        </ul>
      </div>
    </nav>
    <script>
      (function(){{
        var b=document.getElementById('mobile-menu-btn'), m=document.getElementById('mobile-menu');
        if(b&&m) b.addEventListener('click', function(){{ m.classList.toggle('hidden'); }});
      }})();
    </script>
"""
    return f"""
    <nav class="fixed top-0 left-0 right-0 z-40 bg-white/95 backdrop-blur-md py-4 shadow-sm border-b border-gray-100">
      <div class="container mx-auto px-6 md:px-12 flex items-center justify-between">
        <a href="{root}index.html" class="flex items-center gap-4 relative z-50 group">
          <img src="{root}images/logo.png" alt="Sahwan Law - Leading Law Firm in Bahrain Since 1975 - Logo" class="h-14 md:h-16 w-auto object-contain">
        </a>
        <div class="hidden lg:flex items-center gap-10">
          <ul class="flex gap-8">
            <li><a href="{root}index.html" class="text-xs font-sans uppercase tracking-widest text-navy/60 hover:text-navy py-2 relative group">Home<span class="absolute bottom-0 left-0 h-px bg-gold w-0 group-hover:w-full transition-all duration-300"></span></a></li>
            <li><a href="{root}index.html#services" class="text-xs font-sans uppercase tracking-widest text-navy/60 hover:text-navy py-2 relative group">Services<span class="absolute bottom-0 left-0 h-px bg-gold w-0 group-hover:w-full transition-all duration-300"></span></a></li>
            <li><a href="{root}index.html#legacy" class="text-xs font-sans uppercase tracking-widest text-navy/60 hover:text-navy py-2 relative group">About<span class="absolute bottom-0 left-0 h-px bg-gold w-0 group-hover:w-full transition-all duration-300"></span></a></li>
            <li><a href="https://sijilat.sahwanlaw.com/" target="_blank" rel="noopener" class="text-xs font-sans uppercase tracking-widest text-navy/60 hover:text-navy py-2 relative group">Sijilat<span class="absolute bottom-0 left-0 h-px bg-gold w-0 group-hover:w-full transition-all duration-300"></span></a></li>
            <li><a href="{root}knowledge.html" class="text-xs font-sans uppercase tracking-widest text-navy font-medium py-2 relative">Knowledge<span class="absolute bottom-0 left-0 h-px w-full bg-gold"></span></a></li>
            <li><a href="{root}index.html#contact" class="text-xs font-sans uppercase tracking-widest text-navy/60 hover:text-navy py-2 relative group">Careers<span class="absolute bottom-0 left-0 h-px bg-gold w-0 group-hover:w-full transition-all duration-300"></span></a></li>
          </ul>
          <div class="flex items-center gap-4">
            <a href="https://sas-team.vercel.app" target="_blank" rel="noopener" class="text-navy/30 hover:text-gold transition-colors duration-300" title="Staff Portal">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
            </a>
            <a href="{root}index.html#contact" class="text-[10px] font-bold uppercase tracking-[0.2em] px-6 py-3 bg-navy text-white hover:bg-gold transition-colors duration-300">Contact</a>
            <a href="{root}ar/laws/{{AR_SLUG}}.html" class="text-[10px] font-medium uppercase tracking-[0.2em] px-3 py-2 border border-navy/20 text-navy/60 hover:text-gold hover:border-gold transition-colors duration-300">العربية</a>
          </div>
        </div>
        <!-- Mobile: Language toggle + hamburger -->
        <div class="flex items-center gap-4 lg:hidden">
          <a href="{root}ar/laws/{{AR_SLUG}}.html" class="text-[10px] font-bold uppercase tracking-widest text-navy hover:text-gold border border-navy/20 px-2 py-1 rounded">AR</a>
          <button id="mobile-menu-btn" class="text-navy focus:outline-none" aria-label="Open Menu">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
          </button>
        </div>
      </div>
      <div id="mobile-menu" class="hidden lg:hidden bg-white border-t border-gray-100 absolute w-full inset-x-0 top-full shadow-lg">
        <ul class="flex flex-col p-6 space-y-4">
          <li><a href="{root}index.html" class="block text-sm font-medium text-navy/60 hover:text-navy">Home</a></li>
          <li><a href="{root}index.html#services" class="block text-sm font-medium text-navy/60 hover:text-navy">Services</a></li>
          <li><a href="{root}index.html#legacy" class="block text-sm font-medium text-navy/60 hover:text-navy">About Us</a></li>
          <li><a href="https://sijilat.sahwanlaw.com/" target="_blank" rel="noopener" class="block text-sm font-medium text-navy/60 hover:text-navy">Sijilat</a></li>
          <li><a href="{root}knowledge.html" class="block text-sm font-medium text-navy hover:text-gold">Knowledge</a></li>
          <li><a href="{root}index.html#contact" class="block text-sm font-medium text-navy/60 hover:text-navy">Contact</a></li>
        </ul>
      </div>
    </nav>
    <script>
      (function(){{
        var b=document.getElementById('mobile-menu-btn'), m=document.getElementById('mobile-menu');
        if(b&&m) b.addEventListener('click', function(){{ m.classList.toggle('hidden'); }});
      }})();
    </script>
"""


def render_footer(lang: str, relpath: str) -> str:
    root = f"{relpath}../" if lang == "en" else f"{relpath}../../"
    if lang == "ar":
        return f"""
    <footer class="bg-navy py-16 border-t border-white/10" dir="rtl">
      <div class="container mx-auto px-6 md:px-12">
        <div class="flex flex-col md:flex-row items-center justify-between gap-8">
          <div>
            <img src="{root}images/logo.png" alt="سهوان للمحاماة" class="h-12 w-auto object-contain brightness-0 invert opacity-80">
            <p class="text-white/50 text-sm mt-2">تأسست 1975 • المنامة، البحرين</p>
          </div>
          <div class="flex items-center gap-6">
            <a href="{root}index.html" class="text-sm text-white/60 hover:text-white transition-colors">الرئيسية</a>
            <a href="{root}index.html#services" class="text-sm text-white/60 hover:text-white transition-colors">الخدمات</a>
            <a href="https://sijilat.sahwanlaw.com/" target="_blank" rel="noopener" class="text-sm text-white/60 hover:text-white transition-colors">سجلات</a>
            <a href="{root}ar/blog/" class="text-sm text-white/60 hover:text-white transition-colors">المعرفة</a>
            <a href="{root}index.html#contact" class="text-sm text-white/60 hover:text-white transition-colors">تواصل</a>
          </div>
        </div>
        <div class="border-t border-white/10 mt-12 pt-8 text-center">
          <p class="text-white/40 text-xs">© 2025 سلمان عبدالله سهوان للمحاماة والاستشارات القانونية. جميع الحقوق محفوظة.</p>
        </div>
      </div>
    </footer>
"""
    return f"""
    <footer class="bg-navy py-16 border-t border-white/10">
      <div class="container mx-auto px-6 md:px-12">
        <div class="flex flex-col md:flex-row items-center justify-between gap-8">
          <div>
            <img src="{root}images/logo.png" alt="Sahwan Law" class="h-12 w-auto object-contain brightness-0 invert opacity-80">
            <p class="text-white/50 text-sm mt-2">Established 1975 • Manama, Bahrain</p>
          </div>
          <div class="flex items-center gap-6">
            <a href="{root}index.html" class="text-sm text-white/60 hover:text-white transition-colors">Home</a>
            <a href="{root}index.html#services" class="text-sm text-white/60 hover:text-white transition-colors">Services</a>
            <a href="https://sijilat.sahwanlaw.com/" target="_blank" rel="noopener" class="text-sm text-white/60 hover:text-white transition-colors">Sijilat</a>
            <a href="{root}knowledge.html" class="text-sm text-white/60 hover:text-white transition-colors">Knowledge</a>
            <a href="{root}index.html#contact" class="text-sm text-white/60 hover:text-white transition-colors">Contact</a>
          </div>
        </div>
        <div class="border-t border-white/10 mt-12 pt-8 text-center">
          <p class="text-white/40 text-xs">© 2025 Salman A. Sahwan - Attorneys & Legal Consultants. All rights reserved.</p>
        </div>
      </div>
    </footer>
"""


HEAD_TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}" dir="{dir}">
<head>
  <link rel="icon" type="image/x-icon" href="{relpath}../images/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="{relpath}../images/favicon-32x32.png">
  <link rel="manifest" href="{relpath}../site.webmanifest">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="theme-color" content="#1a2b3c">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="https://www.sahwanlaw.com/{canonical_path}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="https://www.sahwanlaw.com/{canonical_path}">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          colors: {{ navy: '#1a3a5c', gold: '#c9a962', pearl: '#f8f7f4' }},
          fontFamily: {{
            serif: ['"Cormorant Garamond"', 'Georgia', 'serif'],
            sans: ['Inter', 'system-ui', 'sans-serif'],
            ar: ['"Noto Naskh Arabic"', '"Amiri"', 'serif'],
          }},
        }}
      }}
    }}
  </script>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=Inter:wght@300;400;500;600&family=Noto+Naskh+Arabic:wght@400;500;600;700&display=swap" rel="stylesheet">
  {jsonld}
</head>
<body class="bg-pearl {fontclass} text-navy antialiased">
"""


def render_breadcrumbs(lang: str, title: str, relpath: str) -> str:
    if lang == "ar":
        return f"""
        <nav class="mb-8 text-sm" dir="rtl">
          <a href="{relpath}../" class="text-navy/50 hover:text-gold">الرئيسية</a>
          <span class="text-navy/30 mx-2">/</span>
          <a href="{relpath}../../ar/blog/" class="text-navy/50 hover:text-gold">المعرفة</a>
          <span class="text-navy/30 mx-2">/</span>
          <span class="text-navy">{html.escape(title)}</span>
        </nav>
"""
    return f"""
        <nav class="mb-8 text-sm">
          <a href="{relpath}../index.html" class="text-navy/50 hover:text-gold">Home</a>
          <span class="text-navy/30 mx-2">/</span>
          <a href="{relpath}../knowledge.html" class="text-navy/50 hover:text-gold">Knowledge</a>
          <span class="text-navy/30 mx-2">/</span>
          <span class="text-navy">{html.escape(title)}</span>
        </nav>
"""


def json_ld(law: dict) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "Legislation",
        "name": law.get("title_en") or "",
        "alternativeHeadline": law.get("title_ar") or "",
        "legislationType": law.get("type") or "",
        "legislationIdentifier": f"{law.get('number') or ''}/{law.get('year') or ''}",
        "legislationPassedBy": law.get("issuing_authority") or "",
        "legislationDate": law.get("date_issued") or "",
        "legislationJurisdiction": "BH",
        "inLanguage": ["ar", "en"],
        "about": {"@type": "Thing", "name": law.get("category") or ""},
        "isPartOf": {"@type": "DataCatalog", "name": "Sahwan Law Bahrain Legal Library"},
        "publisher": {"@type": "LegalService", "name": "Sahwan Law", "url": "https://sahwanlaw.com"},
        "dateModified": law.get("as_of_date") or "",
        "mainEntityOfPage": f"https://www.sahwanlaw.com/laws/{law['slug']}.html",
    }
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"


def render_amendments(law: dict, lang: str) -> str:
    amendments = law.get("amendments") or []
    if not amendments:
        return ""  # silent when there are none — no "No amendments on record" clutter
    header = "التعديلات" if lang == "ar" else "Amendments"
    rows = []
    for a in amendments:
        dnum = html.escape(str(a.get("decree_no", "")))
        date = html.escape(str(a.get("date", "")))
        og = html.escape(str(a.get("og_number", ""))) if a.get("og_number") else ""
        row = f"<li class=\"py-2 border-b border-navy/10\"><span class=\"font-medium\">{dnum}</span>"
        if date:
            row += f" <span class=\"text-navy/60\">— {date}</span>"
        if og:
            row += f" <span class=\"text-navy/40 text-sm\">(OG #{og})</span>"
        row += "</li>"
        rows.append(row)
    return f"""
<div class="bg-white border border-navy/10 rounded-lg p-6">
  <h3 class="font-serif text-xl text-navy mb-4">{header}</h3>
  <ul>{''.join(rows)}</ul>
</div>
"""


def render_articles(law: dict, lang: str) -> str:
    articles = law.get("articles") or []
    if not articles:
        if lang == "ar":
            return '<p class="text-navy/60 italic">لا توجد مواد مسجلة حتى الآن.</p>'
        return '<p class="text-navy/60 italic">No articles loaded yet for this instrument.</p>'
    field_text = "text_ar" if lang == "ar" else "text_en"
    field_heading = "heading_ar" if lang == "ar" else "heading_en"
    label_article = "المادة" if lang == "ar" else "Article"
    dir_attr = 'dir="rtl"' if lang == "ar" else ""
    items = []
    current_chapter = None
    for a in articles:
        # Skip synthetic "Preamble-N" rows — they capture the decree's opening recitals
        # ("بعد الاطلاع على الدستور...") which are framing, not law articles.
        if str(a.get("article_number") or "").startswith("Preamble-"):
            continue
        # Chapter field in DB is Arabic only — only render on Arabic page; English page skips
        chap = a.get("chapter")
        if lang == "ar" and chap and chap != current_chapter:
            current_chapter = chap
            items.append(
                f'<h3 class="font-serif text-xl md:text-2xl text-navy mt-10 mb-4 pb-2 border-b border-gold/30 chapter-heading" {dir_attr}>{html.escape(chap)}</h3>'
            )
        # Fall back to the Arabic text on the English page when the English text is missing.
        # Most of our 27 laws are Arabic-only (treaties, resolutions, older laws with no
        # official English translation). Rendering an empty <p> looks broken; showing the
        # Arabic original with a subtle "Original Arabic text" note is the honest presentation.
        primary = a.get(field_text) or ""
        used_fallback = False
        if not primary.strip() and lang == "en":
            primary = a.get("text_ar") or ""
            used_fallback = bool(primary.strip())
        text = primary
        heading = a.get(field_heading) or ""
        # On the English page, when we fall back, swap direction to RTL for the article body
        article_dir = 'dir="rtl"' if (lang == "ar" or used_fallback) else ""
        # Normalise whitespace: the source docx has aggressive per-clause paragraph breaks,
        # which makes every subclause render on its own line. Collapse consecutive blank
        # lines to a paragraph break, single newlines to a space, and inject <br> before
        # structural markers like "(1)", "(a)", "أ-", "ب-", "١-" so subclauses stay readable.
        import re as _re
        norm = _re.sub(r"\n{2,}", "\u2029", text)  # U+2029 = paragraph separator
        norm = _re.sub(r"\n", " ", norm)
        norm = _re.sub(r" {2,}", " ", norm).strip()
        # Break before roman or arabic sub-markers at clause starts — keep paragraph flow but re-inject breaks where the law structure expects them
        norm = _re.sub(r"(?<=\S)\s+(\([A-Za-z0-9٠-٩]+\))", r"<br>\1", norm)
        norm = _re.sub(r"(?<=\S)\s+([٠-٩]+\s*-)", r"<br>\1", norm)
        norm = _re.sub(r"(?<=\S)\s+([أ-ي]\s*-)", r"<br>\1", norm)
        parts = [html.escape(p).replace("&lt;br&gt;", "<br>") for p in norm.split("\u2029")]
        safe_text = "</p><p class='text-navy/80 leading-relaxed text-justify mt-3'>".join(parts)
        anchor = f"article-{html.escape(str(a['article_number'])).replace(' ', '-')}"
        fallback_note = (
            '<p class="text-xs text-navy/40 italic mb-1" dir="ltr">— Original Arabic text (no official English translation available) —</p>'
            if used_fallback else ""
        )
        items.append(f"""
<article id="{anchor}" class="law-article border-r-2 border-gold/40 pr-4 py-3 mb-2 hover:bg-white/50 transition-colors" {article_dir} data-num="{html.escape(str(a['article_number']))}" data-text="{html.escape(normalize_ar(text))}">
  <div class="flex items-baseline gap-3 mb-2">
    <span class="font-serif text-lg text-gold font-semibold">{label_article} {html.escape(str(a['article_number']))}</span>
    {f'<span class="text-sm text-navy/70 font-medium">{html.escape(heading)}</span>' if heading else ''}
  </div>
  {fallback_note}
  <p class="text-navy/80 leading-relaxed text-justify">{safe_text}</p>
</article>
""")
    return "\n".join(items)


def render_instrument_page(law: dict, lang: str) -> str:
    is_ar = lang == "ar"
    dir_attr = "rtl" if is_ar else "ltr"
    fontclass = "font-ar" if is_ar else "font-sans"
    title_field = "title_ar" if is_ar else "title_en"
    summary_field = "summary_ar" if is_ar else "summary_en"
    title = law.get(title_field) or law.get("title_en") or law["slug"]
    summary = law.get(summary_field) or law.get("summary_en") or ""
    relpath = "../" if is_ar else ""
    canonical_path = f"ar/laws/{law['slug']}.html" if is_ar else f"laws/{law['slug']}.html"

    search_label = "ابحث في مواد هذا التشريع..." if is_ar else "Search articles in this law..."
    summary_label = "ملخص سهوان للمحاماة" if is_ar else "Sahwan Law practitioner summary"
    articles_label = "النص الكامل — المواد" if is_ar else "Full text — Articles"
    as_of_label = "محدَّث حتى" if is_ar else "Current as of"
    # review_badge removed — summaries under editorial review no longer flagged to end users
    review_badge = ""

    # Primary-source (LLOC) sidebar removed — not needed in public-facing page
    source_block = ""

    amendments_html = render_amendments(law, lang)
    articles_html = render_articles(law, lang)

    disclaimer = (DISCLAIMER_AR if is_ar else DISCLAIMER_EN).format(as_of=law.get("as_of_date") or "")

    return HEAD_TEMPLATE.format(
        lang=lang,
        dir=dir_attr,
        title=html.escape(title) + " | Sahwan Law Legal Library",
        description=html.escape((summary or title)[:160]),
        canonical_path=canonical_path,
        og_title=html.escape(title),
        jsonld=json_ld(law),
        fontclass=fontclass,
        relpath=relpath,
    ) + render_nav(lang, relpath).replace("{EN_SLUG}", law["slug"]).replace("{AR_SLUG}", law["slug"]) + f"""
    <main class="pt-32 pb-24" dir="{dir_attr}">
      <article class="container mx-auto px-6 md:px-12 max-w-5xl">
        {render_breadcrumbs(lang, title, relpath)}
        <header class="mb-10">
          <div class="flex flex-wrap items-center gap-2 mb-6">
            <span class="inline-block px-3 py-1 bg-navy text-white text-xs font-semibold uppercase tracking-wider rounded">{'تشريع' if is_ar else 'Legislation'}</span>
            <span class="inline-block px-3 py-1 bg-gold/10 text-gold text-xs font-medium uppercase tracking-wider rounded">{html.escape((law.get('category_ar') if is_ar else law.get('category')) or '')}</span>
          </div>
          <h1 class="font-serif text-3xl md:text-5xl text-navy leading-tight mb-4">{html.escape(title)}</h1>
          <p class="text-navy/60 text-sm">{as_of_label}: <time datetime="{law.get('as_of_date') or ''}">{law.get('as_of_date') or ''}</time></p>
        </header>

        <div class="bg-white p-8 rounded-lg border border-navy/10 mb-12">
          <h2 class="font-serif text-2xl text-navy mb-4">{summary_label}</h2>
          <p class="text-navy/80 leading-relaxed text-justify whitespace-pre-line">{html.escape(summary) if summary else ('<em class="text-navy/50">(no summary yet)</em>' if not is_ar else '<em class="text-navy/50">(لم يُضف ملخص بعد)</em>')}</p>
          {amendments_html}
        </div>

        <section>
          <div class="flex items-center justify-between mb-6 flex-wrap gap-3">
            <h2 class="font-serif text-3xl text-navy">{articles_label}</h2>
            <input type="search" id="article-search" placeholder="{search_label}" class="border border-navy/20 rounded px-4 py-2 w-full md:w-72 focus:outline-none focus:border-gold">
          </div>
          <div id="articles-container" class="space-y-1">
            {articles_html}
          </div>
          <p id="no-results" class="hidden text-navy/60 italic mt-6">— no matches —</p>
        </section>

        <aside class="mt-16 bg-navy/5 p-6 border-l-4 border-gold text-sm text-navy/70 leading-relaxed">
          <strong class="block font-serif text-navy mb-2">{'إخلاء مسؤولية' if is_ar else 'Disclaimer'}</strong>
          <p>{html.escape(disclaimer)}</p>
        </aside>
      </article>
    </main>
""" + render_footer(lang, relpath) + """
    <script>
      (function () {
        const search = document.getElementById('article-search');
        const articles = document.querySelectorAll('.law-article');
        const chapters = document.querySelectorAll('.chapter-heading');
        const noResults = document.getElementById('no-results');
        if (!search) return;

        // Cache each article's original innerHTML once so we can restore + re-highlight cleanly
        articles.forEach(el => { if (!el.dataset.originalHtml) el.dataset.originalHtml = el.innerHTML; });

        function escapeRegex(s) { return s.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&'); }

        // Arabic normalization (mirrors server-side): equates hamza variants, ta marbuta, ya maksura; strips tashkeel+tatweel
        function normalizeAr(s) {
          if (!s) return '';
          return s
            .replace(/[\u064B-\u065F\u0670\u0640]/g, '')       // tashkeel + tatweel
            .replace(/[\u0622\u0623\u0625]/g, '\u0627')          // آ أ إ → ا
            .replace(/\u0649/g, '\u064A')                         // ى → ي
            .replace(/\u0629/g, '\u0647')                         // ة → ه
            .replace(/\u0624/g, '\u0648')                         // ؤ → و
            .replace(/\u0626/g, '\u064A')                         // ئ → ي
            .toLowerCase();
        }

        // Build a regex from a query that matches any equivalent Arabic variant + allows
        // optional tashkeel/tatweel between characters. For Latin/digit chars, escape literally.
        const AR_EQUIV = {
          '\u0627': '[\u0622\u0623\u0625\u0627]',   // ا
          '\u064A': '[\u0649\u064A\u0626]',          // ي
          '\u0647': '[\u0629\u0647]',                 // ه
          '\u0648': '[\u0624\u0648]'                  // و
        };
        function buildHighlightRegex(query) {
          const nq = normalizeAr(query);
          const parts = [...nq].map(ch => AR_EQUIV[ch] || escapeRegex(ch));
          // Allow tashkeel/tatweel to appear between letters in the original text
          return new RegExp(parts.join('[\u064B-\u065F\u0670\u0640]*'), 'gi');
        }

        function highlight(el, query) {
          el.innerHTML = el.dataset.originalHtml;  // always reset first
          if (!query) return;
          const re = buildHighlightRegex(query);
          const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, {
            acceptNode: n => (n.parentNode && /^(SCRIPT|STYLE|MARK)$/i.test(n.parentNode.tagName))
              ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT
          });
          const targets = [];
          let n; while ((n = walker.nextNode())) { if (re.test(n.textContent)) { re.lastIndex = 0; targets.push(n); } }
          targets.forEach(node => {
            const frag = document.createDocumentFragment();
            let last = 0; const text = node.textContent;
            text.replace(re, (m, off) => {
              if (off > last) frag.appendChild(document.createTextNode(text.slice(last, off)));
              const mark = document.createElement('mark');
              mark.className = 'bg-gold/40 text-navy px-0.5 rounded';
              mark.textContent = m;
              frag.appendChild(mark);
              last = off + m.length;
            });
            if (last < text.length) frag.appendChild(document.createTextNode(text.slice(last)));
            node.parentNode.replaceChild(frag, node);
          });
        }

        search.addEventListener('input', () => {
          const raw = search.value.trim();
          const q = normalizeAr(raw);
          let shown = 0;
          articles.forEach(el => {
            const haystack = (el.dataset.text || '') + ' ' + (el.dataset.num || '');
            const match = !q || haystack.includes(q);
            el.style.display = match ? '' : 'none';
            if (match) { shown++; highlight(el, raw); }
            else { el.innerHTML = el.dataset.originalHtml; }
          });
          chapters.forEach(el => { el.style.display = q ? 'none' : ''; });
          noResults.classList.toggle('hidden', shown > 0);
        });
      })();
    </script>
  </body>
</html>
"""


def render_index(laws: list[dict], lang: str) -> str:
    is_ar = lang == "ar"
    dir_attr = "rtl" if is_ar else "ltr"
    fontclass = "font-ar" if is_ar else "font-sans"
    relpath = "../" if is_ar else ""
    title_field = "title_ar" if is_ar else "title_en"
    title = "المكتبة القانونية — تشريعات مملكة البحرين" if is_ar else "Legal Library — Legislation of the Kingdom of Bahrain"
    intro = (
        "مجموعة مُنظَّمة ثنائية اللغة للتشريعات البحرينية، مع تتبُّع للتعديلات وربط بالمصادر الرسمية."
        if is_ar
        else "A curated bilingual catalogue of Bahraini legislation with amendment tracking and links to primary sources."
    )
    cards = []
    by_cat: dict[str, list[dict]] = {}
    for l in laws:
        by_cat.setdefault(l.get("category") or "Uncategorised", []).append(l)

    for cat, items in by_cat.items():
        cards.append(f'<h2 class="font-serif text-2xl text-navy mt-12 mb-4 pb-2 border-b border-navy/10">{html.escape(cat)}</h2>')
        cards.append('<ul class="grid md:grid-cols-2 gap-4">')
        for l in items:
            t = l.get(title_field) or l.get("title_en") or l["slug"]
            href = f"{l['slug']}.html"
            cards.append(f"""
              <li class="bg-white p-6 border border-navy/10 rounded-lg hover:border-gold transition-colors">
                <a href="{href}" class="block">
                  <span class="text-xs uppercase tracking-wider text-gold">{html.escape(l.get('type') or '')}</span>
                  <h3 class="font-serif text-lg text-navy leading-tight mt-2">{html.escape(t)}</h3>
                  <p class="text-navy/60 text-sm mt-2">{l.get('year') or ''}</p>
                </a>
              </li>
            """)
        cards.append('</ul>')

    return HEAD_TEMPLATE.format(
        lang=lang,
        dir=dir_attr,
        title=title + " | Sahwan Law",
        description=html.escape(intro),
        canonical_path=("ar/laws/index.html" if is_ar else "laws/index.html"),
        og_title=title,
        jsonld="",
        fontclass=fontclass,
        relpath=relpath,
    ) + render_nav(lang, relpath).replace("{EN_SLUG}", "").replace("{AR_SLUG}", "") + f"""
    <main class="pt-32 pb-24" dir="{dir_attr}">
      <div class="container mx-auto px-6 md:px-12 max-w-5xl">
        <header class="mb-10">
          <h1 class="font-serif text-4xl md:text-5xl text-navy leading-tight mb-4">{html.escape(title)}</h1>
          <p class="text-navy/70 text-lg">{html.escape(intro)}</p>
        </header>
        {''.join(cards) or '<p class="text-navy/60 italic">No published instruments yet.</p>'}
      </div>
    </main>
""" + render_footer(lang, relpath) + "\n  </body>\n</html>\n"


# =====================================================================
# Auto-maintained cards in knowledge.html + ar/blog/index.html
# =====================================================================

SENTINEL_START = "<!-- LEGISLATION_CARDS_START"
SENTINEL_END = "<!-- LEGISLATION_CARDS_END -->"


def _slugify_tag(s: str) -> str:
    if not s:
        return "legislation"
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "legislation"


def _truncate(s: str, n: int = 220) -> str:
    s = (s or "").strip().replace("\n", " ").replace("\r", " ")
    s = re.sub(r"\s+", " ", s)
    if len(s) <= n:
        return s
    cut = s[:n].rsplit(" ", 1)[0]
    return cut + "…"


def _card_date(law: dict) -> str:
    d = law.get("date_issued") or ""
    if d:
        return d
    y = law.get("year")
    return f"{y}-01-01" if y else ""


def render_card_en(law: dict) -> str:
    slug = law["slug"]
    title = html.escape(law.get("title_en") or slug)
    summary = html.escape(_truncate(law.get("summary_en") or ""))
    category = html.escape(law.get("category") or "Legislation")
    tag = _slugify_tag(law.get("category") or "")
    year = html.escape(str(law.get("year") or ""))
    date_iso = html.escape(_card_date(law))
    return f"""              <!-- English: {title} -->
              <a href="laws/{slug}.html" class="article-card group bg-white p-8 border border-navy/5 hover:border-gold/30 hover:shadow-lg transition-all duration-300" data-lang="en" data-type="legislation" data-tag="{tag}" data-date="{date_iso}">
                <div class="flex items-center gap-2 mb-4">
                  <span class="text-[10px] uppercase tracking-widest font-bold px-2 py-1 rounded-sm bg-navy text-white">Legislation</span>
                  <span class="text-[10px] px-2 py-1 rounded-sm bg-gold/20 text-gold">{category}</span>
                  <span class="text-sm text-navy/40 ml-auto">{year}</span>
                </div>
                <h2 class="font-serif text-xl text-navy mb-3 group-hover:text-gold transition-colors leading-tight">{title}</h2>
                <p class="text-navy/50 text-sm font-light leading-relaxed mb-4 line-clamp-3">{summary}</p>
                <span class="text-xs font-medium uppercase tracking-widest text-navy flex items-center gap-2 group-hover:gap-4 transition-all">Read Full Text <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg></span>
              </a>"""


def render_card_ar(law: dict) -> str:
    slug = law["slug"]
    title = html.escape(law.get("title_ar") or law.get("title_en") or slug)
    summary = html.escape(_truncate(law.get("summary_ar") or ""))
    category = html.escape(law.get("category_ar") or law.get("category") or "تشريع")
    tag = _slugify_tag(law.get("category") or "")
    year = html.escape(str(law.get("year") or ""))
    date_iso = html.escape(_card_date(law))
    return f"""              <!-- Arabic: {title} -->
              <a href="../laws/{slug}.html" class="article-card group bg-white p-8 border border-navy/5 hover:border-gold/30 hover:shadow-lg transition-all duration-300" data-lang="ar" data-type="legislation" data-tag="{tag}" data-date="{date_iso}">
                <div class="flex items-center gap-2 mb-4">
                  <span class="text-[10px] uppercase tracking-widest font-bold px-2 py-1 rounded-sm bg-navy text-white">تشريع</span>
                  <span class="text-[10px] px-2 py-1 rounded-sm bg-gold/20 text-gold">{category}</span>
                  <span class="text-sm text-navy/40 mr-auto">{year}</span>
                </div>
                <h2 class="font-serif text-xl text-navy mb-3 group-hover:text-gold transition-colors leading-tight">{title}</h2>
                <p class="text-navy/50 text-sm font-light leading-relaxed mb-4 line-clamp-3">{summary}</p>
                <span class="text-xs font-medium uppercase tracking-widest text-navy flex items-center gap-2 group-hover:gap-4 transition-all">النص الكامل <svg class="w-4 h-4 rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg></span>
              </a>"""


def update_sentinel_block(path: Path, cards_html: str) -> bool:
    """Replace content between LEGISLATION_CARDS_START and _END with cards_html.
    Returns True if file was modified, False if sentinels not found or content unchanged.
    """
    if not path.exists():
        print(f"  [skip] {path} not found")
        return False
    src = path.read_text(encoding="utf-8")
    start_idx = src.find(SENTINEL_START)
    end_idx = src.find(SENTINEL_END)
    if start_idx == -1 or end_idx == -1 or end_idx < start_idx:
        print(f"  [skip] sentinels not found in {path.name}")
        return False
    # Keep the opening sentinel line intact; replace everything between end-of-that-line and the END marker.
    line_end = src.find("\n", start_idx)
    if line_end == -1:
        return False
    before = src[: line_end + 1]
    after = src[end_idx:]
    new = before + cards_html + "\n              " + after
    if new == src:
        return False
    path.write_text(new, encoding="utf-8")
    return True


def maintain_knowledge_cards(laws: list[dict]) -> None:
    # Order: most recent first (date_issued desc, then year desc)
    sorted_laws = sorted(
        laws,
        key=lambda l: (l.get("date_issued") or f"{l.get('year') or 0}-00-00"),
        reverse=True,
    )
    cards_en = "\n".join(render_card_en(l) for l in sorted_laws)
    cards_ar = "\n".join(render_card_ar(l) for l in sorted_laws)

    en_path = REPO_ROOT / "knowledge.html"
    ar_path = REPO_ROOT / "ar" / "blog" / "index.html"
    if update_sentinel_block(en_path, cards_en):
        print(f"  updated knowledge.html ({len(sorted_laws)} cards)")
    else:
        print(f"  knowledge.html unchanged")
    if update_sentinel_block(ar_path, cards_ar):
        print(f"  updated ar/blog/index.html ({len(sorted_laws)} cards)")
    else:
        print(f"  ar/blog/index.html unchanged")


# =====================================================================
# Main
# =====================================================================

def main() -> int:
    try:
        laws = fetch_all_published()
    except Exception as exc:
        print(f"[ERROR] fetch failed: {exc}", file=sys.stderr)
        return 1

    print(f"Fetched {len(laws)} published laws.")

    out_laws_en = REPO_ROOT / "laws"
    out_laws_ar = REPO_ROOT / "ar" / "laws"
    out_laws_en.mkdir(parents=True, exist_ok=True)
    out_laws_ar.mkdir(parents=True, exist_ok=True)

    for law in laws:
        print(f"  rendering {law['slug']} ({len(law.get('articles', []))} articles)")
        (out_laws_en / f"{law['slug']}.html").write_text(
            render_instrument_page(law, "en"), encoding="utf-8"
        )
        (out_laws_ar / f"{law['slug']}.html").write_text(
            render_instrument_page(law, "ar"), encoding="utf-8"
        )

    (out_laws_en / "index.html").write_text(render_index(laws, "en"), encoding="utf-8")
    (out_laws_ar / "index.html").write_text(render_index(laws, "ar"), encoding="utf-8")
    print(f"Wrote index.html for both EN and AR.")

    print("Maintaining legislation cards in knowledge pages...")
    maintain_knowledge_cards(laws)
    return 0


if __name__ == "__main__":
    sys.exit(main())
