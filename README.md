# Service Matchup — Updated Files (Roofing, Replacement-Intent)

Everything below is a **drop-in replacement** (same filenames as your live site).
⚠️ Per your deploy rule: **upload ALL files to GitHub, not just the changed ones.**

---

## 🌐 LANDING / FUNNEL PAGES (changed)

### `qualify.html` — **/qualify — COST-FIRST, FORM-FIRST FUNNEL (Angi model, multi-market)**
**LIVE (once this branch is on `main`): https://servicematchup.com/qualify** — Cloudflare Pages
serves the root `.html` at the clean URL.

**Faithful port of `reference/roof-price-funnel.html`.** That file is the source of truth for all
copy, layout, colors, and behavior on this route. It **REPLACES** `reference/roof-match-funnel.html`
for /qualify — do not build this page from the roof-match reference. If you change this page, change
the reference too, or the next port silently undoes you. `roof-match.html` is untouched and keeps
its own reference.

**The offer — get this exactly right.** Cost-first: "See what a new roof really runs in {market}."
The visitor answers the quick form → **one honest local roofer comes out and runs the free
23-Point Real-Price Check** (a 23-point inspection at the home) → gives them their real number and
tells them if the roof qualifies for a monthly plan, **as low as $99/mo\*** (with approved credit).
The online form does **not** return a price or an instant qualification. The visit is where the
number comes from, and it is stated above the form (subhead + chip), at the contact step, and on the
button. Never write copy implying an on-screen quote. The button reads **"Set Up My Free Check →"**,
never "get my number/quote". The mechanism name is fixed: **23-Point Real-Price Check**, capitalized
exactly. The copy is ~5th-grade reading level on purpose — do not formalize it.

**Page shape (nothing else belongs here):** logo-only header (no nav, no header CTA) · thin progress
bar under it, 8% filled on load · three-line intro (h1 + one-sentence sub + three trust chips) · the
form, on screen at load · the 3-step "How the 23-Point Real-Price Check works" block · one financing
line · footer disclosures. No testimonials, no FAQ, no reviews, no counts.

**Trust appears at the ask only** — the "Only **one** roofer gets your number" line and the
**One-Roofer Promise** card, plus the three intro chips. Never "never sold or resold."

**FORM = LEADCAPTURE.IO EMBED (funnel `6oeHZT9ts5`)** — same funnel as every other lander, questions
**unchanged**. The reference's demo quiz ships nowhere; it exists only to show flow and copy.

| Deliberate deviation from the reference | Why |
|---|---|
| Demo quiz replaced by the LeadCapture embed | the funnel owns the questions, validation and Lead Prosper → GHL routing |
| The demo quiz's CSS (`.step`, `.field`, `.opt`, `.cta`, `.consent`, `.row2`, `.backbtn`, `#done`) is stripped | those names are generic enough to collide with whatever LeadCapture renders |
| Trust line + Promise card sit under the form, not under the submit button | they live inside the embed's step 6 in the reference; we cannot reach that DOM |
| Card head reads "Free 23-Point Real-Price Check", not "Step 1 of 6" | a step count this page cannot verify would be a false claim; it becomes "Step X of Y" the moment LeadCapture posts real step events |
| Client-side `ipapi.co` fallback removed | reference/demo only — the edge injection in `functions/qualify.js` replaces it (no third-party call, no cost, no latency) |
| Pixel events carry an `event_id`; a CAPI relay posts the same id | that is what makes browser/server dedupe work |

⚠️ **SET THESE INSIDE LEADCAPTURE (dashboard, not code) — the embed's own text is not editable from
this file:**
1. Contact-step title: **"Last step — where should your roofer reach you?"**
2. Contact-step intro, verbatim: *"Here's what happens: one honest local roofer calls to set a time,
   comes out to your home, runs the free 23-Point Real-Price Check, and gives you your real number —
   and tells you if it qualifies for a monthly plan. That's it."*
3. Submit button: **"Set Up My Free Check →"**
4. Auto-advance **ON**; minimum fields (name, phone, ZIP; email optional); TCPA consent at the form.
5. Hidden field **`market`** mapped from the URL param of the same name (see below).
6. Thank-you redirect: keep the query string so `?m=` carries through to the thank-you state.

### MULTI-MARKET + DYNAMIC LOCATION (one template, many metros)
Resolution order, in `qualify.html`:
1. **`?m=slug`** in the URL — explicit override. Every ad URL should still carry its slug
   (`/qualify?m=dfw`).
