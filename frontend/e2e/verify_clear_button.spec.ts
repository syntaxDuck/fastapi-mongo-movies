import { test, expect } from '@playwright/test';

test('clear button functionality', async ({ page }) => {
  await page.goto('http://localhost:3000/test-search', { waitUntil: 'networkidle' });
  const searchInput = page.locator('input[placeholder="Search for movies..."]');
  await searchInput.waitFor({ state: 'visible' });

  await searchInput.fill('Inception');
  const clearButton = page.locator('button[aria-label="Clear input"]');
  await expect(clearButton).toBeVisible();
  await page.screenshot({ path: '/app/with_clear_button_test.png' });

  await clearButton.click();
  await expect(searchInput).toHaveValue('');
  await page.screenshot({ path: '/app/after_clear_test.png' });
});
