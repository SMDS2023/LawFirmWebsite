/* First recorded page in browser session storage; no requests or visitor identifiers. */
(function () {
    'use strict';
    if (window.LotterLeadTracking) return;
    const KEY = 'lotterlaw.lead-attribution.v2';
    const ownHosts = ['lotterlaw.com', 'www.lotterlaw.com'];
    const tagKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'gclid'];
    function cleanURL(value, referrer = false) {
        try {
            const url = new URL(value, window.location.href);
            if (referrer && url.protocol === 'android-app:' && url.hostname) {
                return ('android-app://' + url.hostname).slice(0, 500);
            }
            if (!['https:', 'http:'].includes(url.protocol)) return '';
            return (url.origin + url.pathname).slice(0, 500);
        } catch (_) { return ''; }
    }
    const current = cleanURL(window.location.href);
    const previous = document.referrer ? cleanURL(document.referrer, true) : '';
    const params = new URLSearchParams(window.location.search);
    const tags = {};
    tagKeys.forEach(key => { tags[key] = (params.get(key) || '').slice(0, key === 'gclid' ? 300 : 200); });
    // Facebook click IDs are not Google click IDs.
    const entry = { landing_page: current, entry_referrer: previous, tags };
    function validRecord(saved) {
        if (!saved || typeof saved.landing_page !== 'string' || typeof saved.entry_referrer !== 'string'
            || !saved.tags || typeof saved.tags !== 'object') return false;
        try { return ownHosts.includes(new URL(saved.landing_page).hostname); }
        catch (_) { return false; }
    }
    let visit = entry;
    let storage = 'session';
    try {
        const saved = JSON.parse(window.sessionStorage.getItem(KEY) || 'null');
        const externalArrival = previous && !ownHosts.includes(new URL(previous).hostname);
        if (validRecord(saved) && !externalArrival) visit = saved;
        window.sessionStorage.setItem(KEY, JSON.stringify(visit));
    } catch (_) {
        visit = entry;
        storage = 'page-only';
    }
    function refreshRestoredPage() {
        // A bfcache page has stale JS variables; reuse the current tab record, not its old referrer.
        if (storage !== 'session') return;
        try {
            const saved = JSON.parse(window.sessionStorage.getItem(KEY) || 'null');
            if (validRecord(saved)) visit = saved;
        } catch (_) { storage = 'page-only'; visit = entry; }
    }
    window.addEventListener('pageshow', event => { if (event.persisted) refreshRestoredPage(); });
    window.LotterLeadTracking = {
        payload() {
            refreshRestoredPage();
            const result = {
                tracking_version: '2', tracking_storage: storage,
                landing_page: visit.landing_page, entry_referrer: visit.entry_referrer,
                submission_page: cleanURL(window.location.href),
                referrer: document.referrer ? cleanURL(document.referrer, true) : '',
                user_agent: navigator.userAgent.slice(0, 512)
            };
            tagKeys.forEach(key => { result[key] = typeof visit.tags[key] === 'string' ? visit.tags[key] : ''; });
            return result;
        }
    };
})();