2. **`window.__GEO`**, injected at the edge by `functions/qualify.js` from `request.cf`
   (country, city, region, postalCode, metroCode = Nielsen DMA, latitude, longitude). No third-party
   lookup, no cost, no toggle.
3. Otherwise **market-agnostic** copy: headline "near you", **no cost figure**.

**The headline and the cost figure are two separate decisions.** Getting this backwards is the easy
mistake:

| | Headline | Cost figure |
|---|---|---|
| US visitor, inside a configured market with a range | their own city — "in Plano, TX" | that market's range — "Most run $12,000–$15,000 in Dallas–Fort Worth" |
| US visitor, anywhere else in the country | their own city — "in Tulsa, OK" | **none** — the no-figure sentence |
| Non-US, or location unknown | "near you" | **none** |

Behavior rules — do not change:
- A visitor resolves to a **market** by DMA `metroCode` first, else by distance to the market centroid
  within `radiusMi`. That match controls the cost figure only.
- The **headline** shows the visitor's own city and 2-letter state anywhere in the USA, market or no
  market. `country` other than `US`, or no city, falls back to "near you".
- A market ships **only** with a real, sourced local cost range. An empty `range` falls back to the
  no-figure sentence. **Houston / Austin / San Antonio are stubs — leave `range: ""` until Jeano
  supplies the figures.** Never show a figure for a metro nobody has sourced.
- ZIP is pre-filled (editable) from `postalCode`.
- `<title>` follows the resolved place, not the market name.

**How the market and the geo reach the lead payload.** The form is LeadCapture's iframe, so this page
cannot write hidden fields into it. It writes them into the parent URL instead
(`history.replaceState`, path stays `/qualify`), named exactly as the payload fields so a hidden field
of the same name maps with no dashboard config:

| Param | Value |
|---|---|
| `m` | resolved market slug — canonical, what the ad URLs carry |
| `market` | same slug, for the hidden field |
| `geo_city` · `geo_state` · `geo_zip` | edge geo, on **every** US visitor, so Lead Prosper can route nationally by geography even with no market match |
| `zip` | the same ZIP again, for LeadCapture's own ZIP prefill |

`window.__MARKET`, `window.__GEO_OUT` and the embed's `data-market` attribute carry the same values.

| Ad URL |
|---|
| `https://servicematchup.com/qualify` (geo-resolved) |
| `https://servicematchup.com/qualify?m=dfw` |
| `https://servicematchup.com/qualify?m=houston` · `?m=austin` · `?m=sanantonio` — **not until their ranges are filled in** |

### CLOUDFLARE PAGES FUNCTIONS (new to this repo)
- **`functions/qualify.js`** — injects `window.__GEO` into `/qualify` from `request.cf`. Only touches
  `text/html` responses on that one route.
- **`functions/api/capi.js`** — Meta Conversions API relay. **Inert until the Pages project has a
  `META_CAPI_TOKEN` environment variable** (Meta system-user token); without it every request returns
  204 and the page runs browser-pixel only. Optional: `META_PIXEL_ID`, `META_TEST_EVENT_CODE`.
  It accepts `PageView` and `InitiateCheckout` only, so a spoofed POST cannot manufacture conversions.
- These are the first Functions in this repo. They are route-scoped — no `_middleware.js` — so **no
  other route changes behavior**. Confirm on the first deploy that Pages picked the directory up and
  that `/roof-match`, `/`, and the service pages still serve normally.

### TRACKING
- Meta pixel **`1605200247372902`** + CAPI, deduped by `event_id`. The retired pixel
  `1315531100000095` appears nowhere.
- `PageView` on load · `InitiateCheckout` **once**, on the first answer inside the embed ·
  **`Lead` is NOT fired by this page.** LeadCapture owns Lead, on its true submission — never on a
  button click (commit `db71ba7`; every other embed lander is `Lead:0` for the same reason).
- Clarity `x1ji8qoqun` present.
- The path stays **/qualify** so Ads Manager reads its Lead events separately from `/roof-match`.
- The progress bar follows LeadCapture step events if the embed posts them (origin-checked
  `postMessage`); otherwise it sits at 8% and goes to 100% on a submit message.

### COMPLIANCE (verbatim — keep intact)
- Financing is always **"as low as $99/mo" + "with approved credit"**. Never a bare "$99/month" —
  it is a TILA/Reg Z trigger term. The footer carries the full disclosure: independent roofer/lender
  terms, not everyone qualifies, Service Matchup is not a lender, no credit pull by us, eligibility
  determined after the inspection.
