<script setup lang="ts">
definePageMeta({ layout: 'default' })
useHead({ title: 'Check your email - IEEE SB Oulu' })
</script>

<template>
  <div class="mx-auto max-w-sm px-4 py-16 text-center">
    <div
      class="mx-auto mb-6 flex size-16 items-center justify-center rounded-full bg-blue-100 dark:bg-blue-900"
    >
      <svg
        class="size-8 text-[var(--color-ieee-blue)]"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        aria-hidden="true"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
        />
      </svg>
    </div>
    <h1 class="mb-2 text-2xl font-bold text-[var(--color-text-primary)]">Check your email</h1>
    <p class="mb-6 text-sm text-[var(--color-text-secondary)]">
      We've sent a verification link to your email address. Click the link to continue your
      membership application.
    </p>
    <p class="text-xs text-[var(--color-text-tertiary)]">
      Didn't receive the email? Check your spam folder or
      <NuxtLink to="/auth/login" class="text-[var(--color-ieee-blue)] hover:underline"
        >log in to resend</NuxtLink
      >.
    </p>
  </div>
</template>
