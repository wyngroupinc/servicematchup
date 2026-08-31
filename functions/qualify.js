// Cloudflare Pages Function — /functions/qualify.js
// Injects the visitor's edge geolocation into the /qualify page as window.__GEO so the page can localize itself
// (city, region, postalCode, metroCode = Nielsen DMA, latitude, longitude). No third-party lookup, no cost, no toggle needed.
export async function onRequest(context) {
  const res = await context.next();
  const ct = res.headers.get('content-type') || '';
  if (!ct.includes('text/html')) return res;
  const cf = context.request.cf || {};
  const geo = {
    country: cf.country || '', city: cf.city || '', region: cf.regionCode || cf.region || '', postalCode: cf.postalCode || '',
    metroCode: cf.metroCode || '', latitude: cf.latitude || '', longitude: cf.longitude || ''
  };
  // `<` is escaped so a stray "</script>" inside any cf field cannot close this tag early.
  const tag = `<script>window.__GEO=${JSON.stringify(geo).replace(/</g, '\\u003c')};</script>`;
  return new HTMLRewriter().on('head', { element(el) { el.prepend(tag, { html: true }); } }).transform(res);
}
