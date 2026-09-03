#!/usr/bin/env python3
"""Builds the two deductible-angle pages (long + short) from shared design + copy blocks."""
import os, re

LOGO = open(os.environ.get('LOGO_FILE', './src/logo_uri.txt')).read().strip()
# Deployed pages live at the repo root: Cloudflare Pages serves `decide.html` at /decide,
# the same way it serves qualify.html at /qualify. The __LOGO__ templates stay under src/
# so they never become routes of their own.
OUT = os.environ.get('OUT_DIR', '.')
TPL_OUT = os.environ.get('TPL_DIR', './src')

CSS = r"""
:root{--bg:#F8F4EC;--soft:#FFFDF9;--line:#E9E4DA;--navy:#16324E;--navy2:#0F2439;--green:#2E8259;
--green-dk:#246B48;--muted:#5C6B7A;--gold:#D4A853;--warn:#B5541F;--r:16px}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html{-webkit-text-size-adjust:100%}
html,body{margin:0;padding:0}
body{background:var(--bg);color:var(--navy);line-height:1.55;font-size:16px;
font-family:'Poppins',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
padding-bottom:calc(84px + env(safe-area-inset-bottom))}
img{max-width:100%}
.wrap{max-width:640px;margin:0 auto;padding:0 18px}

/* header */
.top{background:var(--soft);border-bottom:1px solid var(--line)}
.top .wrap{display:flex;align-items:center;justify-content:space-between;height:56px}
.logo{height:30px;width:auto;display:block}
.top .loc{font-size:12px;color:var(--muted);display:flex;align-items:center;gap:5px;white-space:nowrap}
.top .loc .dot{width:7px;height:7px;border-radius:50%;background:var(--green);box-shadow:0 0 0 3px rgba(46,130,89,.18)}

/* hero */
.hero{position:relative;margin:14px 0 0;border-radius:20px;overflow:hidden;
background:#fff;color:var(--navy);border:1px solid var(--line);
padding:26px 20px 22px;box-shadow:0 10px 30px rgba(22,50,78,.07)}
.hero:before{content:"";position:absolute;inset:0;background:
radial-gradient(circle at 100% 0%,rgba(46,130,89,.10),transparent 40%);pointer-events:none}
.hero:after{content:"";position:absolute;left:0;right:0;top:0;height:6px;background:var(--green)}
.hero>*{position:relative}
.eyebrow{display:inline-flex;align-items:center;gap:7px;font-size:11.5px;font-weight:700;letter-spacing:.6px;
text-transform:uppercase;color:var(--green-dk);background:#EEF6F1;border:1px solid #CFE5D8;
border-radius:999px;padding:6px 11px;margin:0 0 14px}
.eyebrow svg{width:14px;height:14px}
h1{font-size:27px;line-height:1.2;font-weight:700;margin:0 0 12px;text-wrap:balance;letter-spacing:-.2px}
h1 .ac{color:var(--green)}
.hero .sub{font-size:15.5px;line-height:1.55;color:var(--muted);margin:0 0 18px}
.hero .sub b{color:var(--navy);font-weight:600}
.btn{display:flex;align-items:center;justify-content:center;gap:9px;width:100%;min-height:54px;
background:var(--green);color:#fff;text-decoration:none;font-weight:700;font-size:17px;
padding:14px 16px;border-radius:14px;box-shadow:0 5px 0 var(--green-dk);border:0;cursor:pointer}
.btn:active{transform:translateY(3px);box-shadow:0 2px 0 var(--green-dk)}
.btn.gold{background:var(--green);color:#fff;box-shadow:0 5px 0 var(--green-dk)}
.btn.gold:active{box-shadow:0 2px 0 var(--green-dk)}
.hero .note{font-size:12.5px;color:var(--muted);text-align:center;margin:10px 0 0}

/* trust strip */
.trust{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin:14px 0 0}
.trust div{display:flex;align-items:center;gap:8px;background:var(--soft);border:1px solid var(--line);
border-radius:12px;padding:10px 12px;font-size:12.5px;font-weight:600;color:var(--navy)}
.trust svg{width:18px;height:18px;flex:none;color:var(--green)}

/* sections */
section.s{margin:34px 0 0}
.kick{font-size:11.5px;font-weight:700;letter-spacing:.7px;text-transform:uppercase;color:var(--green);margin:0 0 8px}
h2{font-size:22px;font-weight:700;margin:0 0 10px;line-height:1.25;letter-spacing:-.2px;text-wrap:balance}
p{font-size:16px;margin:0 0 13px}
.lede{font-size:17px;font-weight:500}
p b{font-weight:700}

/* three bad paths */
.paths{display:grid;gap:10px;margin:14px 0 0}
.path{background:var(--soft);border:1px solid var(--line);border-radius:14px;padding:14px 14px 14px 16px;
display:flex;gap:12px;align-items:flex-start}
.path .ic{width:38px;height:38px;border-radius:11px;flex:none;display:flex;align-items:center;justify-content:center;
background:#EEF6F1;color:var(--green-dk)}
.path .ic svg{width:20px;height:20px}
.path b{display:block;font-size:15.5px;margin-bottom:3px}
.path span{font-size:14.5px;color:var(--muted);line-height:1.5}

/* math */
.math{background:#EEF6F1;color:var(--navy);border:1px solid #CFE5D8;border-radius:18px;padding:18px 18px 16px;
margin:16px 0 0}
.math .row{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:12px 0;
border-bottom:1px solid #CFE5D8;font-size:15px}
.math .row span{flex:1;line-height:1.35}
.math .row b{font-size:18px;white-space:nowrap;flex:none}
.math .row .q{width:40px;height:40px;border-radius:50%;background:#fff;border:2px dashed var(--green);
color:var(--green);display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:800}
.math .row span.known{flex:none;background:#fff;border:1px solid #CFE5D8;color:var(--green-dk);border-radius:999px;padding:6px 12px;font-size:13px;font-weight:600}
.math .row.eq{border-bottom:0;padding-top:14px;position:relative}
.math .row.eq:before{content:"=";position:absolute;left:0;top:-12px;background:var(--green);color:#fff;
font-weight:800;font-size:13px;width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center}
.math .note{font-size:13px;line-height:1.5;color:var(--muted);margin:12px 0 0;padding-top:12px;
border-top:1px solid #CFE5D8}

/* diagram + three factors */
.diagram{background:var(--soft);border:1px solid var(--line);border-radius:18px;padding:14px 14px 6px;margin:14px 0 0}
.diagram svg{width:100%;height:auto;display:block}
.three{list-style:none;padding:0;margin:14px 0 0;display:grid;gap:10px}
.three li{background:var(--soft);border:1px solid var(--line);border-radius:14px;padding:14px;display:flex;gap:12px}
.three .n{width:34px;height:34px;border-radius:50%;background:var(--green);color:#fff;flex:none;
display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:800}
.three b{display:block;font-size:15.5px;margin-bottom:3px;line-height:1.3}
.three span{font-size:14.5px;color:var(--muted);line-height:1.5}
.pull{background:var(--soft);border:1px solid var(--line);border-left:4px solid var(--green);
border-radius:14px;padding:16px 18px;margin:16px 0 0;font-size:16.5px;font-weight:600;line-height:1.45}

/* offer */
.what{background:var(--soft);border:1px solid var(--line);border-radius:18px;padding:16px 16px 6px;margin:14px 0 0}
.what h3{margin:0 0 10px;font-size:16px}
.what ul{list-style:none;margin:0;padding:0}
.what li{display:flex;gap:10px;font-size:15px;color:var(--muted);margin:0 0 11px;line-height:1.5}
.what li b{color:var(--navy)}
.what li svg{width:20px;height:20px;flex:none;color:var(--green);margin-top:2px}

.honest{background:#fff;border:1px solid var(--line);border-radius:16px;padding:16px;margin:14px 0 0;display:flex;gap:12px}
.honest .ic{width:36px;height:36px;border-radius:10px;background:#F1EDE4;color:var(--navy);flex:none;
display:flex;align-items:center;justify-content:center}
.honest .ic svg{width:20px;height:20px}
.honest b{display:block;font-size:15.5px;margin-bottom:5px}
.honest p{font-size:14.5px;color:var(--muted);margin:0 0 8px;line-height:1.5}
.honest p:last-child{margin:0}

.promise{background:#EEF6F1;border:1px solid #CFE5D8;color:var(--navy);border-radius:16px;padding:16px;margin:14px 0 0;display:flex;gap:12px}
.promise .ic{width:36px;height:36px;border-radius:10px;background:var(--green);color:#fff;flex:none;
display:flex;align-items:center;justify-content:center}
.promise .ic svg{width:20px;height:20px}
.promise b{display:block;font-size:15.5px;margin-bottom:5px}
.promise span{font-size:14.5px;color:var(--muted);line-height:1.5}

/* form */
#check{scroll-margin-top:12px;margin:30px 0 0}
.formcard{background:var(--soft);border:1px solid var(--line);border-top:5px solid var(--green);border-radius:18px;
padding:20px 18px;box-shadow:0 12px 30px rgba(22,50,78,.08)}
.formcard h2{font-size:22px;margin:0 0 4px}
.formcard .fsub{font-size:14.5px;color:var(--muted);margin:0 0 14px}
#lc-embed{min-height:400px;border-radius:12px}
.chips{display:flex;flex-wrap:wrap;gap:7px;margin:14px 0 0}
.chip{display:inline-flex;align-items:center;gap:5px;font-size:12.5px;font-weight:600;color:var(--navy);
background:var(--bg);border:1px solid var(--line);border-radius:999px;padding:7px 11px}
.chip svg{width:14px;height:14px;color:var(--green)}

/* how */
.how ol{list-style:none;padding:0;margin:12px 0 0;display:grid;gap:8px}
.how li{display:flex;gap:12px;align-items:flex-start;font-size:14.5px;color:var(--muted);line-height:1.5}
.how li .n{width:28px;height:28px;border-radius:50%;background:var(--green);color:#fff;flex:none;
display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:800;margin-top:1px}
.how li b{display:block;color:var(--navy);font-size:15px}

footer{font-size:11.5px;color:#8A97A3;line-height:1.6;margin:30px 0 0;padding:18px 0 10px;border-top:1px solid var(--line)}

/* sticky mobile CTA */
.sticky{position:fixed;left:0;right:0;bottom:0;z-index:50;background:rgba(255,253,249,.96);
backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border-top:1px solid var(--line);
padding:10px 16px calc(10px + env(safe-area-inset-bottom));transform:translateY(110%);transition:transform .25s ease}
.sticky.on{transform:translateY(0)}
.sticky .btn{min-height:50px;font-size:16px;box-shadow:0 4px 0 var(--green-dk)}
.sticky .btn small{font-weight:500;opacity:.85;font-size:12.5px}

@media(min-width:640px){
  h1{font-size:36px}h2{font-size:26px}.hero{padding:34px 32px 28px}
  .trust{grid-template-columns:repeat(4,1fr)}
  .three{grid-template-columns:1fr}
  body{padding-bottom:0}.sticky{display:none}
}
"""

