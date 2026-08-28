# Service Matchup — Updated Files (Roofing, Replacement-Intent)

Everything below is a **drop-in replacement** (same filenames as your live site).
⚠️ Per your deploy rule: **upload ALL files to GitHub, not just the changed ones.**

---

## 🌐 LANDING / FUNNEL PAGES (changed)

### `roof-match.html` — **ROOF-MATCHING QUIZ FUNNEL (single page, no redirect)**
Route: **`/roof-match`** (Cloudflare Pages serves the `.html` at the clean URL). Live on `main`.

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

⚠️ **BEFORE RUNNING TRAFFIC**
1. **Verify the embed renders on the live domain and that a test lead reaches Lead Prosper → GHL.**
   It could not be verified from the build session: that sandbox blocks outbound hosts, so
   `my.leadcapture.io` was stubbed in testing. The script tag, its container and the event
   wiring are confirmed correct; the funnel itself is unverified.
2. **Reviews are real** (12, verbatim) but **anonymous** — no names/cities were supplied, and
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
