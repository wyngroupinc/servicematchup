# Service Matchup — Updated Files (Roofing, Replacement-Intent)

Everything below is a **drop-in replacement** (same filenames as your live site).
⚠️ Per your deploy rule: **upload ALL files to GitHub, not just the changed ones.**

---

## 🌐 LANDING / FUNNEL PAGES (changed)

### `roof-match.html` — **ROOF-MATCHING QUIZ FUNNEL (single page, no redirect)**
Route: **`/roof-match`** (Cloudflare Pages serves the `.html` at the clean URL).
Collapses the old `roofing-lander → get-started` two-page hop — that hop leaks
conversions, so the multi-step quiz lives **on the page, above the fold**.

**This is a faithful PORT of `reference/roof-match-funnel.html`, not a redesign.**
That reference file is the source of truth for all copy, layout, sections, colors,
and behavior. Above the fold it renders **pixel-identical** to the reference at
390px (verified by screenshot hash). If you change this page, change the reference
too — or the next port will silently undo you.

The only deliberate deviations from the reference, all of them required:

| Change | Why |
|---|---|
| `LEAD_ENDPOINT` / `CAPI_ENDPOINT` hoisted to a config block at the top of the script | allowed integration wiring |
| Lead payload gains `event_id`, `tcpa_consent`, `landing_page`; `Lead` fires with that `eventID` | lets a server-side CAPI Lead dedupe against the pixel |
| Final-CTA `onclick="fbq('track','InitiateCheckout')"` removed; `InitiateCheckout` now fires once, on the first step-1 answer | the reference double-fired it; spec says "on form start" |
| Review placeholders say `[City], [State]`, not `[City], TX`; phone/ZIP placeholders no longer Dallas-specific | geo-neutral is a hard rule |
| Trust badge read `local Local` → `Local Pros Near You` | find/replace artifact in the reference |
| `TICK` ticker array ships **empty** (reference strings preserved, commented) | "No fabricated reviews/stats/activity" — the reference's own comment says the same; the popup removes itself until real data is wired |
| 3 placeholder review cards → 12 real owner-supplied reviews, anonymous attribution | the reference's placeholders were explicitly marked "REPLACE WITH REAL" |

⚠️ **BEFORE RUNNING TRAFFIC**
1. `LEAD_ENDPOINT` — the Lead Prosper posting URL. **Ships empty = preview mode**: the
   quiz runs and shows the success state but posts nothing, so the page is safe to
   deploy now. Fill it in, then send one real test lead and confirm Lead Prosper → GHL
   → the follow-up sequence actually fires. (Still untested end to end.)
2. **Reviews are REAL** — 12 owner-supplied homeowner reviews, quotes verbatim, replacing
   the reference's 3 placeholders. Attribution is deliberately anonymous
   ("Verified homeowner") because no reviewer **names or cities** were supplied, and
   inventing them would be fabrication. If you have names/cities, add
   `<div class="loc">Name, City</div>` back into each `.top` block — the `.rev .loc`
   CSS rule is still there, so it's a pure markup edit. Named reviews convert better
   than anonymous ones, so this is worth doing.
3. **Verify the `4.9` rating and the `2,300+` counts** in the header, proof band, and
   reviews lead — they're carried over from the reference and are still on the
   "verify your stats" open item below.
4. `TICK` — uncomment/wire to real recent requests from GHL/CRM if you want the ticker.

### `servicematchup-roofing-lander.html` — PRIMARY landing page (Variant A)
- Headline: **"Your Roof Looks Fine. That's Exactly the Problem."**
- Full conversion rewrite (Schwartz + Hormozi $100M Offers/Leads/Money Models)
- Reoriented toward **roof replacement** intent (filters out small-repair shoppers)
- Headings now **Manrope bold** (matching the green accent), no serif
- Meta Pixel `1605200247372902` (PageView). Compliant — no "free roof / insurance pays / you qualify."
- **Point your main ads here.** (Superseded for quiz-funnel traffic by `roof-match.html`.)

### `servicematchup-roofing-lander-b.html` — A/B TEST variant (Variant B)
- Identical page, different headline: **"Is Your Roof One Storm From Failing?"** + matched subhead
- Use to split-test headline mindset. Point a duplicate ad set here, split budget 50/50.
- Judge by **cost-per-qualified-lead + close rate**, NOT raw CPL.

### `servicematchup-form.html` — Lead form page
- Headline: "Find Out If Your Roof Needs Replacing"
- NEW: reassurance bar above the form (Free · 90 Seconds · No Obligation) to cut abandonment
- Meta Pixel PageView only (correct for mid-funnel). TCPA + TrustedForm/Jornaya intact.
- ⚠️ The actual form QUESTIONS live in LeadCapture.io (funnel `6oeHZT9ts5`), NOT this file — see the spec below.

### `thank-you.html` — Confirmation page
- Pixel ID corrected to `1605200247372902` + `Lead` event fires here
- Headings → Manrope. Already has a strong "answer the call from a local number" section (drives lead→contact rate) — left as-is.

### `call-now.html` — Pay-per-call page
- FIXED: buttons no longer overflow the card (added `box-sizing:border-box`, trimmed glow)
- Headings → Manrope. Meta Pixel added.
- ⚠️ STILL TODO (compliance): this page has invented scarcity ("14:59 expires," "3 slots left") + a claim-timing line. Recommend a compliance pass before sending FB traffic here.

---

## 📄 REFERENCE DOCS

### `leadcapture-form-spec-replacement.md` — **BUILD THIS IN LEADCAPTURE.IO**
The two-tier qualification logic that makes the whole replacement-intent strategy work:
- Hard floor: renters + sub-5-yr roofs → disqualify
- Roof age = the filter (fail fast); scope = a tier tag, never a hard kill
- Tier A (replacement-ready) fires the `Lead` pixel; Tier B does not
- **This is the single most important piece for lead quality + low cost-per-qualified-lead.**

### `static-image-ads-aggressive.md` — 8 aggressive, compliant FB static ad concepts
(Also lives in the ClickUp campaign doc.)

### `servicematchup-roofing-copy.md` — Original full copy + Meta ads package (earlier deliverable)

---

## ✅ WHAT'S DONE vs ⏳ WHAT'S LEFT

DONE:
- Compliance pass (lander, form, thank-you)
- Replacement-intent restructure (lander + form copy)
- Conversion rewrite + A/B headline variant
- Font fixes (Manrope headings), call-now button fix
- ClickUp campaign doc (strategy, ad sets, UGC scripts, podcasts, statics, b-roll)

LEFT (when you're ready):
1. Build the LeadCapture.io two-tier logic (use the spec)
2. Compliance pass on `call-now.html` (fake scarcity + claim timing)
3. Campaign restructure finish: ad sets (drop leak angle, add "Roof at End of Life") + strategy doc two-tier model
4. Set up CAPI alongside the pixel (target EMQ ≥ 7)
5. Verify your stats/testimonials are real before running (4.9★, 11,000+, named reviews)

— Not legal advice; have counsel review final wording given Texas HB 2102.
