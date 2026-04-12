# Sahwan Law — SEO Playbook

**Owner:** Abdulla Sahwan, Principal Partner
**Last updated:** 2026-04-12

This runbook captures the SEO / AEO (Answer Engine Optimization) actions that cannot be performed from the repository — they require logged-in access to Google, LinkedIn, directory sites, or direct outreach. Work through them in order. Each section ends with a "done?" line so this file can be reused as a checklist.

---

## 0. Prerequisites

You need, before anything below works:

- [ ] **Google account** that owns / can manage `sahwanlaw.com`
- [ ] **Admin access** to DNS for `sahwanlaw.com` (for verification records)
- [ ] **Verified email** at `@sahwanlaw.com` for directory submissions

---

## 1. Google Search Console (GSC) — **highest priority**

Without GSC you cannot (i) see what Google has indexed, (ii) remove stale URLs, (iii) monitor ranking queries, (iv) submit fresh content for crawl, (v) receive manual-penalty notices.

### 1.1 Verify the property

1. Go to https://search.google.com/search-console
2. Click **Add property** → choose **Domain** (not URL-prefix) → enter `sahwanlaw.com`
3. Google shows a TXT record — add it to the `sahwanlaw.com` DNS zone (wherever the domain is managed)
4. Wait 5–10 minutes, click **Verify**

### 1.2 Submit the sitemap

1. Left menu → **Sitemaps**
2. Submit: `https://www.sahwanlaw.com/sitemap.xml`
3. Submit: `https://www.sahwanlaw.com/feed.xml` (GSC accepts Atom feeds too — gives crawlers a second discovery path)
4. Wait 24–72 hours; you should see "Success" with discovered URL count matching the 28 URLs in the sitemap

### 1.3 Remove stale / placeholder URLs

The `site:sahwanlaw.com` query currently returns legacy Webflow-era URLs that no longer exist. Each now has a `meta-refresh` redirect in the repo (pushed 2026-04-12), but GSC can be asked to *expedite* removal:

1. Left menu → **Removals** → **New request** → **Temporarily remove URL**
2. Submit each of these one-by-one:
   - `https://www.sahwanlaw.com/cases`
   - `https://sahwanlaw.com/home/`
   - `https://www.sahwanlaw.com/lawyer/melissa-mills`
   - `https://www.sahwanlaw.com/lawyer/john-castillo`
   - `https://www.sahwanlaw.com/case/wrongful-death`
   - `https://www.sahwanlaw.com/post/understanding-the-recent-changes-in-social-insurance-contributions-in-bahrain`
   - `https://www.sahwanlaw.com/post/the-amicable-compositeur-in-bahraini-arbitration-law-the-flexibility-of-justice-in-a-global-framewor`
3. Temporary removal lasts ~6 months; during that window, Google should re-crawl, see the canonical redirect, and drop the stale entries permanently

### 1.4 Request indexing of key pages

For any important page not yet indexed (or that changed substantially):

1. Top search bar → paste full URL → **Enter**
2. **Request Indexing** (if button is live; rate-limited to ~10/day)
3. Prioritise: homepage, `/knowledge.html`, each newly published article

- [ ] GSC property verified
- [ ] Sitemap + feed submitted
- [ ] Stale URL removal requests filed
- [ ] Key pages requested for indexing

---

## 2. Google Business Profile (GBP) — critical for local search

Bahraini users searching "law firm near me" or "محامي في المنامة" will see the Google Maps pack before organic results. Without a GBP, you are invisible in that space.

### 2.1 Claim / create the profile

1. https://www.google.com/business → **Manage now**
2. Sign in with the same Google account used for GSC
3. Search for **Sahwan Law** in Manama. If a listing exists (auto-generated from public sources), **claim** it. Otherwise **add** it.
4. Name: `Salman A. Sahwan - Attorneys & Legal Consultants`
5. Category primary: **Law firm**. Secondary: **Legal services**, **Corporate office**
6. Address: Wind Tower, Building 403, Road 1705, Diplomatic Area, Manama, Bahrain
7. Service area: Kingdom of Bahrain (+ optional: Saudi Arabia, UAE, Kuwait, Qatar, Oman if you serve clients cross-border)
8. Phone: +973 17 531 566
9. Website: https://www.sahwanlaw.com
10. Hours: Sun–Thu 08:00–17:00 (Bahrain weekend Fri/Sat)
11. Verify (postcard or phone verification — Google will send a code)

### 2.2 Fill the profile

- [ ] Add 5–10 photos: office exterior, reception, conference room, legal library, team (no low-res phone pics — daylight, wide-angle)
- [ ] Write a 750-char description that naturally includes your core keywords (Bahrain law firm, commercial law, corporate law, arbitration, notary, sijilat) without keyword-stuffing
- [ ] List services: Corporate Law, Litigation, Arbitration, Notarization, Sijilat Registration, Debt Collection, Banking & Finance, Real Estate, Owners' Associations, Employment Law
- [ ] Enable messaging (optional — if you want inbound client chats via the Maps listing)

### 2.3 Reviews — the flywheel

Google ranks local businesses heavily on review quantity + quality + recency.

- [ ] Identify 10–15 satisfied clients who would leave an honest review. Email them a direct link (Google gives you a short URL under **Get more reviews** in the GBP dashboard). Target: 1–2 new reviews per month, sustained.
- [ ] Respond to **every** review within 48 hours — positive and negative. Google weights "owner responsiveness" in ranking.

- [ ] GBP claimed & verified
- [ ] Profile filled (services, hours, photos, description)
- [ ] First 5 reviews solicited

---

## 3. Directory submissions — backlink foundation

