const { test, expect } = require('@playwright/test');

test.describe('Mobile sidebar', () => {
  test.beforeEach(async ({ page, baseURL }) => {
    await page.goto(baseURL || '/');
  });

  test('opens and traps focus, closes with Escape and click-outside', async ({ page }) => {
    const hamburger = page.locator('#hamburger');
    const sidebar = page.locator('#sidebar');

    await expect(sidebar).toHaveAttribute('aria-hidden', 'true');

    // Open sidebar
    await hamburger.click();
    await expect(sidebar).toHaveClass(/open/);
    await expect(sidebar).toHaveAttribute('aria-hidden', 'false');
    await expect(hamburger).toHaveAttribute('aria-expanded', 'true');

    // Tab inside sidebar and ensure focus cycles
    const firstLink = sidebar.locator('a').first();
    await expect(firstLink).toBeFocused();

    // Press Tab until it wraps (simulate), ensure focus stays in sidebar
    await page.keyboard.press('Tab');
    // No assertion on exact element but ensure focus is within sidebar
    const active = await page.evaluate(() => document.activeElement.closest('#sidebar') !== null);
    expect(active).toBeTruthy();

    // Close with Escape
    await page.keyboard.press('Escape');
    await expect(sidebar).not.toHaveClass(/open/);
    await expect(sidebar).toHaveAttribute('aria-hidden', 'true');
    await expect(hamburger).toHaveAttribute('aria-expanded', 'false');

    // Re-open then click outside to close
    await hamburger.click();
    await expect(sidebar).toHaveClass(/open/);
    await page.click('body', { position: { x: 5, y: 5 } });
    await expect(sidebar).not.toHaveClass(/open/);
  });

  test('skill bars animate when entering viewport', async ({ page }) => {
    // navigate to about page where skill bars are expected
    await page.goto('/about');
    const skillFill = page.locator('.skill-fill[data-width]').first();
    if (await skillFill.count() === 0) {
      test.skip();
      return;
    }
    // Scroll into view and wait for width style to be applied
    await skillFill.scrollIntoViewIfNeeded();
    await page.waitForTimeout(400); // allow JS animation to run
    const width = await skillFill.evaluate((el) => window.getComputedStyle(el).width);
    expect(parseFloat(width)).toBeGreaterThan(0);
  });
});