ICONS = {
 'check':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>',
 'shield':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>',
 'home':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 11 9-8 9 8"/><path d="M5 10v10h14V10"/></svg>',
 'nodoor':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="3" width="12" height="18" rx="1"/><circle cx="14.5" cy="12" r="1"/><path d="m3 3 18 18"/></svg>',
 'lock':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>',
 'file':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M9 13h6M9 17h6"/></svg>',
 'dollar':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20"/><path d="M17 6.5c0-1.9-2.2-3-5-3s-5 1.1-5 3 2.2 3 5 3 5 1.1 5 3-2.2 3.5-5 3.5-5-1.6-5-3.5"/></svg>',
 'clock':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
 'alert':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/></svg>',
}

# roof cross-section diagram with 3 callouts
DIAGRAM = """<svg viewBox="0 0 600 270" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Roof cross-section: 1 real size, 2 pitch and layers, 3 decking">
<rect width="600" height="270" fill="#F8F4EC" rx="12"/>
<rect x="150" y="160" width="300" height="90" fill="#FFFDF9" stroke="#E9E4DA" stroke-width="2"/>
<rect x="272" y="192" width="44" height="58" fill="#16324E" opacity=".85"/>
<rect x="188" y="186" width="46" height="34" fill="#DDE6EE" stroke="#16324E" stroke-width="1.5"/>
<rect x="366" y="186" width="46" height="34" fill="#DDE6EE" stroke="#16324E" stroke-width="1.5"/>
<polygon points="104,162 300,46 496,162 472,162 300,60 128,162" fill="#B5541F" opacity=".6"/>
<polygon points="114,154 300,38 486,154 466,154 300,53 134,154" fill="#8A97A3"/>
<polygon points="124,146 300,30 476,146 456,146 300,46 144,146" fill="#3D5568"/>
<g stroke="#F8F4EC" stroke-width="1.4" opacity=".55">
<line x1="184" y1="110" x2="204" y2="110"/><line x1="226" y1="82" x2="246" y2="82"/><line x1="268" y1="56" x2="288" y2="56"/>
<line x1="396" y1="110" x2="416" y2="110"/><line x1="354" y1="82" x2="374" y2="82"/><line x1="312" y1="56" x2="332" y2="56"/>
</g>
<g stroke="#2E8259" stroke-width="3" fill="none" stroke-linecap="round">
<line x1="112" y1="128" x2="286" y2="20"/><path d="M112 128 l12 -2 M112 128 l3 -12"/><path d="M286 20 l-12 2 M286 20 l-3 12"/>
</g>
<g font-family="Poppins,Arial" font-weight="800" font-size="24" fill="#FFFFFF" text-anchor="middle">
<circle cx="150" cy="40" r="24" fill="#2E8259"/><text x="150" y="49">1</text>
<line x1="470" y1="150" x2="520" y2="120" stroke="#16324E" stroke-width="2" stroke-dasharray="4 4"/>
<circle cx="540" cy="104" r="24" fill="#2E8259"/><text x="540" y="113">2</text>
<circle cx="300" cy="118" r="11" fill="#B5541F" opacity=".3"/><circle cx="300" cy="118" r="5" fill="#B5541F"/>
<line x1="300" y1="118" x2="300" y2="228" stroke="#B5541F" stroke-width="2" stroke-dasharray="4 4"/>
<circle cx="90" cy="228" r="24" fill="#2E8259"/><text x="90" y="237">3</text>
<line x1="114" y1="228" x2="266" y2="228" stroke="#B5541F" stroke-width="2" stroke-dasharray="4 4"/>
</g>
<g font-family="Poppins,Arial" font-size="17" font-weight="700" fill="#16324E">
<text x="186" y="46">Real size</text><text x="540" y="150" text-anchor="middle">Layers</text><text x="60" y="262" >Decking</text>
</g>
</svg>"""