Competitor firms (Al Tamimi, Zu'bi, Hassan Radhi, ASAR, Al Doseri) rank well partly because they have decades of authoritative backlinks. Catch up by submitting to the directories Google treats as authoritative for the Bahraini legal market.

Priority order:

### 3.1 Tier-1 (do first)

| Directory | URL | Action |
|---|---|---|
| **Legal 500 — Bahrain** | https://www.legal500.com/c/bahrain/ | Submit firm profile. Editorial review required; publish cycle is annual. Apply for ranking in at least: Commercial/Corporate/M&A, Dispute Resolution, Banking & Finance, Real Estate. |
| **Chambers & Partners — Global / Middle East** | https://chambers.com/about-us/submissions | Submit during the annual research window. Chambers rankings carry significant authority signal. |
| **Bahrain Bar Society Directory** | Check directly with the Society | Ensure firm is listed with current address + Abdulla Sahwan as Principal Partner. |

### 3.2 Tier-2 (thought-leadership syndication)

| Platform | URL | Action |
|---|---|---|
| **Mondaq — Bahrain author** | https://www.mondaq.com/ | Apply as a contributor. Syndicate our blog articles. Every Mondaq article carries a backlink and gets indexed in high-authority law databases. |
| **Lexology — Bahrain contributor** | https://www.lexology.com/contributors | Same model as Mondaq. Frequently top-of-page for GCC legal queries. |
| **HG.org** | https://www.hg.org/ | Already listed (Salman Abdulla Sahwan profile) — update to reflect current firm, address, Abdulla as Principal Partner. |

### 3.3 Tier-3 (local presence)

| Platform | URL | Action |
|---|---|---|
| **GDN Online / Daily Tribune / News of Bahrain** | Respective sites | When publishing a law-in-the-news piece, pitch it as a guest column. Local-press backlinks are Google-authoritative. |
| **LinkedIn Company Page** | https://www.linkedin.com/company/sahwan-law | Post every new blog article with a summary. LinkedIn posts are indexed by Google; high engagement → signal. |

- [ ] Legal 500 submission sent
- [ ] Chambers & Partners submission sent
- [ ] Mondaq contributor application submitted
- [ ] Lexology contributor application submitted
- [ ] HG.org profile updated
- [ ] LinkedIn company page posting cadence established

---

## 4. Content strategy (ongoing)

### 4.1 Publishing cadence

Aim for **one article per month minimum**. Google rewards freshness; AI crawlers re-sample sites with fresh content more often. Months of silence between posts is the single biggest self-inflicted ranking wound.

Suggested topics aligned with AEO (questions clients actually ask AI search):

- "How do I file a debt claim in Bahrain?"
- "What is the minimum capital for a WLL in Bahrain?"
- "How is a foreign judgment enforced in Bahrain?"
- "What is the cheque bounce penalty in Bahrain?" (cross-links existing `cheque-regulations-law-23-2025.html`)
- "How long does an arbitration take at BCDR?"
- "What is the notarization fee in Bahrain?"
- "How do I contest a CR rejection on Sijilat?"

### 4.2 Arabic-first is the moat

Per the existing content strategy: most Bahraini legal content on the web is in English. AI systems are starved for authoritative Arabic GCC legal content. Every English article should have an Arabic mirror (as we've now done for `force-majeure-bahrain-practitioners-framework`).

### 4.3 Internal linking

Every article should link to ≥ 3 others — both pillar guides and related articles. Google uses internal links to understand topical authority.

- [ ] Publishing cadence committed (target: 1 article / month)
- [ ] Arabic mirror created for every English article
- [ ] Internal linking audit on existing articles

---

## 5. Technical / on-repo (automation)

### 5.1 Before every new article commit

Run:

```bash
python build_syndication.py
```

This regenerates `sitemap.xml` and `feed.xml` from the canonical article list in `knowledge.html`. Commit both alongside the new article so they're in sync.

### 5.2 After the commit lands in production

- [ ] Open the new article URL in GSC → **Request Indexing**
- [ ] Post the article on LinkedIn with a 2-line teaser + link
- [ ] Submit the article text to Mondaq / Lexology (if contributor status granted)

### 5.3 Monthly review

- [ ] Check GSC **Performance** → note top queries, CTR, avg position; identify which articles are ranking and which aren't
- [ ] Check GBP **Insights** → note how many users found you via Maps vs Search; respond to any new reviews
- [ ] Check GSC **Coverage** → resolve any new indexing errors or invalid URLs

---

## 6. What to avoid

- ❌ **Paid link schemes.** Any service offering "100 Bahraini legal backlinks for $99" will damage your domain long-term.
- ❌ **Fake reviews.** Google detects volume/velocity anomalies and penalizes. We removed the unverified `aggregateRating` from the homepage schema on 2026-04-12 for this reason.
- ❌ **Keyword-stuffed meta descriptions.** Write for humans; Google models are sophisticated enough to penalize stuffing.
- ❌ **Duplicate content between English and Arabic without proper hreflang.** We have hreflang set correctly now; preserve the pattern for every new article pair.
- ❌ **Publishing on sensitive current-affairs topics** without brand-discipline framing (see internal `feedback_drafting_in_terminal.md` memory and the `force-majeure` rescope conversation of 2026-04-12).

---

## 7. Escalation / resources

- **Google Search Console help** — https://support.google.com/webmasters
- **Google Business Profile help** — https://support.google.com/business
- **Schema.org structured-data validator** — https://validator.schema.org/
- **Google Rich Results Test** — https://search.google.com/test/rich-results
- **PageSpeed Insights** — https://pagespeed.web.dev/

---

*This playbook is a living document. Update it after each SEO milestone, or whenever a new directory / AI-citation surface becomes relevant to the Bahraini legal market.*
