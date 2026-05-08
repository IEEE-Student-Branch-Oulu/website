import { test, expect } from '@playwright/test'

test.describe('Auth pages', () => {
  test('register page renders the 3-step wizard', async ({ page }) => {
    await page.goto('/auth/register')
    await expect(page).toHaveTitle(/Register/)
    await expect(page.getByRole('heading', { name: /create your account/i })).toBeVisible()
    await expect(page.getByLabel(/email/i)).toBeVisible()
    await expect(page.getByLabel(/^password$/i)).toBeVisible()
  })

  test('register step 1 validates required fields', async ({ page }) => {
    await page.goto('/auth/register')
    await page.getByRole('button', { name: /next/i }).click()
    await expect(page.getByText(/required/i).first()).toBeVisible()
  })

  test('login page renders email and password fields', async ({ page }) => {
    await page.goto('/auth/login')
    await expect(page).toHaveTitle(/Log in/)
    await expect(page.getByLabel(/email/i)).toBeVisible()
    await expect(page.getByLabel(/password/i)).toBeVisible()
    await expect(page.getByRole('button', { name: /log in/i })).toBeVisible()
  })

  test('login page has links to register and forgot password', async ({ page }) => {
    await page.goto('/auth/login')
    await expect(page.getByRole('link', { name: /register/i })).toBeVisible()
    await expect(page.getByRole('link', { name: /forgot/i })).toBeVisible()
  })

  test('forgot password page renders', async ({ page }) => {
    await page.goto('/auth/forgot-password')
    await expect(page).toHaveTitle(/Forgot Password/)
    await expect(page.getByLabel(/email/i)).toBeVisible()
  })

  test('reset password page renders with token field', async ({ page }) => {
    await page.goto('/auth/reset-password?token=test-token')
    await expect(page).toHaveTitle(/Reset Password/)
    await expect(page.getByLabel(/new password/i)).toBeVisible()
  })

  test('verify email page handles missing token', async ({ page }) => {
    await page.goto('/auth/verify-email')
    await expect(page.getByText(/invalid|missing|no token/i)).toBeVisible()
  })

  test('check your email page renders', async ({ page }) => {
    await page.goto('/auth/check-your-email')
    await expect(page.getByText(/check your email/i)).toBeVisible()
  })
})

test.describe('Auth navigation', () => {
  test('navbar shows Join Us button when not authenticated', async ({ page }) => {
    await page.goto('/')
    const nav = page.getByRole('navigation')
    await expect(nav.getByRole('link', { name: /join us/i })).toBeVisible()
  })

  test('Join Us links to register page', async ({ page }) => {
    await page.goto('/')
    await page
      .getByRole('navigation')
      .getByRole('link', { name: /join us/i })
      .click()
    await expect(page).toHaveURL(/\/auth\/register/)
  })

  test('unauthenticated user is redirected from /members to login', async ({ page }) => {
    await page.goto('/members')
    await expect(page).toHaveURL(/\/auth\/login/)
  })
})

test.describe('Legal pages', () => {
  test('privacy policy page renders with draft banner', async ({ page }) => {
    await page.goto('/legal/privacy')
    await expect(page).toHaveTitle(/Privacy/)
    await expect(page.getByText(/draft/i)).toBeVisible()
  })

  test('terms page renders with draft banner', async ({ page }) => {
    await page.goto('/legal/terms')
    await expect(page).toHaveTitle(/Terms/)
    await expect(page.getByText(/draft/i)).toBeVisible()
  })
})

test.describe('Membership info page', () => {
  test('membership page explains the join process', async ({ page }) => {
    await page.goto('/about/membership')
    await expect(page).toHaveTitle(/Membership/)
    await expect(page.getByText(/ieee membership/i).first()).toBeVisible()
  })

  test('membership page has a register CTA', async ({ page }) => {
    await page.goto('/about/membership')
    await expect(page.getByRole('link', { name: /register|join|apply/i })).toBeVisible()
  })
})