def trust():
    return f"""<div class="trust">
  <div>{ICONS['check']}Free, no obligation</div>
  <div>{ICONS['home']}Licensed local roofer</div>
  <div>{ICONS['nodoor']}Nobody knocks</div>
  <div>{ICONS['lock']}Never sold or resold</div>
</div>"""

def math_box(note):
    return f"""<div class="math">
  <div class="row"><span>What your roof actually costs to replace</span><b class="q">?</b></div>
  <div class="row"><span>Minus your wind-and-hail deductible</span><span class="known">you know this</span></div>
  <div class="row eq"><span>What filing would actually save you</span><b class="q">?</b></div>
  <p class="note">{note}</p>
</div>"""

def three(long=True):
    a = ("Pitch and overhangs mean two houses that look identical from the street can differ by 800 square feet of shingle. Your home's square footage tells a roofer almost nothing."
         if long else "Pitch and overhangs can add 800 square feet of shingle between two look-alike homes.")
    b = ("A second layer has to come off before anything new goes on. That's a day of labor and a dumpster before the first new shingle is nailed down."
         if long else "A second layer means a day of labor and a dumpster before anything new goes on.")
    c = ("Soft decking gets replaced board by board. Nobody can see it from the ground, from a satellite photo, or over the phone. Which is why a phone quote so often doubles once someone is actually on the roof."
         if long else "Nobody can see decking from the ground or the phone. Which is why phone quotes double on the roof.")
    return f"""<div class="diagram">{DIAGRAM}</div>
<ol class="three">
  <li><span class="n">1</span><div><b>How big the roof actually is. Not the house.</b><span>{a}</span></div></li>
  <li><span class="n">2</span><div><b>How steep it is, and how many layers are already up there.</b><span>{b}</span></div></li>
  <li><span class="n">3</span><div><b>What the wood underneath looks like.</b><span>{c}</span></div></li>
</ol>"""

