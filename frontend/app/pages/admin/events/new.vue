<script setup lang="ts">
import { useEventsApi, type EventInput } from '~/composables/useEvents'
import type { ApiError } from '~/composables/useApi'

definePageMeta({ middleware: 'admin' })
useHead({ title: 'New event - IEEE SB Oulu' })

const { create } = useEventsApi()
const submitting = ref(false)
const error = ref<string | null>(null)

async function onSubmit(payload: EventInput) {
  submitting.value = true
  error.value = null
  try {
    const event = await create(payload)
    await navigateTo(`/events/${event.slug}`)
  } catch (e) {
    error.value = (e as ApiError)?.detail ?? 'Failed to create event.'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="mx-auto max-w-4xl px-4 py-16">
    <h1 class="mb-8 text-2xl font-bold text-[var(--color-text-primary)]">New event</h1>
    <AdminEventForm :submitting="submitting" :error="error" @submit="onSubmit" />
  </div>
</template>
