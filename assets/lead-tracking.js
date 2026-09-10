/* First recorded page in this tab visit; no network requests or visitor identifiers. */
(function () {
    'use strict';
    if (window.LotterLeadTracking) return;
    const KEY = 'lotterlaw.lead-attribution.v2';
    const MAX_IDLE_MS = 30 * 60 * 1000;
    const now = Date.now();
    const ownHosts = ['lotterlaw.com', 'www.lotterlaw.com'];
    const tagKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'gclid'];
    function cleanURL(value) {
        try {
            const url = new URL(value, window.location.href);
            if (!['https:', 'http:'].includes(url.protocol)) return '';
            return (url.origin + url.pathname).slice(0, 500);
        } catch (_) { return ''; }
    }
    const current = cleanURL(window.location.href);
    const previous = document.referrer ? cleanURL(document.referrer) : '';
    const params = new URLSearchParams(window.location.search);
    const tags = {};
    tagKeys.forEach(key => { tags[key] = (params.get(key) || '').slice(0, key === 'gclid' ? 300 : 200); });
    // Facebook click IDs are not Google click IDs.
    const entry = {
        landing_page: current,
        entry_referrer: previous,
        tags,
        last_seen: now
    };
    let visit = entry;
    let storage = 'session';
    try {
        const saved = JSON.parse(window.sessionStorage.getItem(KEY) || 'null');
        const externalArrival = previous && !ownHosts.includes(new URL(previous).hostname);
        if (saved && typeof saved.landing_page === 'string' && typeof saved.entry_referrer === 'string'
            && saved.tags && typeof saved.tags === 'object' && Number.isFinite(saved.last_seen)
            && now >= saved.last_seen && now - saved.last_seen < MAX_IDLE_MS
            && !externalArrival) {
            visit = saved;
        }
        visit.last_seen = now;
        window.sessionStorage.setItem(KEY, JSON.stringify(visit));
    } catch (_) {
        visit = entry;
        storage = 'page-only';
    }
    window.LotterLeadTracking = {
        payload() {
            const result = {
                tracking_version: '2',
                tracking_storage: storage,
                landing_page: visit.landing_page,
                entry_referrer: visit.entry_referrer,
                submission_page: cleanURL(window.location.href),
                referrer: document.referrer ? cleanURL(document.referrer) : '',
                user_agent: navigator.userAgent.slice(0, 512)
            };
            tagKeys.forEach(key => { result[key] = typeof visit.tags[key] === 'string' ? visit.tags[key] : ''; });
            return result;
        }
    };
})();
