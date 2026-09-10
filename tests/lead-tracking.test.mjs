import assert from 'node:assert/strict';
import { test } from 'node:test';
import { readFileSync, readdirSync } from 'node:fs';
import { resolve } from 'node:path';
import vm from 'node:vm';
const root = resolve(import.meta.dirname, '..');
const tracker = readFileSync(resolve(root, 'assets/lead-tracking.js'), 'utf8');
function visit(url, referrer = '', memory = new Map(), { blocked = false, time = 1000000, track = true } = {}) {
  const sent = [];
  const components = {};
  const location = new URL(url);
  const storage = { getItem: key => memory.get(key) || null, setItem: (key, val) => memory.set(key, val) };
  const window = { location, sessionStorage: storage };
  if (blocked) Object.defineProperty(window, 'sessionStorage', { get() { throw Error('storage denied'); } });
  const context = vm.createContext({
    window, navigator: { userAgent: 'test-browser' }, URL, URLSearchParams,
    Date: { now: () => time }, console, setTimeout() {},
    document: { referrer, addEventListener(name, fn) { if (name === 'alpine:init') fn(); } },
    Alpine: { data(name, factory) { components[name] = factory; } },
    fetch: async (url, options) => { sent.push({ url, body: JSON.parse(options.body) }); return { ok: true, json: async () => ({ ok: true, id: 'synthetic' }) }; }
  });
  if (track) vm.runInContext(tracker, context);
  return { context, window, memory, sent, components };
}
function payload(page) { return JSON.parse(JSON.stringify(page.window.LotterLeadTracking.payload())); }
test('Google blog entry survives internal navigation to submitted form', () => {
  const first = visit('https://lotterlaw.com/blog/example/?private=value#name', 'https://www.google.com/search?q=private');
  const form = visit('https://lotterlaw.com/index.html?private=secret#contact', 'https://lotterlaw.com/blog/example/', first.memory);
  assert.equal(payload(form).landing_page, 'https://lotterlaw.com/blog/example/');
  assert.equal(payload(form).entry_referrer, 'https://www.google.com/search');
  assert.equal(payload(form).submission_page, 'https://lotterlaw.com/index.html');
  assert.equal(payload(form).referrer, 'https://lotterlaw.com/blog/example/');
  assert.equal(payload(form).tracking_storage, 'session');
});
test('blank source stays unknown and later internal tags cannot rewrite entry attribution', () => {
  const first = visit('https://lotterlaw.com/blog/example/');
  const form = visit('https://lotterlaw.com/?utm_source=internal&utm_campaign=misleading', 'https://lotterlaw.com/blog/example/', first.memory);
  assert.equal(payload(form).entry_referrer, '');
  assert.equal(payload(form).utm_source, '');
  assert.equal(payload(form).landing_page, 'https://lotterlaw.com/blog/example/');
});
test('entry campaign tags stay together and Facebook IDs never become Google IDs', () => {
  const first = visit('https://lotterlaw.com/?utm_source=newsletter&utm_medium=email&fbclid=facebook');
  const form = visit('https://lotterlaw.com/car/', 'https://lotterlaw.com/', first.memory);
  assert.equal(payload(form).utm_source, 'newsletter');
  assert.equal(payload(form).utm_medium, 'email');
  assert.equal(payload(form).gclid, '');
});
test('idle visit and new external arrival start a fresh entry', () => {
  const first = visit('https://lotterlaw.com/blog/example/');
  const later = visit('https://lotterlaw.com/', 'https://lotterlaw.com/blog/example/', first.memory, { time: 1000000 + 31 * 60000 });
  assert.equal(payload(later).landing_page, 'https://lotterlaw.com/');
  const external = visit('https://lotterlaw.com/car/', 'https://www.bing.com/', later.memory);
  assert.equal(payload(external).entry_referrer, 'https://www.bing.com/');
});
test('blocked or corrupt storage uses explicitly limited page evidence', () => {
  for (const page of [visit('https://lotterlaw.com/', '', new Map(), { blocked: true }), visit('https://lotterlaw.com/', '', new Map([['lotterlaw.lead-attribution.v2', 'bad json']]))]) {
    assert.equal(payload(page).tracking_storage, 'page-only');
    assert.equal(payload(page).submission_page, 'https://lotterlaw.com/');
  }
});
for (const file of ['contact-form.js', 'contact-form-es.js']) {
  for (const mode of ['normal', 'blocked', 'missing-tracker']) {
    test(file + ' submits successfully with ' + mode, async () => {
      const page = visit('https://lotterlaw.com/', 'https://www.google.com/', new Map(), { blocked: mode === 'blocked', track: mode !== 'missing-tracker' });
      vm.runInContext(readFileSync(resolve(root, 'assets', file), 'utf8'), page.context);
      for (const [name, factory] of Object.entries(page.components)) {
        const form = factory();
        form.$root = { querySelector: () => ({}) };
        form.init();
        Object.assign(form.formData, { name: 'Synthetic Test', phone: '4075550100', email: 'test@example.invalid', message: 'Synthetic tracking check', caseType: 'Traffic' });
        form.smsConsent = true;
        await form.submitForm();
        assert.equal(form.showSuccess, true, name);
      }
      assert.equal(page.sent.length, Object.keys(page.components).length);
      for (const request of page.sent) {
        assert.equal(request.url, 'https://lotterlaw-leads.vercel.app/api/lead');
        assert.equal(request.body.submission_page, 'https://lotterlaw.com/');
        assert.equal(request.body.tracking_storage, mode === 'normal' ? 'session' : 'page-only');
      }
    });
  }
}
test('every HTML document loads exactly one tracker before form scripts', () => {
  function scan(dir) {
    for (const entry of readdirSync(dir, { withFileTypes: true })) {
      if (entry.name.startsWith('.')) continue;
      const path = resolve(dir, entry.name);
      if (entry.isDirectory()) scan(path);
      else if (entry.name.endsWith('.html')) {
        const html = readFileSync(path, 'utf8');
        if (!/<head\b/i.test(html)) continue;
        const matches = [...html.matchAll(/<script\b[^>]*src=["']\/assets\/lead-tracking\.js["'][^>]*>/g)];
        assert.equal(matches.length, 1, path);
        const formAt = html.search(/<script\b[^>]*src=["'][^"']*contact-form(?:-es)?\.js/);
        if (formAt >= 0) assert.ok(matches[0].index < formAt, path);
      }
    }
  }
  scan(root);
});
