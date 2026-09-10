import assert from 'node:assert/strict';
import { readFile, mkdir, writeFile, stat } from 'node:fs/promises';
import { resolve, extname } from 'node:path';
import { chromium, webkit } from 'playwright';

const root = resolve(import.meta.dirname, '..');
const out = process.env.BROWSER_PROOF_DIR || resolve(root, '../verification/browser');
await mkdir(out, { recursive: true });
const mime = { '.html': 'text/html', '.js': 'application/javascript', '.css': 'text/css', '.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.json': 'application/json' };
const article = '/blog/motion-in-limine-florida-criminal-case/';
const results = [];
const cdnCache = new Map();

async function run(engine, engineName) {
  const browser = await engine.launch({ headless: true, args: engineName === 'chromium' && process.env.AGENT_BROWSER_PATH ? ['--remote-debugging-port=9335'] : [] });
  async function setup({ blocked = false, android = false } = {}) {
    const context = await browser.newContext({ viewport: { width: 1440, height: 1100 } });
    const requests = [];
    const forbidden = [];
    const errors = [];
    await context.route('**/*', async route => {
      const request = route.request();
      const url = new URL(request.url());
      if (url.hostname === 'lotterlaw-leads.vercel.app') {
        // Explicit test sink: no production lead or email can be created by these browser checks.
        if (request.method() === 'OPTIONS') return route.fulfill({ status: 204, headers: { 'access-control-allow-origin': 'https://lotterlaw.com', 'access-control-allow-methods': 'POST', 'access-control-allow-headers': 'content-type' } });
        requests.push(JSON.parse(request.postData()));
        return route.fulfill({ status: 200, contentType: 'application/json', headers: { 'access-control-allow-origin': 'https://lotterlaw.com' }, body: '{"ok":true,"id":"synthetic-browser-only"}' });
      }
      if (url.hostname === 'www.google.com' && url.pathname === '/' && request.isNavigationRequest() && !request.frame().parentFrame()) {
        return route.fulfill({ contentType: 'text/html', body: '<!doctype html><title>Synthetic referral origin</title><a href="https://lotterlaw.com' + article + '">Open article</a>' });
      }
      if (url.hostname === 'lotterlaw.com') {
        let path = resolve(root, '.' + decodeURIComponent(url.pathname));
        if (path !== root && !path.startsWith(root + '/')) return route.abort();
        try {
          if ((await stat(path)).isDirectory()) path = resolve(path, 'index.html');
          return route.fulfill({ contentType: mime[extname(path)] || 'application/octet-stream', body: await readFile(path) });
        } catch { return route.fulfill({ status: 404, body: 'Not found in review checkout' }); }
      }
      // Real UI runtime assets only. Analytics and third-party form systems never receive test activity.
      if (['cdn.jsdelivr.net', 'cdn.tailwindcss.com', 'fonts.googleapis.com', 'fonts.gstatic.com'].includes(url.hostname)) {
        try {
          if (!cdnCache.has(request.url())) {
            const response = await context.request.get(request.url());
            cdnCache.set(request.url(), { status: response.status(), headers: response.headers(), body: await response.body() });
          }
          return route.fulfill(cdnCache.get(request.url()));
        } catch { return route.abort(); }
      }
      forbidden.push(url.hostname);
      return route.abort();
    });
    if (blocked) await context.addInitScript(() => Object.defineProperty(window, 'sessionStorage', { get() { throw new DOMException('Test storage denied', 'SecurityError'); } }));
    if (android) await context.addInitScript(() => Object.defineProperty(document, 'referrer', { get() { return 'android-app://com.google.android.googlequicksearchbox'; } }));
    const page = await context.newPage();
    page.on('pageerror', error => errors.push(error.message));
    return { context, page, requests, forbidden, errors };
  }
  async function fillAndSubmit(page, { qr = false, label }) {
    const form = page.locator(qr ? 'form[x-data="qrOptInForm()"]' : 'form[x-data="contactForm()"]').first();
    await form.waitFor({ state: 'visible' });
    await form.locator('[x-model="formData.name"]').fill('TEST LOJ-545 Browser ' + label);
    await form.locator('[x-model="formData.phone"]').fill('4075550100');
    if (!qr) {
      await form.locator('[x-model="formData.email"]').fill('browser-test@example.invalid');
      await form.locator('[x-model="formData.message"]').fill('Synthetic local browser verification only; do not create a real lead.');
    }
    await form.locator('[x-model="formData.caseType"]').selectOption('Traffic');
    if (qr) await form.locator('[x-model="smsConsent"]').check();
    const button = form.locator('button[type="submit"]');
    await button.evaluate(element => element.scrollIntoView({ block: 'center', behavior: 'instant' }));
    await button.click();
    const success = form.locator('[x-show="showSuccess"]');
    await success.waitFor({ state: 'visible' });
    await success.evaluate(element => element.scrollIntoView({ block: 'center', behavior: 'instant' }));
    await page.screenshot({ path: resolve(out, engineName + '-' + label + '.png'), fullPage: false, animations: 'disabled' });
  }
  async function capture(name, flow) {
    const started = Date.now();
    try { await flow(); results.push({ engine: engineName, journey: name, result: 'PASS', milliseconds: Date.now() - started }); }
    catch (error) { results.push({ engine: engineName, journey: name, result: 'FAIL', error: error.message }); throw error; }
    finally { await writeFile(resolve(out, 'results.json'), JSON.stringify({ type: 'real-browser/local-code/intercepted-integrations', results }, null, 2)); }
  }
  await capture('article-to-homepage', async () => {
    const state = await setup();
    try {
      await state.page.goto('https://www.google.com/');
      await state.page.getByRole('link', { name: 'Open article' }).click();
      await state.page.waitForURL('**' + article);
      const first = await state.page.evaluate(() => window.LotterLeadTracking.payload());
      assert.equal(first.entry_referrer, 'https://www.google.com/');
      // Advance the browser clock by45minutes without waiting45minutes; real navigation/storage remain unchanged.
      await state.page.clock.setFixedTime(new Date(Date.now() + 45 * 60000));
      const home = state.page.locator('a[href="/"],a[href="/index.html"],a[href="../../index.html"],a[href="https://lotterlaw.com/"]').first();
      await home.click();
      await state.page.waitForURL(url => ['/', '/index.html'].includes(url.pathname));
      await fillAndSubmit(state.page, { label: 'article-home' });
      assert.equal(state.requests.length, 1);
      assert.equal(state.requests[0].landing_page, 'https://lotterlaw.com' + article);
      assert.equal(state.requests[0].entry_referrer, 'https://www.google.com/');
      const events = await state.page.evaluate(() => window.dataLayer.filter(x => x.event === 'form_submission'));
      assert.equal(events.length, 1);
      assert.equal(events[0].landing_page, state.requests[0].landing_page);
      assert.equal(events[0].submission_page, state.requests[0].submission_page);
      assert.equal(events[0].entry_referrer_host, 'www.google.com');
      assert.equal(events[0].utm_source, '');
      for (const key of ['name', 'phone', 'email', 'message', 'website', 'user_agent']) assert.equal(events[0][key], undefined);
      await writeFile(resolve(out, engineName + '-article-evidence.json'), JSON.stringify({ request: state.requests[0], event: events[0], pageErrors: state.errors }, null, 2));
      if (engineName === 'chromium' && process.env.AGENT_BROWSER_PATH) {
        const { execFile } = await import('node:child_process');
        const { promisify } = await import('node:util');
        const captured = await promisify(execFile)(process.env.AGENT_BROWSER_PATH, ['--session', 'loj545-review', '--cdp', 'http://127.0.0.1:9335', 'snapshot', '-i']);
        await writeFile(resolve(out, 'agent-browser-snapshot.txt'), captured.stdout);
      }

    } finally { await state.context.close(); }
  });
  for (const scenario of [
    { label: 'direct-car', path: '/car/', qr: true },
    { label: 'spanish', path: '/es/practice-areas/dui.html' },
    { label: 'blocked-storage', path: '/', blocked: true },
    { label: 'android-referrer-simulated', path: '/', android: true },
  ]) {
    await capture(scenario.label, async () => {
      const state = await setup(scenario);
      try {
        await state.page.goto('https://lotterlaw.com' + scenario.path);
        await fillAndSubmit(state.page, scenario);
        assert.equal(state.requests.length, 1);
        const request = state.requests[0];
        assert.equal(request.submission_page, 'https://lotterlaw.com' + scenario.path);
        assert.equal(request.tracking_storage, scenario.blocked ? 'page-only' : 'session');
        if (scenario.android) assert.equal(request.entry_referrer, 'android-app://com.google.android.googlequicksearchbox');
        const events = await state.page.evaluate(() => window.dataLayer.filter(x => x.event === 'form_submission'));
        assert.equal(events.length, 1);
        for (const key of ['utm_source', 'utm_medium', 'utm_campaign']) assert.equal(events[0][key], '');
        await writeFile(resolve(out, engineName + '-' + scenario.label + '.json'), JSON.stringify({ request, event: events[0], pageErrors: state.errors }, null, 2));
      } finally { await state.context.close(); }
    });
  }
  await capture('back-forward-and-new-tab', async () => {
    const state = await setup();
    try {
      await state.page.goto('https://www.google.com/');
      await state.page.getByRole('link', { name: 'Open article' }).click();
      await state.page.waitForURL('**' + article);
      await state.page.locator('a[href="/"],a[href="/index.html"],a[href="../../index.html"],a[href="https://lotterlaw.com/"]').first().click();
      await state.page.goBack();
      await state.page.waitForFunction(() => !!window.LotterLeadTracking);
      assert.equal((await state.page.evaluate(() => window.LotterLeadTracking.payload())).entry_referrer, 'https://www.google.com/');
      // A genuinely independent tab has no opener; it must not inherit a made-up external origin.
      const other = await state.context.newPage();
      await other.goto('https://lotterlaw.com/car/');
      const fresh = await other.evaluate(() => window.LotterLeadTracking.payload());
      assert.equal(fresh.entry_referrer, '');
      await other.close();
    } finally { await state.context.close(); }
  });
  await browser.close();
}
for (const [engine, name] of [[chromium, 'chromium'], [webkit, 'webkit']]) {
  if (process.env.BROWSER_ENGINES && !process.env.BROWSER_ENGINES.split(',').includes(name)) continue;
  await run(engine, name);
}
console.log(JSON.stringify({ results, note: 'Real browser execution against local review files. API responses intercepted; no CRM, inbox or GA4 delivery proof is claimed.' }, null, 2));