def promise():
    return f"""<div class="promise"><div class="ic">{ICONS['shield']}</div>
  <div><b>The One-Roofer Promise</b>
  <span>One local roofer. One free Check. One honest number. Nobody knocks on your door. Your information is never listed, sold, or resold, not to a lead site, not to anyone, so your phone will not blow up.</span></div></div>"""

def honest(short=False):
    if short:
        return f"""<div class="honest"><div class="ic">{ICONS['alert']}</div>
  <div><b>What he will not do</b>
  <p>Waive or "cover" your deductible (Texas law says it's yours), file for you, or promise what your insurer will decide. He gives you the number. You make the call.</p></div></div>"""
    return f"""<div class="honest"><div class="ic">{ICONS['alert']}</div>
  <div><b>What he will not do</b>
  <p>He won't "waive" your deductible, "cover" it, or "work it into the estimate." Texas law says the deductible is yours to pay, and any roofer offering otherwise is offering something illegal, usually right before knocking on your neighbor's door.</p>
  <p>He also won't file for you or promise what your insurance company will decide. That's theirs to decide. His job is to give you the real number so <strong>you</strong> can decide.</p></div></div>"""

def formcard(kick, h2):
    c = ICONS['check']
    return f"""<section id="check"><div class="formcard">
  <p class="kick">{kick}</p>
  <h2>{h2}</h2>
  <p class="fsub">A few quick questions so we can match you with the right local roofer. About 90 seconds.</p>
  <!-- LEADCAPTURE.IO FORM EMBED — funnel 6oeHZT9ts5 ("Service Matchup Roofing",
       3a6436bf-6b28-4dbc-890e-5c8f32a53f34, hosted at my.leadcapture.io/p/yltkxh0_).
       Identical snippet and identical funnel to every other embed lander in this repo.
       The funnel owns the question set, validation, and Lead Prosper -> GHL routing, and
       it fires Meta `Lead` on its true submission — so this page must never fire `Lead`
       or `InitiateCheckout` (commit db71ba7; a duplicate double-counts every conversion).
       The script is nested inside #lc-embed rather than replacing it so the container
       keeps its min-height:400px and cannot collapse before the form paints. -->
  <div id="lc-embed"><script src="https://my.leadcapture.io/embed.min.js" data-funnel="6oeHZT9ts5"></script></div>
  <div class="chips">
    <span class="chip">{c}Free on-site 23-Point Check</span>
    <span class="chip">{c}Straight answer: file, pay, or wait</span>
    <span class="chip">{c}Nobody knocks. Never resold.</span>
    <span class="chip">{c}Won't affect your credit</span>
  </div>
</div></section>"""

