#!/usr/bin/env python3
"""Replace old HEADER blocks in blog HTML files with the new NAVBAR."""

import glob
import re

NEW_NAVBAR = '''    <!-- NAVBAR -->
    <nav class="fixed top-0 left-0 right-0 z-40 bg-white/95 backdrop-blur-md py-4 shadow-sm border-b border-gray-100">
      <div class="container mx-auto px-6 md:px-12 flex items-center justify-between">
        <a href="../index.html" class="flex items-center gap-4 relative z-50 group">
            <img src="../images/logo.png" alt="Sahwan Law - Leading Law Firm in Bahrain Since 1975 - Logo" class="h-14 md:h-16 w-auto object-contain">
        </a>
        <div class="hidden lg:flex items-center gap-10">
          <ul class="flex gap-8">
            <li><a href="../index.html" class="text-xs font-sans uppercase tracking-widest text-navy/60 hover:text-navy py-2 relative group">Home<span class="absolute bottom-0 left-0 h-px bg-gold w-0 group-hover:w-full transition-all duration-300"></span></a></li>
            <li><a href="../index.html#services" class="text-xs font-sans uppercase tracking-widest text-navy/60 hover:text-navy py-2 relative group">Services<span class="absolute bottom-0 left-0 h-px bg-gold w-0 group-hover:w-full transition-all duration-300"></span></a></li>
            <li><a href="../index.html#legacy" class="text-xs font-sans uppercase tracking-widest text-navy/60 hover:text-navy py-2 relative group">About<span class="absolute bottom-0 left-0 h-px bg-gold w-0 group-hover:w-full transition-all duration-300"></span></a></li>
            <li><a href="https://sijilat.sahwanlaw.vercel.app/" target="_blank" rel="noopener" class="text-xs font-sans uppercase tracking-widest text-navy/60 hover:text-navy py-2 relative group">Sijilat<span class="absolute bottom-0 left-0 h-px bg-gold w-0 group-hover:w-full transition-all duration-300"></span></a></li>
            <li><a href="../knowledge.html" class="text-xs font-sans uppercase tracking-widest text-navy/60 hover:text-navy py-2 relative group">Knowledge<span class="absolute bottom-0 left-0 h-px bg-gold w-0 group-hover:w-full transition-all duration-300"></span></a></li>
            <li><a href="../index.html#contact" class="text-xs font-sans uppercase tracking-widest text-navy/60 hover:text-navy py-2 relative group">Careers<span class="absolute bottom-0 left-0 h-px bg-gold w-0 group-hover:w-full transition-all duration-300"></span></a></li>
          </ul>
          <div class="flex items-center gap-4">
            <a href="https://sas-team.vercel.app" target="_blank" rel="noopener" class="text-navy/30 hover:text-gold transition-colors duration-300" title="Staff Portal">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
            </a>
            <a href="../index.html#contact" class="text-[10px] font-bold uppercase tracking-[0.2em] px-6 py-3 bg-navy text-white hover:bg-gold transition-colors duration-300">Contact</a>
            <a href="../ar/blog/" class="text-[10px] font-medium uppercase tracking-[0.2em] px-3 py-2 border border-navy/20 text-navy/60 hover:text-gold hover:border-gold transition-colors duration-300">\u0627\u0644\u0639\u0631\u0628\u064a\u0629</a>
          </div>
        </div>

        <!-- Mobile: Language Toggle + Hamburger -->
        <div class="flex items-center gap-4 lg:hidden">
          <a href="../ar/blog/" class="text-[10px] font-bold uppercase tracking-widest text-navy hover:text-gold border border-navy/20 px-2 py-1 rounded">AR</a>
          <button id="mobile-menu-btn" class="text-navy focus:outline-none" aria-label="Open Menu">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile Menu Dropdown -->
      <div id="mobile-menu" class="hidden lg:hidden bg-white border-t border-gray-100 absolute w-full inset-x-0 top-full shadow-lg">
        <ul class="flex flex-col p-6 space-y-4">
          <li><a href="../index.html" class="block text-sm font-medium text-navy/60 hover:text-navy">Home</a></li>
          <li><a href="../index.html#services" class="block text-sm font-medium text-navy/60 hover:text-navy">Services</a></li>
          <li><a href="../index.html#legacy" class="block text-sm font-medium text-navy/60 hover:text-navy">About Us</a></li>
          <li><a href="https://sijilat.sahwanlaw.vercel.app/" target="_blank" rel="noopener" class="block text-sm font-medium text-navy/60 hover:text-navy">Sijilat</a></li>
          <li><a href="../knowledge.html" class="block text-sm font-medium text-navy/60 hover:text-navy">Knowledge</a></li>
          <li><a href="../index.html#contact" class="block text-sm font-medium text-navy/60 hover:text-navy">Contact</a></li>
        </ul>
      </div>
    </nav>

    <script>
      const mBtn = document.getElementById('mobile-menu-btn');
      const mMenu = document.getElementById('mobile-menu');
      mBtn.addEventListener('click', () => { mMenu.classList.toggle('hidden'); });
    </script>'''

# Pattern: match from "<!-- HEADER -->" through the closing "</header>" tag
PATTERN = re.compile(
    r'[ \t]*<!-- HEADER -->.*?</header>',
    re.DOTALL
)

files = sorted(glob.glob('/tmp/sahwanlaw/blog/*.html'))
updated = []
skipped = []

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content, count = PATTERN.subn(NEW_NAVBAR, content)

    if count > 0:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        updated.append(fpath)
        print(f"  UPDATED: {fpath}")
    else:
        skipped.append(fpath)
        print(f"  SKIPPED (no match): {fpath}")

print(f"\nDone. {len(updated)} files updated, {len(skipped)} files skipped.")