- Cost figures are labeled typical local ranges and "not a quote; your price is set by the roofer
  after inspecting your roof."
- Free **inspection/Check**, never "free roof" · "**if it qualifies**", never guaranteed · no
  insurance-outcome or deductible-waiver language (TX HB 2102) · matching-service disclaimer in the
  footer · TCPA consent at the form.
- No reviews, ratings or counts anywhere unless real and permissioned. There are none.

⚠️ **BEFORE RUNNING TRAFFIC — could not be verified from the build session**
1. **The LeadCapture embed itself.** `my.leadcapture.io` is blocked from the build sandbox (403 at the
   proxy), so the embed was never rendered here. The script tag, its container and the event wiring
   are confirmed correct; the funnel is not. Load the page and confirm the first question is visible
   without scrolling on a 390×844 viewport.
2. **One test lead end to end:** LeadCapture.io → Lead Prosper → GHL, with `market` on the payload.
3. **Pixel/CAPI in Meta Pixel Helper:** PageView on load, InitiateCheckout on the first answer,
   **Lead only on the true submit**, and each browser event deduped against its CAPI twin.
4. **Edge geo**, four cases (set `window.__GEO` in devtools to fake them):
   DFW → "in Plano, TX" **with** the range · another US metro → "in Tulsa, OK" with **no** figure ·
   non-US → "near you", no figure · ZIP pre-fills in all US cases. Check `geo_city`/`geo_state`/
   `geo_zip` land on the URL each time.
5. Ranges for Houston / Austin / San Antonio before any of those `?m=` URLs runs traffic.

---

### `decide.html` / `decide-rt.html` / `book.html` — **/decide + /decide-rt + /book — BUILT PAGES**

Three pages off one generator. Two run the "file, pay, or wait?" deductible angle for cold and
retargeting traffic; the third is the bottom-funnel booking page for traffic that has already
decided it wants an inspection. Cloudflare Pages serves each at its clean URL the same way it
serves `qualify.html` at `/qualify`.

| File | Path | Traffic |
|---|---|---|
| `decide.html` | `/decide` | Cold prospecting (long form, deductible angle) |
| `decide-rt.html` | `/decide-rt` | Retargeting (short form, deductible angle) |
| `book.html` | `/book` | Most-aware / ready to book (no deductible math) |

**The separate paths are load-bearing** — they are how the ad audiences stay attributable in
Ads Manager and how the LPV custom audiences get split later. Do not collapse them into one route
or serve one as a redirect to another.

All three are **self-contained**: one inline `<style>` block, inline JS, and the logo as a base64 data
URI. That is deliberate and matches this repo — there is no shared stylesheet here (the root
`styles.css` is orphaned; nothing links it) and no layout/partial system. Do not extract the CSS or
the logo.

**Generated, not hand-edited.** `src/build.py` is the source of truth: all three pages share their
CSS, icons, roof diagram, math block, promise/honesty cards, LeadCapture embed, tracking JS, and
footer. Editing one HTML file alone drifts them apart.

```bash
python3 src/build.py          # writes ./decide.html, ./decide-rt.html, ./book.html + src/*.template.html
```

Python 3, no dependencies. The `src/*.template.html` files are the same markup with `__LOGO__` in
place of the base64 logo — useful for diffing without 20KB of base64 noise. They live in `src/` so
they never become routes of their own.

**FORM = LEADCAPTURE.IO EMBED (funnel `6oeHZT9ts5`)** — same funnel and same snippet as every other
embed lander here, emitted for all three pages by `lc_embed()` so they cannot drift onto different
funnels. The script is nested **inside** `<div id="lc-embed">` rather than replacing it:
the embed inserts its `.lc-form-container` as a sibling of the script tag, so nesting keeps the form
inside the container that carries `min-height:400px` and the border radius. Replacing the div would
drop the form into `<section id="check">` and let the card collapse before the embed paints.

### TRACKING (/decide, /decide-rt, /book)
- Meta pixel **`1605200247372902`** (Service Matchup dataset). The retired `1315531100000095`
  appears nowhere.
- `PageView` on load, **once per page**. The LeadCapture funnel has `metaPixelSettings.enabled =
  false`, so the embed loads no second pixel; even if it were enabled, the embed detects an existing
  `fbevents.js` and skips its own init. Two independent guards against a double PageView.
