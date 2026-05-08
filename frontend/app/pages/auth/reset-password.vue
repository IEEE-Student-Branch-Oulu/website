<script setup lang="ts">
definePageMeta({ layout: 'default' })
useHead({ title: 'Reset password - IEEE SB Oulu' })

const { api } = useApi()
const route = useRoute()

const password = ref('')
const loading = ref(false)
const success = ref(false)
const error = ref('')

async function submit() {
  const rawToken = route.query.token
  const token = Array.isArray(rawToken) ? rawToken[0] : rawToken

  if (!token) {
    error.value = 'Invalid or missing reset token.'
    return
  }

  if (password.value.length < 12) {
    error.value = 'Password must be at least 12 characters'
    return
  }
  error.value = ''
  loading.value = true
  try {
    await api('/auth/reset-password', {
      method: 'POST',
      body: { token, password: password.value },
    })
    success.value = true
  } catch (e: unknown) {
    const err = e as { detail?: string }
    error.value = err?.detail ?? 'Reset failed. The link may have expired.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="mx-auto max-w-sm px-4 py-16">
    <h1 class="mb-2 text-2xl font-bold text-[var(--color-text-primary)]">Set new password</h1>

    <div v-if="success" class="text-center">
      <p class="mb-6 text-sm text-[var(--color-text-secondary)]">
        Your password has been reset. You can now log in with your new password.
      </p>
      <UiBaseButton href="/auth/login" variant="primary">Log in</UiBaseButton>
    </div>

    <form v-else class="space-y-4" @submit.prevent="submit">
      <div
        v-if="error"
        class="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700 dark:border-red-800 dark:bg-red-950 dark:text-red-300"
        role="alert"
      >
        {{ error }}
      </div>

      <UiFormField label="New password" hint="At least 12 characters" required>
        <template #default="{ id }">
          <UiPasswordInput :id="id" v-model="password" show-strength />
        </template>
      </UiFormField>

      <UiBaseButton type="submit" variant="primary" class="w-full" :loading="loading">
        Reset password
      </UiBaseButton>
    </form>
  </div>
</template>
