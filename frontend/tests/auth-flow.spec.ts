import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the home page which should redirect to login
    await page.goto('/');
    await expect(page).toHaveURL(/.*login/);
  });

  test('should allow user to register and login', async ({ page }) => {
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

    // Wait for redirect to login page or for an error to appear
    // Wait up to 10 seconds for the redirect to happen
    try {
      await page.waitForURL(/.*login/, { timeout: 10000 });
      console.log('Successfully redirected to login page');
    } catch (error) {
      console.log('Redirect to login did not happen, checking for errors...');
      // Check if we're still on register page and if there's an error message
      const currentUrl = page.url();
      console.log('Current URL after registration attempt:', currentUrl);

      // Wait a bit more to see if there are any delayed error messages
      await page.waitForTimeout(2000);

      if (currentUrl.includes('register')) {
        // Check for error message
        const hasError = await page.locator('div[class*="bg-red-500"]').isVisible();
        if (hasError) {
          const errorMessage = await page.locator('div[class*="bg-red-500"]').textContent();
          console.log('Found error message:', errorMessage);
          throw new Error(`Registration failed with error: ${errorMessage}`);
        } else {
          // Check if the button is still in a loading state or if there are console errors
          const isButtonLoading = await page.locator('button:has-text("Creating account...")').isVisible();
          if (isButtonLoading) {
            console.log('Button is still in loading state');
          }

          // Get any console errors that might have occurred
          const consoleErrors = await page.evaluate(() => {
            // This is a simplified approach - in a real test, you'd need to capture console events
            return 'No direct way to get console errors after the fact';
          });
          console.log('Console error check:', consoleErrors);

          console.log('No visible error message found, but registration did not redirect');
          throw new Error('Registration did not complete successfully - no redirect or visible error message');
        }
      } else {
        // If we're on a different page, just continue with the test
        console.log('Not on register page, continuing with test');
      }
    }

    // If we get here, we should be on the login page
    await expect(page.locator('text=Welcome Back')).toBeVisible();

    // Now login with the registered credentials
    await page.locator('input[placeholder="your@email.com"]').fill(testEmail);
    await page.locator('input[type="password"]').first().fill(testPassword);
    await page.locator('button', { hasText: 'Sign In' }).click();

    // Wait for redirect to dashboard or check for errors
    try {
      await page.waitForURL(/.*dashboard/, { timeout: 10000 });
      console.log('Successfully redirected to dashboard');
    } catch (error) {
      console.log('Login redirect did not happen, checking current page...');
      const currentUrl = page.url();
      console.log('Current URL after login attempt:', currentUrl);

      // Check if still on login page and if there are error messages
      if (currentUrl.includes('login')) {
        const hasError = await page.locator('div[class*="bg-red-500"]').isVisible();
        if (hasError) {
          const errorMessage = await page.locator('div[class*="bg-red-500"]').textContent();
          console.log('Found login error message:', errorMessage);
          throw new Error(`Login failed with error: ${errorMessage}`);
        } else {
          console.log('Still on login page but no error message found');
          throw new Error('Login did not complete successfully - still on login page');
        }
      }
    }

    // Should be redirected to dashboard after login
    await expect(page).toHaveURL(/.*dashboard/);
    await expect(page.locator('text=Current Tasks')).toBeVisible();

    // Verify user info is displayed in the top right (or somewhere on the page)
    // Check for the user's first name, email, or a welcome message
    const hasFirstName = await page.locator(`text=${testName.split(' ')[0]}`).isVisible();
    const hasEmail = await page.locator(`text=${testEmail.split('@')[0]}`).isVisible();
    const hasWelcome = await page.locator('text=Welcome').isVisible();

    if (!hasFirstName && !hasEmail && !hasWelcome) {
      // Take a screenshot to see what's actually on the page
      await page.screenshot({ path: 'debug-dashboard.png' });
      throw new Error(`User info not visible on dashboard. Expected to find: ${testName.split(' ')[0]}, ${testEmail.split('@')[0]}, or 'Welcome'`);
    }
  });

  test('should show error for invalid login credentials', async ({ page }) => {
    // Try to login with invalid credentials
    await page.locator('input[placeholder="your@email.com"]').fill('invalid@example.com');
    await page.locator('input[type="password"]').first().fill('invalidpassword');
    await page.locator('button', { hasText: 'Sign In' }).click();

    // Should show an error message (check for common error patterns)
    // Wait a bit for the error to appear
    await page.waitForTimeout(1000);

    // Check for any of the possible error messages
    const hasLoginFailed = await page.locator('text=Login failed').isVisible();
    const hasInvalid = await page.locator('text=Invalid').isVisible();
    const hasError = await page.locator('text=error').isVisible();
    const hasFailed = await page.locator('text=failed').isVisible();

    expect(hasLoginFailed || hasInvalid || hasError || hasFailed).toBe(true);
  });

  test('should allow user to logout', async ({ page }) => {
    // First register and login a user
    await page.locator('text=Sign up').click();
    const testEmail = `testuser_${Date.now()}@example.com`;
    const testPassword = 'SecurePassword123!';
    const testName = 'Test User';

    await page.locator('input[placeholder="Your name"]').fill(testName);
    await page.locator('input[placeholder="your@email.com"]').fill(testEmail);
    await page.locator('input[type="password"]').nth(0).fill(testPassword);
    await page.locator('input[type="password"]').nth(1).fill(testPassword);
    await page.locator('button', { hasText: 'Sign Up' }).click();

    // Wait for redirect to login page or for an error to appear
    try {
      await page.waitForURL(/.*login/, { timeout: 10000 });
      console.log('Logout test - Successfully redirected to login page');
    } catch (error) {
      console.log('Logout test - Redirect to login did not happen, checking for errors...');
      const currentUrl = page.url();
      console.log('Logout test - Current URL after registration attempt:', currentUrl);

      // Wait a bit more to see if there are any delayed error messages
      await page.waitForTimeout(2000);

      if (currentUrl.includes('register')) {
        // Check for error message
        const hasError = await page.locator('div[class*="bg-red-500"]').isVisible();
        if (hasError) {
          const errorMessage = await page.locator('div[class*="bg-red-500"]').textContent();
          console.log('Logout test - Found error message:', errorMessage);
          throw new Error(`Registration failed with error: ${errorMessage}`);
        } else {
          console.log('Logout test - No visible error message found, but registration did not redirect');
          throw new Error('Registration did not complete successfully - no redirect or visible error message');
        }
      }
    }

    // If we get here, we should be on the login page
    await expect(page.locator('text=Welcome Back')).toBeVisible();

    // Now login with the registered credentials
    await page.locator('input[placeholder="your@email.com"]').fill(testEmail);
    await page.locator('input[type="password"]').first().fill(testPassword);
    await page.locator('button', { hasText: 'Sign In' }).click();

    // Wait for redirect to dashboard or check for errors
    try {
      await page.waitForURL(/.*dashboard/, { timeout: 10000 });
      console.log('Logout test - Successfully redirected to dashboard');
    } catch (error) {
      console.log('Logout test - Login redirect did not happen, checking current page...');
      const currentUrl = page.url();
      console.log('Logout test - Current URL after login attempt:', currentUrl);

      // Check if still on login page and if there are error messages
      if (currentUrl.includes('login')) {
        const hasError = await page.locator('div[class*="bg-red-500"]').isVisible();
        if (hasError) {
          const errorMessage = await page.locator('div[class*="bg-red-500"]').textContent();
          console.log('Logout test - Found login error message:', errorMessage);
          throw new Error(`Login failed with error: ${errorMessage}`);
        } else {
          console.log('Logout test - Still on login page but no error message found');
          throw new Error('Login did not complete successfully - still on login page');
        }
      }
    }

    // Should be redirected to dashboard after login
    await expect(page).toHaveURL(/.*dashboard/);
    await expect(page.locator('text=Current Tasks')).toBeVisible();

    // Verify user info is displayed in the top right (or somewhere on the page)
    // Check for the user's first name, email, or a welcome message
    const hasFirstName = await page.locator(`text=${testName.split(' ')[0]}`).isVisible();
    const hasEmail = await page.locator(`text=${testEmail.split('@')[0]}`).isVisible();
    const hasWelcome = await page.locator('text=Welcome').isVisible();

    if (!hasFirstName && !hasEmail && !hasWelcome) {
      throw new Error(`User info not visible on dashboard. Expected to find: ${testName.split(' ')[0]}, ${testEmail.split('@')[0]}, or 'Welcome'`);
    }

    // Click logout button
    await page.locator('text=Logout').click();

    // Should be redirected back to login
    await expect(page.locator('text=Welcome Back')).toBeVisible();
  });
});