def how():
    return """<section class="s how"><p class="kick">How it works</p><h2>Four steps. One number.</h2>
<ol>
  <li><span class="n">1</span><div><b>Answer a few questions</b>About 90 seconds. Roof age, what's going on, where you are.</div></li>
  <li><span class="n">2</span><div><b>One roofer calls to set a time</b>Not five. One. Evenings and weekends are fine.</div></li>
  <li><span class="n">3</span><div><b>He runs the 23-Point Check at your house</b>About 45 minutes, free, no obligation.</div></li>
  <li><span class="n">4</span><div><b>You get your real number and a straight answer</b>File, pay, or wait. If paying makes sense, whether it qualifies for a monthly plan as low as $99/mo.*</div></li>
</ol></section>"""

FOOTER = """<footer>
*Financing is subject to approved credit. Terms are set by the independent roofer and lender, and not everyone qualifies. Monthly payment examples are illustrative and are not an offer of credit. Checking available options will not affect your credit score.<br><br>
Deductible figures are illustrative examples of common Texas wind-and-hail deductible structures and are not a statement about your policy; check your declarations page. Under Texas law (HB 2102) the policyholder is responsible for paying the deductible in full. Service Matchup and its independent partner roofers do not waive, rebate, or absorb deductibles, do not adjust or file insurance claims on your behalf, and make no representation about whether any damage is covered. Coverage decisions are made solely by your insurer.<br><br>
The 23-Point Real-Price Check is a free, no-obligation on-site inspection. Service Matchup connects homeowners with independent licensed roofing contractors; we are not a roofing contractor, not a public adjuster, and not a lender.<br><br>
© <span id="yr"></span> Service Matchup · Wyn Group Inc · Privacy Policy · Terms of Service
</footer>"""

