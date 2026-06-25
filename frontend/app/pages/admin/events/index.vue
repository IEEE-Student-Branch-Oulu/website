<script setup lang="ts">
import { useEventsApi } from '~/composables/useEvents'

definePageMeta({ middleware: 'admin' })
useHead({ title: 'Manage Events - IEEE SB Oulu' })

const { list, remove } = useEventsApi()
const { data, refresh } = await useAsyncData('admin-events', () => list())
const events = computed(() => data.value?.items ?? [])

const deleting = ref<number | null>(null)

async function onDelete(id: number, title: string) {
  if (!globalThis.confirm(`Delete "${title}"? This cannot be undone.`)) return
  deleting.value = id
  try {
    await remove(id)
    await refresh()
  } finally {
    deleting.value = null
  }
}
</script>

<template>
  <div class="mx-auto max-w-4xl px-4 py-16">
    <div class="mb-8 flex items-center justify-between">
      <h1 class="text-2xl font-bold text-[var(--color-text-primary)]">Events</h1>
      <UiBaseButton href="/admin/events/new" variant="primary" size="sm">New event</UiBaseButton>
    </div>

    <p v-if="!events.length" class="text-sm text-[var(--color-text-secondary)]">
      No events yet. Create your first one.
    </p>

    <ul v-else class="flex flex-col gap-3">
      <li
        v-for="event in events"
        :key="event.id"
        class="flex items-center justify-between gap-4 rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-4"
      >
        <div class="min-w-0">
          <p class="truncate font-medium text-[var(--color-text-primary)]">{{ event.title }}</p>
          <p class="text-xs text-[var(--color-text-muted)]">
            {{ event.dateDisplay }} · {{ event.status }}
          </p>
        </div>
        <div class="flex flex-shrink-0 gap-2">
          <UiBaseButton :href="`/events/${event.slug}`" variant="ghost" size="sm">
            View
          </UiBaseButton>
          <UiBaseButton :href="`/admin/events/${event.id}`" variant="secondary" size="sm">
            Edit
          </UiBaseButton>
          <UiBaseButton
            variant="danger"
            size="sm"
            :loading="deleting === event.id"
            @click="onDelete(event.id, event.title)"
          >
            Delete
          </UiBaseButton>
        </div>
      </li>
    </ul>
  </div>
</template>
