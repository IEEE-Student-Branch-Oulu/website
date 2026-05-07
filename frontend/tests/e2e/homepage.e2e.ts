import { test, expect } from '@playwright/test'

test.describe('Homepage', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('has correct page title', async ({ page }) => {
    await expect(page).toHaveTitle(/IEEE Oulu/)
  })

  test('hero section is visible', async ({ page }) => {
    // HeroSection is the first full-viewport section
    await expect(page.locator('section').first()).toBeVisible()
  })

  test('navigation links to events and blog', async ({ page }) => {
    const nav = page.getByRole('navigation')
    await expect(nav.getByRole('link', { name: /events/i })).toBeVisible()
    await expect(nav.getByRole('link', { name: /news/i })).toBeVisible()
  })

  test('navigating to /events works', async ({ page }) => {
    await page
      .getByRole('navigation')
      .getByRole('link', { name: /^events$/i })
      .first()
      .click()
    await expect(page).toHaveURL(/\/events/)
    await expect(page.getByRole('heading', { name: 'Events & Meetups' })).toBeVisible()
  })
})
