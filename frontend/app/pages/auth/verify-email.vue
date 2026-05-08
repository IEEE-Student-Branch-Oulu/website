<script setup lang="ts">
definePageMeta({ layout: 'default' })
useHead({ title: 'Verify email - IEEE SB Oulu' })

const { api } = useApi()
const route = useRoute()

const status = ref<'loading' | 'success' | 'error'>('loading')
const errorMessage = ref('')

onMounted(async () => {
  const token = route.query.token as string
  if (!token) {
    status.value = 'error'
    errorMessage.value = 'No verification token provided.'
    return
  }
  try {
    await api('/auth/verify-email', { method: 'POST', body: { token } })
    status.value = 'success'
  } catch (e: unknown) {
    status.value = 'error'
    const err = e as { detail?: string }
    errorMessage.value = err?.detail ?? 'Verification failed.'
  }
})
</script>

<template>
  <div class="mx-auto max-w-sm px-4 py-16 text-center">
    <div v-if="status === 'loading'" class="text-[var(--color-text-secondary)]">
      Verifying your email...
    </div>

    <div v-else-if="status === 'success'">
      <div
        class="mx-auto mb-6 flex size-16 items-center justify-center rounded-full bg-green-100 dark:bg-green-900"
      >
        <svg
          class="size-8 text-green-600"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M5 13l4 4L19 7"
          />
        </svg>
      </div>
      <h1 class="mb-2 text-2xl font-bold text-[var(--color-text-primary)]">Email verified!</h1>
      <p class="mb-6 text-sm text-[var(--color-text-secondary)]">
        Your application has been submitted for board review. We'll notify you when a decision is
        made.
      </p>
      <UiBaseButton href="/auth/login" variant="primary">Log in</UiBaseButton>
    </div>

    <div v-else>
      <div
        class="mx-auto mb-6 flex size-16 items-center justify-center rounded-full bg-red-100 dark:bg-red-900"
      >
        <svg
          class="size-8 text-red-600"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M6 18L18 6M6 6l12 12"
          />
        </svg>
      </div>
      <h1 class="mb-2 text-2xl font-bold text-[var(--color-text-primary)]">Verification failed</h1>
      <p class="mb-6 text-sm text-red-500">{{ errorMessage }}</p>
      <UiBaseButton href="/auth/login" variant="secondary">Go to login</UiBaseButton>
    </div>
  </div>
</template>
