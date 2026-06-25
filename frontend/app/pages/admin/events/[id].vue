<script setup lang="ts">
import { useEventsApi, type EventInput } from '~/composables/useEvents'
import type { ApiError } from '~/composables/useApi'

definePageMeta({ middleware: 'admin' })

const route = useRoute()
const id = Number(route.params.id)

const { getRaw, update } = useEventsApi()
const { data: event, error: loadError } = await useAsyncData(`admin-event-${id}`, () => getRaw(id))

if (loadError.value || !event.value) {
  throw createError({ statusCode: 404, statusMessage: 'Event not found' })
}

useHead({ title: `Edit: ${event.value.title} - IEEE SB Oulu` })

const submitting = ref(false)
const error = ref<string | null>(null)

async function onSubmit(payload: EventInput) {
  submitting.value = true
  error.value = null
  try {
    const updated = await update(id, payload)
    await navigateTo(`/events/${updated.slug}`)
  } catch (e) {
    error.value = (e as ApiError)?.detail ?? 'Failed to update event.'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="mx-auto max-w-4xl px-4 py-16">
    <h1 class="mb-8 text-2xl font-bold text-[var(--color-text-primary)]">Edit event</h1>
    <AdminEventForm :initial="event" :submitting="submitting" :error="error" @submit="onSubmit" />
  </div>
</template>
