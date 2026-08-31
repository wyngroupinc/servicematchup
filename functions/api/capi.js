// Cloudflare Pages Function — /functions/api/capi.js
// Server-side relay to the Meta Conversions API for /qualify.
//
// The page fires each browser-pixel event with an event_id and POSTs the SAME event_id here;
// Meta then dedupes the browser/server pair instead of counting it twice.
//
// It is INERT until the Pages project has a META_CAPI_TOKEN environment variable (a Meta system-user
// access token with ads_management on the dataset). Without it every request returns 204 and nothing
// is sent — the page keeps working, it just runs browser-pixel only.
//
// The page never posts `Lead` here: the LeadCapture funnel owns Lead, on its true submission.
// Only PageView and InitiateCheckout are accepted, so a spoofed POST cannot manufacture conversions.

const PIXEL_ID = '1605200247372902';          // Service Matchup dataset — the only one this page uses.
const ALLOWED = new Set(['PageView', 'InitiateCheckout']);
const GRAPH = 'https://graph.facebook.com/v21.0';

function cookie(request, name) {
  const raw = request.headers.get('cookie') || '';
  const hit = raw.split(';').map(s => s.trim()).find(s => s.startsWith(name + '='));
  return hit ? decodeURIComponent(hit.slice(name.length + 1)) : undefined;
}

export async function onRequestPost(context) {
  const { request, env } = context;
  const token = env.META_CAPI_TOKEN;
  if (!token) return new Response(null, { status: 204 });          // not configured — no-op

  let body;
  try { body = await request.json(); } catch (e) { return new Response(null, { status: 204 }); }
  const name = body && body.event_name;
  if (!ALLOWED.has(name) || !body.event_id) return new Response(null, { status: 204 });

  const cf = request.cf || {};
  const payload = {
    data: [{
      event_name: name,
      event_time: Math.floor(Date.now() / 1000),
      event_id: String(body.event_id).slice(0, 100),               // the dedupe key — same value the pixel sent
      event_source_url: String(body.event_source_url || '').slice(0, 500),
      action_source: 'website',
      user_data: {
        client_ip_address: request.headers.get('cf-connecting-ip') || undefined,
        client_user_agent: request.headers.get('user-agent') || undefined,
        fbp: cookie(request, '_fbp'),
        fbc: cookie(request, '_fbc'),
        ct: undefined, st: undefined                                // no PII is collected here; the form owns that
      },
      custom_data: {
        market: (body.custom_data && String(body.custom_data.market || '').slice(0, 40)) || '',
        city: cf.city || '',
        region: cf.regionCode || cf.region || ''
      }
    }]
  };
  if (env.META_TEST_EVENT_CODE) payload.test_event_code = env.META_TEST_EVENT_CODE;

  try {
    await fetch(`${GRAPH}/${env.META_PIXEL_ID || PIXEL_ID}/events?access_token=${encodeURIComponent(token)}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
  } catch (e) { /* never let tracking break the page */ }

  return new Response(null, { status: 204 });
}

// Only onRequestPost is exported: Pages answers any other method on /api/capi with 405 by itself.
