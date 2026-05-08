<script setup lang="ts">
definePageMeta({ layout: 'default' })

useHead({ title: 'Log in - IEEE SB Oulu' })

const { login } = useAuth()
const route = useRoute()

const form = reactive({ email: '', password: '' })
const loading = ref(false)
const error = ref('')

async function submit() {
  error.value = ''
  loading.value = true
  try {
    await login(form.email, form.password)
    const next = (route.query.next as string) || '/members'
    await navigateTo(next)
  } catch (e: unknown) {
    const err = e as { detail?: string }
    error.value = err?.detail ?? 'Invalid credentials.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="mx-auto max-w-sm px-4 py-16">
    <h1 class="mb-2 text-2xl font-bold text-[var(--color-text-primary)]">Log in</h1>
    <p class="mb-8 text-sm text-[var(--color-text-secondary)]">Welcome back to IEEE SB Oulu</p>

    <div
      v-if="error"
      class="mb-4 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700 dark:border-red-800 dark:bg-red-950 dark:text-red-300"
      role="alert"
    >
      {{ error }}
    </div>

    <form class="space-y-4" @submit.prevent="submit">
      <UiFormField label="Email" required>
        <template #default="{ id }">
          <UiInputField :id="id" v-model="form.email" type="email" placeholder="you@example.com" />
        </template>
      </UiFormField>

      <UiFormField label="Password" required>
        <template #default="{ id }">
          <UiPasswordInput :id="id" v-model="form.password" placeholder="Your password" />
        </template>
      </UiFormField>

      <div class="text-right">
        <NuxtLink
          to="/auth/forgot-password"
          class="text-sm text-[var(--color-ieee-blue)] hover:underline"
        >
          Forgot password?
        </NuxtLink>
      </div>

      <UiBaseButton type="submit" variant="primary" class="w-full" :loading="loading">
        Log in
      </UiBaseButton>
    </form>

    <p class="mt-6 text-center text-sm text-[var(--color-text-secondary)]">
      Don't have an account?
      <NuxtLink to="/auth/register" class="text-[var(--color-ieee-blue)] hover:underline"
        >Register</NuxtLink
      >
    </p>
  </div>
</template>