- Custom events — **these exact strings are what ad reporting keys off**:
  `SkipToForm` / `ReachedForm` on `/decide`, `SkipToForm_RT` / `ReachedForm_RT` on `/decide-rt`,
  `SkipToForm_BF` / `ReachedForm_BF` on `/book`. The suffixes keep cold, warm, and bottom-funnel
  behavior separable and let each build its own audience. Both events and the sticky mobile CTA
  bind to the hero CTA's `id="jumpTop"`, so every page body must carry one — the shared JS throws
  without it and takes the sticky observer down with it.
- **`Lead` and `InitiateCheckout` are NOT fired by any of these pages.** LeadCapture owns both on true
  submission (commit `db71ba7`); a duplicate would double-count every conversion.
- Geo: `?m=` param → `window.__GEO` → `ipapi.co` fallback → "Texas". No edge function is wired for
  any of these routes (`functions/qualify.js` is scoped to `/qualify` only), so they use the client-side
  fallback.

### COMPLIANCE (/decide, /decide-rt, /book — verbatim, keep intact)
Same rules as `/qualify`. `/book` carries no deductible math, but it keeps the shared footer and the
"what he will not do" line, and both stay. On `/decide` and `/decide-rt` the deductible copy is presented as **illustrative Texas
wind-and-hail structures**, explicitly "not a statement about your policy". Under **Texas HB 2102**
the homeowner pays the deductible in full, and the pages state that Service Matchup and its partner
roofers **do not waive, rebate, or absorb deductibles**, do not adjust or file claims, and make no
representation about coverage. "as low as $99/mo" always carries the `*` and the "subject to
approved credit" footnote. "Dallas–Fort Worth" is spelled out — never "DFW" in customer-facing copy.
No testimonials, review counts, or star ratings. Do not edit any of it without review.

### `roof-match.html` — **ROOF-MATCHING QUIZ FUNNEL (single page, no redirect)**
**LIVE: https://servicematchup.com/roof-match** (Cloudflare Pages serves the root `.html`
at the clean URL; deploys from `main`).

Ad links — point each ad at its matching angle so the promise and the first screen line up:

| Angle | URL |
|---|---|
| generic | `https://servicematchup.com/roof-match` |
| leak | `https://servicematchup.com/roof-match?angle=leak` |
| storm | `https://servicematchup.com/roof-match?angle=storm` |
| aging roof | `https://servicematchup.com/roof-match?angle=old` |
| insurance claim | `https://servicematchup.com/roof-match?angle=insurance` |

**Faithful PORT of `reference/roof-match-funnel.html` — emotion-led version.** That file is
the source of truth for all copy, layout, sections, colors, and behavior. Above the fold the
port renders **pixel-identical** to the reference at 390px (screenshot hashes match). If you
change this page, change the reference too, or the next port silently undoes you.

This version: emotion/desire-led H1 ("Get the truth about your roof…"), objections moved into
the subhead, the "why now" line, the named mechanisms (**The One-Match Method**, the
**4-Point Pro Check**, the **23-Point Roof Report**), the value-stack checklist, the
**No-Runaround Promise** risk-reversal block, the "just a free look" objection-buster under
the form, and the DFW-city live-activity ticker.
Palette navy `#16324E` / green `#2E8259` / gold `#C4972F`; Plus Jakarta Sans + Inter.

Deliberate deviations from the reference, all of them required:

| Change | Why |
|---|---|
| `LEAD_ENDPOINT` / `CAPI_ENDPOINT` hoisted to a config block at the top of the script | allowed integration wiring |
| Lead payload gains `event_id`, `tcpa_consent`, `landing_page`; `Lead` fires with that `eventID` | lets a server-side CAPI Lead dedupe against the pixel |
| Final-CTA `onclick` InitiateCheckout removed; it now fires **once**, on the first step-1 answer | the reference fired it on every step-1 tap *and* on the CTA; spec says "on form start" |
| "The One-Match Method™" → "The One-Match Method" (no ™) | per the brief: no ™ unless the marks are actually filed. **If they are filed, put it back.** |
| 3 placeholder review cards → 12 real owner-supplied reviews, anonymous attribution | the reference's placeholders were marked "REPLACE WITH REAL" |

**The DFW-city ticker is kept exactly as the reference has it** (Plano, Frisco, Arlington,
McKinney, Fort Worth, Denton, Allen, Rockwall, Garland, Mansfield) per the brief. Wire `TICK`
to real GHL/CRM activity when you can — the format already matches.

