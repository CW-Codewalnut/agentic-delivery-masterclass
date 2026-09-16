const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const roles = ['capture-refine','design','planner','builder','tester','reviewer','curator'];
const acts = [
  'AI Has Accelerated Coding, Not Software Delivery',
  'Reimagining the Lifecycle, From Code Generation to Confidence',
  'The Four Capabilities of an Agentic SDLC',
  'From Theory to Practice, One Change Travels Through the SDLC',
  'Closing the Confidence Gaps, What Changed?',
  'From Masterclass to Enterprise Adoption'
];
const scene = page => page.locator('.scene.active');

function observeErrors(page) {
  const errors = [];
  page.on('console', msg => { if (msg.type() === 'error') errors.push(`console: ${msg.text()}`); });
  page.on('pageerror', error => errors.push(`page: ${error.message}`));
  page.on('requestfailed', request => errors.push(`network: ${request.url()} ${request.failure()?.errorText || ''}`));
  return errors;
}

test('all 16 scenes, next/back/reset, final state, and keyboard route', async ({ page }) => {
  const started = performance.now();
  await page.goto('/web/index.html');
  const payload = JSON.parse(await page.locator('#masterclass-data').textContent());
  expect(payload.experience.scenes).toHaveLength(16);
  for (let index = 0; index < 16; index++) {
    await expect(scene(page)).toHaveAttribute('id', `scene-${payload.experience.scenes[index].id}`);
    await expect(page.locator('#count')).toHaveText(`${String(index + 1).padStart(2,'0')} / 16`);
    if (index < 15) await page.locator('[data-control="next"]').click();
  }
  await expect(page.locator('[data-control="next"]')).toBeDisabled();
  await expect(scene(page)).toHaveAttribute('id', `scene-${payload.experience.scenes[15].id}`);
  await page.locator('[data-control="back"]').click();
  await expect(page.locator('#count')).toHaveText('15 / 16');
  await page.keyboard.press('Home');
  await expect(scene(page)).toHaveAttribute('id', 'scene-opening');
  await expect(page.locator('[data-control="back"]')).toBeDisabled();
  await page.keyboard.press('ArrowRight');
  await expect(scene(page)).toHaveAttribute('id', 'scene-ambiguity');
  await page.keyboard.press('ArrowLeft');
  await page.locator('[data-control="next"]').click();
  await page.locator('[data-control="reset"]').click();
  await expect(scene(page)).toHaveAttribute('id', 'scene-opening');
  const elapsedMs = Math.round((performance.now() - started) * 100) / 100;
  fs.writeFileSync('qa/automated-route-timing.json', JSON.stringify({
    route: '16 scenes plus back, reset, and keyboard checks',
    elapsedMs,
    measurement: 'automated Playwright execution; not human speech or rehearsal duration'
  }, null, 2) + '\n');
});

test('all seven role and all six exact act controls navigate', async ({ page }) => {
  await page.goto('/web/index.html');
  for (const role of roles) {
    const control = page.locator(`[data-control="role-${role}"]`);
    await control.click();
    await expect(control).toHaveAttribute('aria-current','true');
    await expect(scene(page)).toHaveAttribute('data-index', /\d+/);
  }
  for (let n=0; n<acts.length; n++) {
    const control = page.locator(`[data-control="act-${n+1}"]`);
    await expect(control).toContainText(acts[n]);
    await control.click();
    await expect(control).toHaveClass(/active/);
  }
});

test('every expanded source file equals embedded content and disk hash', async ({ page }) => {
  await page.goto('/web/index.html#ambiguity');
  await page.locator('[data-control="open-files"]').click();
  const payload = JSON.parse(await page.locator('#masterclass-data').textContent());
  const expectedPaths = Object.keys(payload.files);
  await expect(page.locator('.file-tab')).toHaveCount(expectedPaths.length);
  for (const sourcePath of expectedPaths) {
    const record = payload.files[sourcePath];
    const disk = fs.readFileSync(sourcePath, 'utf8');
    expect(disk, sourcePath).toBe(record.content);
    expect(crypto.createHash('sha256').update(disk).digest('hex'), sourcePath).toBe(record.sha256);
    await page.locator(`.file-tab[data-path="${sourcePath}"]`).evaluate(element => element.click());
    await expect(page.locator('#fileView')).toHaveText(disk);
    await expect(page.locator('#fileMeta')).toContainText(record.sha256);
  }
});

test('drawer traps focus, supports keyboard close, and restores focus', async ({ page }) => {
  await page.goto('/web/index.html');
  const open = page.locator('[data-control="open-files"]');
  await open.focus();
  await page.keyboard.press('Enter');
  await expect(page.locator('#drawer')).toHaveAttribute('aria-modal', 'true');
  await expect(page.locator('[data-control="close-files"]')).toBeFocused();
  await page.keyboard.press('Shift+Tab');
  await expect(page.locator('#fileView')).toBeFocused();
  await page.keyboard.press('Tab');
  await expect(page.locator('[data-control="close-files"]')).toBeFocused();
  await page.keyboard.press('Escape');
  await expect(page.locator('#drawer')).toHaveAttribute('aria-hidden', 'true');
  await expect(open).toBeFocused();
});

test('offline file route retains navigation and relative downloads', async ({ page }) => {
  await page.goto('file://' + path.resolve('web/index.html'));
  await expect(scene(page)).toHaveAttribute('id', 'scene-opening');
  await page.keyboard.press('ArrowRight');
  await expect(scene(page)).toHaveAttribute('id', 'scene-ambiguity');
  const links = await page.locator('a[download]').evaluateAll(nodes => nodes.map(node => node.getAttribute('href')));
  expect(links.length).toBeGreaterThanOrEqual(5);
  for (const href of new Set(links)) expect(fs.existsSync(path.resolve('web', href)), href).toBe(true);
});

test('download bytes match canonical PDF, PPTX, and presenter documents', async ({ page }) => {
  await page.goto('/web/index.html');
  const pairs = [
    ['web/downloads/Masterclass-Experience.pdf','presentation/Masterclass-Experience.pdf'],
    ['web/downloads/Masterclass-Experience.pptx','presentation/Masterclass-Experience.pptx'],
    ['web/downloads/Presenter-Script.md','presenter/SCRIPT.md'],
    ['web/downloads/Presenter-Cue-Sheet.md','presenter/CUE-SHEET.md'],
    ['web/downloads/Presenter-Timing.md','presenter/TIMING.md']
  ];
  for (const [copy, source] of pairs) {
    expect(crypto.createHash('sha256').update(fs.readFileSync(copy)).digest('hex'), copy)
      .toBe(crypto.createHash('sha256').update(fs.readFileSync(source)).digest('hex'));
  }
});

test('screen and print states have zero axe WCAG A/AA violations', async ({ page }) => {
  await page.goto('/web/index.html#reviewer');
  const tags = ['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa'];
  const screen = await new AxeBuilder({ page }).withTags(tags).analyze();
  expect(screen.violations).toEqual([]);
  await page.emulateMedia({ media: 'print' });
  const print = await new AxeBuilder({ page }).withTags(tags).analyze();
  expect(print.violations).toEqual([]);
});

test('guided route has no console, page, or network errors', async ({ page }) => {
  const errors = observeErrors(page);
  await page.goto('/web/index.html');
  for (let index=1; index<16; index++) await page.locator('[data-control="next"]').click();
  await page.locator('[data-control="open-files"]').click();
  for (const tab of await page.locator('.file-tab').all()) await tab.evaluate(element => element.click());
  await page.keyboard.press('Escape');
  expect(errors).toEqual([]);
});
