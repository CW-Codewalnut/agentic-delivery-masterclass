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
