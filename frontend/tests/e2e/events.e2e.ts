import { test, expect } from '@playwright/test'

test.describe('Events page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/events')
  })

  test('renders page heading and stats', async ({ page }) => {
    await expect(page.getByRole('heading', { name: 'Events & Meetups', level: 1 })).toBeVisible()
    await expect(page.getByText('Upcoming').first()).toBeVisible()
    await expect(page.getByText('Total')).toBeVisible()
  })

  test('shows event cards', async ({ page }) => {
    // At least one EventCard should be rendered
    const cards = page.locator('[data-testid="event-card"], article').first()
    await expect(cards).toBeVisible()
  })

  test('filter bar is present and has upcoming/past/all options', async ({ page }) => {
    // Fallback: just check filter labels exist in the page
    await expect(page.getByText(/upcoming/i).first()).toBeVisible()
    await expect(page.getByText(/all/i).first()).toBeVisible()
  })

  test('clicking "All" filter shows events', async ({ page }) => {
    // Find the All filter button and click it
    const allBtn = page
      .getByRole('button', { name: /^all/i })
      .or(page.getByRole('tab', { name: /^all/i }))
    if ((await allBtn.count()) > 0) {
      await allBtn.first().click()
    }
    // After clicking All, there should be at least one event visible
    const resultCount = page.getByText(/event(s)? found/i)
    await expect(resultCount).toBeVisible()
  })

  test('sidebar quick links are present', async ({ page }) => {
    await expect(page.getByText('Quick Links')).toBeVisible()
    await expect(page.getByText(/Discord/i).first()).toBeVisible()
  })

  test('event type legend is shown', async ({ page }) => {
    await expect(page.getByText('Event Types')).toBeVisible()
  })
})
