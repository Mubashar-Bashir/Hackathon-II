import { test, expect } from '@playwright/test';

test.describe('Console Error Detection', () => {
  test('should capture console errors during auth flow', async ({ page }) => {
    // Set up console error capture
    const consoleErrors: string[] = [];
    page.on('console', message => {
      if (message.type() === 'error') {
        consoleErrors.push(message.text());
        console.error('Console Error:', message.text());
      }
      if (message.type() === 'warning') {
        console.warn('Console Warning:', message.text());
      }
    });

    // Navigate to the home page which should redirect to login
    await page.goto('/');
    await expect(page).toHaveURL(/.*login/);

    // Navigate to registration page
    await page.locator('text=Sign up').click();
    await expect(page).toHaveURL(/.*register/);

    // Generate unique email for test
    const testEmail = `testuser_${Date.now()}@example.com`;
    const testPassword = 'SecurePassword123!';
    const testName = 'Test User';

    // Fill registration form
    await page.locator('input[placeholder="Your name"]').fill(testName);
    await page.locator('input[placeholder="your@email.com"]').fill(testEmail);
    await page.locator('input[type="password"]').nth(0).fill(testPassword);
    await page.locator('input[type="password"]').nth(1).fill(testPassword);

    // Submit registration
    await page.locator('button', { hasText: 'Sign Up' }).click();

    // Wait for potential redirects and capture any console errors
    await page.waitForTimeout(3000);

    // Now login with the registered credentials
    await page.locator('input[placeholder="your@email.com"]').fill(testEmail);
    await page.locator('input[type="password"]').first().fill(testPassword);
    await page.locator('button', { hasText: 'Sign In' }).click();

    // Wait for dashboard and capture any console errors
    await page.waitForTimeout(3000);

    // Check for console errors
    expect(consoleErrors).toHaveLength(0);
    if (consoleErrors.length > 0) {
      console.log('Found console errors:', consoleErrors);
    }
  });

  test('should capture console errors on dashboard', async ({ page }) => {
    // Set up console error capture
    const consoleErrors: string[] = [];
    page.on('console', message => {
      if (message.type() === 'error') {
        consoleErrors.push(message.text());
        console.error('Console Error:', message.text());
      }
      if (message.type() === 'warning') {
        console.warn('Console Warning:', message.text());
      }
    });

    // Navigate to login
    await page.goto('/login');

    // Use a known test user or register a new one
    const testEmail = `testuser_${Date.now()}@example.com`;
    const testPassword = 'SecurePassword123!';
    const testName = 'Test User';

    // Navigate to registration
    await page.locator('text=Sign up').click();

    // Fill registration form
    await page.locator('input[placeholder="Your name"]').fill(testName);
    await page.locator('input[placeholder="your@email.com"]').fill(testEmail);
    await page.locator('input[type="password"]').nth(0).fill(testPassword);
    await page.locator('input[type="password"]').nth(1).fill(testPassword);

    // Submit registration
    await page.locator('button', { hasText: 'Sign Up' }).click();
    await page.waitForURL(/.*login/, { timeout: 10000 });

    // Login
    await page.locator('input[placeholder="your@email.com"]').fill(testEmail);
    await page.locator('input[type="password"]').first().fill(testPassword);
    await page.locator('button', { hasText: 'Sign In' }).click();

    // Wait for dashboard
    await page.waitForURL(/.*dashboard/, { timeout: 10000 });
    await expect(page.locator('text=Current Tasks')).toBeVisible();

    // Wait and monitor for any console errors during normal operation
    await page.waitForTimeout(5000);

    // Check for console errors
    expect(consoleErrors).toHaveLength(0);
    if (consoleErrors.length > 0) {
      console.log('Found console errors on dashboard:', consoleErrors);
    }
  });
});