⚠️ **KNOWN ISSUES CARRIED OVER FROM THE REFERENCE — not fixed, so the port stays faithful.
Say the word and either is a one-line change:**
1. **"Step 1 of 6" never renders.** `.step{display:none}` (which hides quiz steps) also catches
   `<span class="step" id="stepcount">`. The author's own `.progmeta .step{color:var(--gold)}`
   shows it was meant to be visible in gold. Fix: rename that span's class (e.g. `stepno`) and
   update `.progmeta .step` to match.
2. **No answer options are above the fold at 390px.** The taller hero puts the first option at
   y=831–899 against an 844px viewport — the question shows, the options do not (and real
   browser chrome takes ~90px more). Previous version had 4 of 5 visible. Trimming the hero
   would fix it but would break pixel-fidelity with the reference, so it is your call.

**LEAD CAPTURE = LEADCAPTURE.IO EMBED (funnel `6oeHZT9ts5`)** — same as every other lander.
The native 6-step quiz was **removed** and replaced by the embed inside the hero card, because
the funnel already owns the full question set. Consequences:
- The page fires `PageView` + `InitiateCheckout` only. It must **NOT** fire `Lead` — LeadCapture
  owns that (see commit `db71ba7`, and note every other embed lander has `Lead:0`). Firing it
  here too would double-count every conversion.
- `InitiateCheckout` = "form started", fired **once**, on first interaction with the embed or on
  a CTA that jumps to it. Same convention as `aging-roof.html` / `storm-damage.html`.
- The progress bar was removed from the card head: it cannot reflect LeadCapture's internal
  step state, and a bar frozen at 16% reads as broken. This also retires the hidden-step-counter
  bug noted below.
- `LEAD_ENDPOINT` / `CAPI_ENDPOINT` and the native submit handler are **gone** — routing to
  Lead Prosper → GHL is LeadCapture's job now.
- The quiz answers are no longer collected by this page, so `?angle=` still swaps the
  headline/subhead but no longer pre-highlights a step-1 option (there is no step 1 here).
- **The One-Pro, Never-Sold Guarantee card appears ONCE**, as its own section directly below
  the "Trusted by Over 11,000+ Homeowners" bar. The reference has it twice, but on a real
  phone the two landed ~500px apart and read as a duplicate. The under-form copy was dropped
  on the owner's call — it was cramped there, and out of the card it now renders full width
  (350px vs 308px) with the heading on one line. The two `.microtrust` lines stay under the
  form. Do not re-add the second card when porting a future reference.
- **`.microtrust` was fixed.** `display:flex` made every text fragment and the `<b>one</b>` a
  separate flex item, so "Your info goes to / one / local pro…" rendered as broken columns on
  a phone. Each line's text is now wrapped in a single span. This bug is still in the
  reference — do not port it back in.
- The guarantee card is tightened under 430px, and the activity ticker sits at `bottom:84px`
  on phones so it clears the sticky CTA bar.

**COPY RULES — enforce on every future port**
- Every homeowner-facing mention of the matched professional reads **"one honest local roofer"**
  (or "local roofer/roofers"). Never reintroduce "local pro", "vetted pro", or bare "pro".
  Two exceptions stay: the branded mechanism name **4-Point Pro Check**, and the legal footer's
  "roofing professionals" / "independent professional".
- The guarantee is **The One-Roofer, Never-Sold Guarantee**.
- **$99/month is a TILA/Reg Z trigger term.** It must NEVER appear as a flat "$99/month". Every
  instance carries "as low as", and the financing block carries the disclosure verbatim:
  *"Payments as low as $99/mo with approved credit. Terms are set by the independent roofer and
  their lender and are subject to approval — not everyone qualifies."* The footer repeats it.
  Service Matchup is not the lender. There are currently 4 `$99` mentions and all 4 are hedged.

⚠️ **BEFORE RUNNING TRAFFIC**
0. **Auto-advance in the LeadCapture funnel: ON** (confirmed by the owner).
1. **Verify a test lead reaches Lead Prosper → GHL.** The embed itself is confirmed rendering on
   the live domain.
   It could not be verified from the build session: that sandbox blocks outbound hosts, so
   `my.leadcapture.io` was stubbed in testing. The script tag, its container and the event
   wiring are confirmed correct; the funnel itself is unverified.
2. **Reviews are real** (4 shown, verbatim; the other 8 are parked in an HTML comment beside them) but **anonymous** — no names/cities were supplied, and
   inventing them would be fabrication. Add `<div class="loc">Name, City</div>` back into each
   `.top` block when you have them; the `.rev .loc` CSS is still present.
3. `4.9`, `11,000+`, and "Thousands of roofs checked" are the owner's own figures, confirmed.

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
