const { test, expect } = require('@playwright/test');
const fs = require('fs');

test('all scenes fit the presentation stage at projector size', async ({ page }) => {
  await page.goto('/web/index.html');
  const scenes = await page.locator('.scene').count();
  const report = [];
  for (let i=0; i<scenes; i++) {
    if (i) await page.keyboard.press('ArrowRight');
    const active = page.locator('.scene.active');
    const measure = await active.evaluate(el => ({
      id: el.id,
      scrollWidth: el.scrollWidth,
      clientWidth: el.clientWidth,
      scrollHeight: el.scrollHeight,
      clientHeight: el.clientHeight
    }));
    report.push(measure);
    expect(measure.scrollWidth, `${measure.id} horizontal overflow`).toBeLessThanOrEqual(measure.clientWidth + 1);
    expect(measure.scrollHeight, `${measure.id} vertical overflow`).toBeLessThanOrEqual(measure.clientHeight + 1);
  }
  fs.mkdirSync('qa', { recursive: true });
  fs.writeFileSync('qa/layout-measurements.json', JSON.stringify(report, null, 2) + '\n');
  await page.goto('/web/index.html#opening');
  await expect(page.locator('.scene.active h1')).toHaveText('Faster coding is only the beginning.');
  await expect(page.locator('#count')).toHaveText('01 / 16');
  await page.screenshot({ path: 'qa/experience-wide.png', fullPage: true });
  await page.goto('/web/index.html#capabilities');
  await expect(page.locator('.scene.active h1')).toHaveText('Four capabilities make the lifecycle dependable.');
  await expect(page.locator('#count')).toHaveText('06 / 16');
  await page.screenshot({ path: 'qa/experience-capabilities.png', fullPage: true });
  await page.goto('/web/index.html#reviewer');
  await expect(page.locator('.scene.active h1')).toHaveText('Why should we trust this change?');
  await expect(page.locator('#count')).toHaveText('11 / 16');
  await page.screenshot({ path: 'qa/experience-reviewer.png', fullPage: true });
});

test('mobile route remains usable without horizontal clipping', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/web/index.html#ambiguity');
  await expect(page.locator('.scene.active h1')).toHaveText('The request is simple. The behaviour isn’t.');
  await expect(page.locator('#count')).toHaveText('02 / 16');
  await page.screenshot({ path: 'qa/experience-mobile-top.png', fullPage: true });
  const width = await page.evaluate(() => ({ scroll: document.documentElement.scrollWidth, client: document.documentElement.clientWidth }));
  expect(width.scroll).toBeLessThanOrEqual(width.client + 1);
  await expect(page.locator('[data-control="next"]')).toBeVisible();
  const question = page.locator('.scene.active .question').last();
  const takeaway = page.locator('.scene.active .takeaway');
  await question.scrollIntoViewIfNeeded();
  await takeaway.scrollIntoViewIfNeeded();
  const [qBox, tBox] = await Promise.all([question.boundingBox(), takeaway.boundingBox()]);
  expect(qBox.y + qBox.height).toBeLessThanOrEqual(tBox.y + 1);
  await expect(takeaway).toBeInViewport();
  await page.screenshot({ path: 'qa/experience-mobile.png', fullPage: true });
  await page.locator('[data-control="next"]').click();
  await expect(page.locator('.scene.active')).toHaveAttribute('id', 'scene-agreement');
  await expect(page.locator('.scene.active .card').last()).toContainText('Testable behaviour');
});

for (const viewport of [
  { name: 'desktop', width: 1440, height: 900 },
  { name: 'mobile', width: 390, height: 844 },
]) {
  test(`source drawer stays contained and pointer-reachable on ${viewport.name}`, async ({ page }) => {
    await page.setViewportSize({ width: viewport.width, height: viewport.height });
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.goto('/web/index.html#ambiguity');
    await page.locator('[data-control="open-files"]').click();

    const drawer = page.locator('#drawer');
    const close = page.locator('[data-control="close-files"]');
    const fileView = page.locator('#fileView');
    const payload = JSON.parse(await page.locator('#masterclass-data').textContent());
    const paths = Object.keys(payload.files);
    await expect(page.locator('.file-tab')).toHaveCount(paths.length);

    const geometry = await drawer.evaluate(element => {
      const box = selector => {
        const rect = element.querySelector(selector).getBoundingClientRect();
        return { left: rect.left, right: rect.right, width: rect.width };
      };
      return {
        viewportWidth: window.innerWidth,
        drawer: (() => { const rect = element.getBoundingClientRect(); return { left: rect.left, right: rect.right, width: rect.width }; })(),
        head: box('.drawer-head'),
        close: box('[data-control="close-files"]'),
        fileTabs: box('#fileTabs'),
        fileMeta: box('#fileMeta'),
        fileView: box('#fileView'),
        scrollWidth: element.scrollWidth,
        clientWidth: element.clientWidth,
      };
    });
    for (const [name, box] of Object.entries(geometry)) {
      if (!box || typeof box !== 'object') continue;
      expect(box.left, `${name} starts outside viewport`).toBeGreaterThanOrEqual(-1);
      expect(box.right, `${name} ends outside viewport`).toBeLessThanOrEqual(viewport.width + 1);
    }
    expect(geometry.scrollWidth, 'drawer must not horizontally overflow').toBeLessThanOrEqual(geometry.clientWidth + 1);

    for (const sourcePath of paths) {
      const tab = page.locator('.file-tab').filter({ hasText: sourcePath }).first();
      await tab.scrollIntoViewIfNeeded();
      await expect(tab).toBeInViewport();
      await tab.click();
      await expect(tab).toHaveAttribute('aria-selected', 'true');
      await expect(fileView).toContainText(payload.files[sourcePath].content.slice(0, 80));
    }

    const firstTab = page.locator('.file-tab').first();
    await firstTab.scrollIntoViewIfNeeded();
    await firstTab.click();
    await expect(firstTab).toHaveAttribute('aria-selected', 'true');
    await page.screenshot({ path: `qa/source-drawer-${viewport.name}.png`, fullPage: true });
    await expect(close).toBeInViewport();
    await close.click();
    await expect(drawer).toHaveAttribute('aria-hidden', 'true');
  });
}