def sticky(label, sub):
    return f"""<div class="sticky" id="sticky"><a class="btn" href="#check">{label} <small>· {sub}</small></a></div>"""

JS = r"""
<script>
document.getElementById('yr').textContent=new Date().getFullYear();
var MARKETS = {
  dfw:{name:"Dallas–Fort Worth",metro:"623",lat:32.80,lon:-97.04,radiusMi:60},
  houston:{name:"Houston",metro:"618",lat:29.76,lon:-95.37,radiusMi:60},
  austin:{name:"Austin",metro:"635",lat:30.27,lon:-97.74,radiusMi:50},
  sanantonio:{name:"San Antonio",metro:"641",lat:29.42,lon:-98.49,radiusMi:50}
};
function milesBetween(a,b,c,d){var R=3958.8,p=Math.PI/180,x=(c-a)*p,y=(d-b)*p,h=Math.sin(x/2)*Math.sin(x/2)+Math.cos(a*p)*Math.cos(c*p)*Math.sin(y/2)*Math.sin(y/2);return 2*R*Math.asin(Math.sqrt(h));}
function marketFromGeo(g){
  if(!g) return null; var k,m;
  if(g.metroCode){ for(k in MARKETS){ if(MARKETS[k].metro===String(g.metroCode)) return k; } }
  if(g.latitude && g.longitude){ var best=null,bd=1e9;
    for(k in MARKETS){ m=MARKETS[k]; var d=milesBetween(+g.latitude,+g.longitude,m.lat,m.lon); if(d<m.radiusMi&&d<bd){best=k;bd=d;} }
    return best; }
  return null;
}
function applyMarket(slug, geo){
  var m = slug && MARKETS[slug] ? MARKETS[slug] : null;
  var isUS = !geo || !geo.country || String(geo.country).toUpperCase()==='US';
  var placeName = m ? m.name : 'Texas';
  if(isUS && geo && geo.city){ placeName=geo.city+(geo.region?', '+String(geo.region).toUpperCase().slice(0,2):''); }
  window.__GEO_OUT = geo ? {city:geo.city||'',state:geo.region||'',zip:geo.postalCode||''} : {city:'',state:'',zip:''};
  document.querySelectorAll('[data-m="name"]').forEach(function(e){e.textContent='in '+placeName;});
  document.querySelectorAll('[data-m="name2"]').forEach(function(e){e.textContent=placeName;});
  window.__MARKET = slug || '';
}
(function(){
  var param=(new URLSearchParams(location.search).get('m')||'').toLowerCase();
  var geo=window.__GEO||null;
  if(param && MARKETS[param]){ applyMarket(param,geo); return; }
  if(geo){ applyMarket(marketFromGeo(geo),geo); return; }
  applyMarket(null,null);
  try{ var ctl=new AbortController(); setTimeout(function(){ctl.abort();},1500);
    fetch('https://ipapi.co/json/',{signal:ctl.signal}).then(function(r){return r.json();}).then(function(j){
      var g={city:j.city,region:j.region_code,postalCode:j.postal,country:j.country_code,latitude:j.latitude,longitude:j.longitude};
      applyMarket(marketFromGeo(g),g); }).catch(function(){}); }catch(e){}
})();
/* tracking: skip vs read, reached form */
document.getElementById('jumpTop').addEventListener('click',function(){ try{ if(typeof fbq==='function') fbq('trackCustom','__SKIP__'); }catch(e){} });
(function(){var fired=false;window.addEventListener('scroll',function(){ if(fired) return;
  var el=document.getElementById('check'); if(!el) return;
  if(el.getBoundingClientRect().top < window.innerHeight*1.5){ fired=true; try{ if(typeof fbq==='function') fbq('trackCustom','__REACH__'); }catch(e){} }
},{passive:true});})();
/* sticky CTA: show after hero CTA leaves view, hide while form is on screen */
(function(){
  var st=document.getElementById('sticky'), hero=document.getElementById('jumpTop'), form=document.getElementById('check');
  if(!('IntersectionObserver' in window)||!st) return;
  var heroOut=false, formIn=false;
  function upd(){ st.classList.toggle('on', heroOut && !formIn); }
  new IntersectionObserver(function(es){ heroOut=!es[0].isIntersecting; upd(); },{threshold:0}).observe(hero);
  new IntersectionObserver(function(es){ formIn=es[0].isIntersecting; upd(); },{threshold:0.15}).observe(form);
})();
</script>"""

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#2E8259">
<title>__TITLE__</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://my.leadcapture.io">
<link rel="dns-prefetch" href="https://my.leadcapture.io">
<link rel="preload" as="script" href="https://my.leadcapture.io/embed.min.js">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script>
!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init','1605200247372902');fbq('track','PageView');
</script>
<style>__CSS__</style>
</head>
<body>
<div class="top"><div class="wrap"><img class="logo" src="__LOGO__" alt="Service Matchup"><span class="loc"><span class="dot"></span>Roofers available in <span data-m="name2">Texas</span></span></div></div>
<div class="wrap">
"""

def page(title, body, skip, reach, sticky_label, sticky_sub):
    html = HEAD.replace('__TITLE__', title).replace('__CSS__', CSS)
    html += body + FOOTER + "\n</div>\n" + sticky(sticky_label, sticky_sub)
    html += JS.replace('__SKIP__', skip).replace('__REACH__', reach) + "\n</body>\n</html>\n"
    return html

# ---------------- LONG (cold, problem-aware) ----------------
LONG = f"""
<section class="hero">
  <span class="eyebrow">{ICONS['home']} For Dallas–Fort Worth homeowners</span>
  <h1 id="h1">Deciding whether to <span class="ac">file a claim</span>, pay for the roof yourself, or wait it out?</h1>
  <p class="sub">You already know one number: your wind-and-hail deductible. On a lot of <span data-m="name2">Dallas–Fort Worth</span> policies that's now 1% to 2% of the home's value, <b>$4,000 to $8,000 out of your pocket</b> before insurance pays a dollar. What nobody's given you is the <b>other</b> number: what your roof actually costs. And you can't make this decision with half the math.</p>
  <a class="btn gold" href="#check" id="jumpTop">Get my real number →</a>
  <p class="note">Free 23-Point Real-Price Check · about 90 seconds · you keep the decision</p>
