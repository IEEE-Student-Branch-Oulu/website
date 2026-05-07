import { test, expect } from '@playwright/test'

test.describe('Blog page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/blog')
  })

  test('renders page heading', async ({ page }) => {
    await expect(page.getByRole('heading', { name: 'Infodumps', level: 1 })).toBeVisible()
  })

  test('shows posts count', async ({ page }) => {
    await expect(page.getByText(/\d+ posts?/i).first()).toBeVisible()
  })

  test('featured post is visible', async ({ page }) => {
    // Featured post takes the full-width hero slot above the grid
    const featured = page.locator('article').first()
    await expect(featured).toBeVisible()
  })

  test('category sidebar is present', async ({ page }) => {
    await expect(page.getByText(/About Infodumps/i)).toBeVisible()
  })
})
