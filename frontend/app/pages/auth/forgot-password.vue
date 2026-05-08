<script setup lang="ts">
definePageMeta({ layout: 'default' })
useHead({ title: 'Forgot password - IEEE SB Oulu' })

const { api } = useApi()
const email = ref('')
const submitted = ref(false)
const loading = ref(false)

async function submit() {
  loading.value = true
  try {
    await api('/auth/forgot-password', { method: 'POST', body: { email: email.value } })
  } catch {
    // Always show success to prevent enumeration
  } finally {
    loading.value = false
    submitted.value = true
  }
}
</script>

<template>
  <div class="mx-auto max-w-sm px-4 py-16">
    <h1 class="mb-2 text-2xl font-bold text-[var(--color-text-primary)]">Reset password</h1>

    <div v-if="!submitted">
      <p class="mb-6 text-sm text-[var(--color-text-secondary)]">
        Enter your email address and we'll send you a reset link.
      </p>
      <form class="space-y-4" @submit.prevent="submit">
        <UiFormField label="Email" required>
          <template #default="{ id }">
            <UiInputField :id="id" v-model="email" type="email" placeholder="you@example.com" />
          </template>
        </UiFormField>
        <UiBaseButton type="submit" variant="primary" class="w-full" :loading="loading">
          Send reset link
        </UiBaseButton>
      </form>
    </div>

    <div v-else class="text-center">
      <p class="mb-6 text-sm text-[var(--color-text-secondary)]">
        If an account exists with that email, we've sent a password reset link. Check your inbox.
      </p>
    </div>

    <p class="mt-6 text-center text-sm text-[var(--color-text-secondary)]">
      <NuxtLink to="/auth/login" class="text-[var(--color-ieee-blue)] hover:underline"
        >Back to login</NuxtLink
      >
    </p>
  </div>
</template>