</section>
{trust()}

<section class="s">
  <p class="kick">The problem</p>
  <h2>So most people guess. And each guess has a price.</h2>
  <p class="lede">They file. Or they pay. Or they wait. All three go wrong the same way: without the real number.</p>
  <div class="paths">
    <div class="path"><div class="ic">{ICONS['file']}</div><div><b>They file</b><span>Because a guy at the door said to. Then the check barely clears the deductible, or the roof gets depreciated for its age, and now there's a claim on the house for a roof they mostly paid for anyway.</span></div></div>
    <div class="path"><div class="ic">{ICONS['dollar']}</div><div><b>They pay</b><span>And call three roofers, and get three numbers that are $12,000 apart, with no way to tell which one is honest. So the folder goes in a drawer.</span></div></div>
    <div class="path"><div class="ic">{ICONS['clock']}</div><div><b>They wait</b><span>And water that gets past old shingles sits in the wood. Replace a roof before that and you're buying a roof. After, you're buying a roof plus carpentry. And more carriers every year want it replaced before they'll renew.</span></div></div>
  </div>
</section>

<section class="s">
  <p class="kick">The math</p>
  <h2>The decision is one subtraction. You only have half of it.</h2>
  {math_box("If the top number is well above your deductible and there's real storm damage, filing may make sense. If it's close, you're better off knowing what a monthly payment looks like. If the roof has years left, you should hear that too. None of it is knowable from a range online.")}
