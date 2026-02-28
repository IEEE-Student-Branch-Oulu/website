<script setup lang="ts">
/**
 * EventsEmptyState
 *
 * Shown when filters return no events.
 * Provides a clear, friendly path back to all events.
 *
 * Uses:
 *   - UiBaseCard for the container
 *   - UiBaseButton for the reset action
 *
 * Props:
 *   activeFilter - current filter key (for contextual message)
 *
 * Emits:
 *   reset - clear filter and show all
 */

interface Props {
  activeFilter?: string
}

withDefaults(defineProps<Props>(), { activeFilter: 'all' })

defineEmits<{ reset: [] }>()
</script>

<template>
  <UiBaseCard
    padding="none"
    class="flex flex-col items-center justify-center border-dashed px-4 py-20 text-center"
  >
    <!-- Icon -->
    <div
      class="mb-5 flex size-14 items-center justify-center rounded-2xl border border-[var(--color-border)] bg-[var(--color-surface-raised)]"
      aria-hidden="true"
    >
      <svg
        class="size-7 text-[var(--color-text-muted)]"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="1.5"
      >
        <circle cx="11" cy="11" r="8" />
        <path stroke-linecap="round" d="M21 21l-4.35-4.35" />
        <path stroke-linecap="round" d="M8 11h6M11 8v6" />
      </svg>
    </div>

    <p class="mb-2 font-mono text-xs uppercase tracking-widest text-[var(--color-text-muted)]">
      No results
    </p>
    <p class="mb-1 text-base font-semibold text-[var(--color-text-primary)]">
      No events match this filter
    </p>
    <p class="mb-6 max-w-xs text-sm text-[var(--color-text-secondary)]">
      Try a different filter or check back later for new events.
    </p>

    <UiBaseButton variant="secondary" size="sm" @click="$emit('reset')">
      <svg
        class="size-4"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        aria-hidden="true"
      >
        <path stroke-linecap="round" d="M3 12a9 9 0 109-9 9.75 9.75 0 00-6.74 2.74L3 8" />
        <path stroke-linecap="round" d="M3 3v5h5" />
      </svg>
      Show all events
    </UiBaseButton>
  </UiBaseCard>
</template>
