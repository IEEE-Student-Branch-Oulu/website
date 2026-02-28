<script setup lang="ts">
/**
 * EventFilterBar
 *
 * Filter controls for the events page.
 * Looks like an IDE tab strip — matches the engineering aesthetic.
 *
 * Props:
 *   modelValue - currently active filter key
 *   counts     - { upcoming: number, past: number } for the badges
 *
 * Emits:
 *   update:modelValue - when a filter is selected
 *
 * Usage:
 *   <EventFilterBar v-model="activeFilter" :counts="counts" />
 */

export type EventFilter =
  | 'all'
  | 'upcoming'
  | 'past'
  | 'workshop'
  | 'talk'
  | 'social'
  | 'hackathon'
  | 'meeting'
  | 'excursion'

interface FilterDef {
  key: EventFilter
  label: string
  icon?: string
  group: 'status' | 'type'
}

interface Props {
  modelValue: EventFilter
  counts?: Partial<Record<EventFilter, number>>
}

withDefaults(defineProps<Props>(), { counts: () => ({}) })
const emit = defineEmits<{ 'update:modelValue': [value: EventFilter] }>()

const STATUS_FILTERS: FilterDef[] = [
  { key: 'all', label: 'All Events', group: 'status' },
  { key: 'upcoming', label: 'Upcoming', group: 'status' },
  { key: 'past', label: 'Past', group: 'status' },
]

const TYPE_FILTERS: FilterDef[] = [
  { key: 'workshop', label: 'Workshop', group: 'type' },
  { key: 'talk', label: 'Tech Talk', group: 'type' },
  { key: 'social', label: 'Social', group: 'type' },
  { key: 'hackathon', label: 'Hackathon', group: 'type' },
  { key: 'meeting', label: 'Meeting', group: 'type' },
  { key: 'excursion', label: 'Excursion', group: 'type' },
]

function select(key: EventFilter) {
  emit('update:modelValue', key)
}
</script>

<template>
  <div class="flex flex-col gap-3">
    <!-- Row 1: Status filters -->
    <div
      class="inline-flex w-fit items-center gap-0.5 rounded-lg border border-[var(--color-border)] bg-[var(--color-surface-raised)] p-1"
      role="radiogroup"
      aria-label="Filter by status"
    >
      <button
        v-for="f in STATUS_FILTERS"
        :key="f.key"
        type="button"
        role="radio"
        :aria-checked="modelValue === f.key"
        :class="[
          'relative rounded-md px-4 py-1.5 text-sm font-medium transition-all duration-150',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-ieee-blue)]',
          modelValue === f.key
            ? 'border border-[var(--color-border)] bg-[var(--color-surface)] text-[var(--color-text-primary)] shadow-sm'
            : 'text-[var(--color-text-muted)] hover:bg-[var(--color-surface-overlay)] hover:text-[var(--color-text-primary)]',
        ]"
        @click="select(f.key)"
      >
        {{ f.label }}

        <!-- Count badge -->
        <span
          v-if="counts[f.key] !== undefined"
          :class="[
            'ml-2 rounded-full px-1.5 py-0.5 font-mono text-[10px]',
            modelValue === f.key
              ? 'bg-[var(--color-ieee-blue)]/10 text-[var(--color-ieee-blue)]'
              : 'bg-[var(--color-surface-overlay)] text-[var(--color-text-muted)]',
          ]"
        >
          {{ counts[f.key] }}
        </span>
      </button>
    </div>

    <!-- Row 2: Type filters (chips) -->
    <div class="flex flex-wrap gap-2" role="radiogroup" aria-label="Filter by event type">
      <button
        v-for="f in TYPE_FILTERS"
        :key="f.key"
        type="button"
        role="radio"
        :aria-checked="modelValue === f.key"
        :class="[
          'rounded-full px-3 py-1 font-mono text-xs font-medium uppercase tracking-wider',
          'border transition-all duration-150',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-ieee-blue)]',
          modelValue === f.key
            ? 'border-[var(--color-ieee-blue)] bg-[var(--color-ieee-blue)] text-white'
            : 'hover:border-[var(--color-ieee-blue)]/40 border-[var(--color-border)] bg-transparent text-[var(--color-text-muted)] hover:text-[var(--color-text-primary)]',
        ]"
        @click="select(modelValue === f.key ? 'all' : f.key)"
      >
        {{ f.label }}
      </button>
    </div>
  </div>
</template>