</section>

<section class="s">
  <p class="kick">Why a search can't tell you</p>
  <h2>Three things set that top number. None of them show up online.</h2>
  {three(long=True)}
  <div class="pull">Your number doesn't exist until somebody is standing on your roof. And your decision doesn't exist until you have your number.</div>
</section>

<section class="s">
  <p class="kick">The offer</p>
  <h2>That's what the 23-Point Real-Price Check is for.</h2>
  <p>One honest, licensed and insured local roofer comes to your house and goes through all 23 points: size, pitch, layers, decking, flashing, valleys, ventilation, and whether there's actual storm damage up there or not. It's free, it takes about 45 minutes, and you're not obligated to anything.</p>
  <div class="what"><h3>What you walk away with</h3><ul>
    <li>{ICONS['check']}<div><b>Your actual number</b>, priced off your roof, not a national average. Now the subtraction works.</div></li>
    <li>{ICONS['check']}<div><b>A straight answer on file, pay, or wait</b>, including "you've got a few years" when that's the truth.</div></li>
    <li>{ICONS['check']}<div><b>If paying makes more sense:</b> whether it qualifies for a monthly plan, as low as $99/mo*. Checking won't affect your credit.</div></li>
  </ul></div>
  {honest()}
  {promise()}
</section>

{formcard("Free · No obligation · You keep the decision", "Get the number that decides it")}
{how()}
"""

# ---------------- SHORT (retargeting, product-aware) ----------------
SHORT = f"""
<section class="hero">
  <span class="eyebrow">{ICONS['home']} Dallas–Fort Worth homeowners</span>
  <h1 id="h1">Still deciding on the roof? You're missing <span class="ac">one number.</span></h1>
  <p class="sub">You know your deductible. You don't know what your roof actually costs <span data-m="name">in Dallas–Fort Worth</span>. One free, on-site 23-Point Real-Price Check from one honest local roofer gets you that number, and a straight answer on whether to <b>file, pay, or wait</b>.</p>
  <a class="btn gold" href="#check" id="jumpTop">Get my real number →</a>
  <p class="note">Free · about 90 seconds · no obligation · you keep the decision</p>
</section>
{trust()}

<section class="s">
  <p class="kick">The math</p>
  <h2>One subtraction. You have half of it.</h2>
  {math_box("A range online can't fill in the top line. Three things decide it, and none of them show up in a search.")}
  {three(long=False)}
</section>

<section class="s">
  {honest(short=True)}
  {promise()}
</section>

{formcard("Free · No obligation", "Get the number that decides it")}
{how()}
"""

os.makedirs(OUT, exist_ok=True)
os.makedirs(TPL_OUT, exist_ok=True)
pages = {
 'decide': page("File, Pay, or Wait? Get the Number That Decides It | Service Matchup", LONG, 'SkipToForm','ReachedForm', "Get my real number", "free, 90 sec"),
 'decide-rt':      page("Still Deciding on the Roof? | Service Matchup", SHORT, 'SkipToForm_RT','ReachedForm_RT', "Get my real number", "free, 90 sec"),
}
for name, html in pages.items():
    open(f'{TPL_OUT}/{name}.template.html','w').write(html)
    open(f'{OUT}/{name}.html','w').write(html.replace('__LOGO__', LOGO))
    txt = re.sub(r'<script.*?</script>|<style.*?</style>|<svg.*?</svg>|<[^>]+>',' ',html,flags=re.S)
    print(name, 'words:', len(txt.split()), 'bytes:', len(html.replace('__LOGO__', LOGO)))
