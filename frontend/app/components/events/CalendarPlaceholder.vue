<script setup lang="ts">
/**
 * CalendarPlaceholder
 *
 * Reserved visual space for the calendar feature.
 * Designed to look like a genuine teaser, not a broken feature.
 * When the calendar is implemented, delete this component
 * and render <EventCalendar /> in its place on the events page.
 *
 * Uses:
 *   - UiBaseCard for the outer container
 *   - UiBaseBadge for the "Coming Soon" label
 *
 * No props.
 */

// Generate a static "ghost" calendar grid so it looks like real UI
const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

// A fake March 2026 grid
const WEEKS = [
  [null, null, null, null, null, 1, 2],
  [3, 4, 5, 6, 7, 8, 9],
  [10, 11, 12, 13, 14, 15, 16],
  [17, 18, 19, 20, 21, 22, 23],
  [24, 25, 26, 27, 28, 29, 30],
  [31, null, null, null, null, null, null],
]

// Days that "have events" in the ghost UI
const GHOST_EVENT_DAYS = new Set([4, 8, 15, 17, 22, 29])
const TODAY = 10
</script>

<template>
  <section aria-label="Calendar — coming soon">
    <UiBaseCard padding="none" class="relative overflow-hidden border-dashed">
      <!-- Frosted overlay -->
      <div
        class="bg-[var(--color-surface)]/80 dark:bg-[var(--color-surface)]/85 absolute inset-0 z-10 flex flex-col items-center justify-center gap-4 backdrop-blur-[2px]"
      >
        <!-- Icon -->
        <div
          class="bg-[var(--color-ieee-blue)]/10 border-[var(--color-ieee-blue)]/20 flex size-12 items-center justify-center rounded-xl border"
          aria-hidden="true"
        >
          <svg
            class="size-6 text-[var(--color-ieee-blue)]"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.5"
          >
            <rect x="3" y="4" width="18" height="18" rx="2" />
            <line x1="16" y1="2" x2="16" y2="6" />
            <line x1="8" y1="2" x2="8" y2="6" />
            <line x1="3" y1="10" x2="21" y2="10" />
            <path stroke-linecap="round" d="M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01" />
          </svg>
        </div>

        <!-- Label -->
        <div class="flex flex-col items-center text-center">
          <UiBaseBadge variant="blue" dot class="mb-2"> Coming Soon </UiBaseBadge>
          <p class="text-sm font-semibold text-[var(--color-text-primary)]">Interactive Calendar</p>
          <p class="mt-1 max-w-xs text-xs text-[var(--color-text-muted)]">
            Browse and filter events in a full calendar view.
          </p>
        </div>
      </div>

      <!-- Ghost calendar (blurred background) aria-hidden — purely decorative -->
      <div class="pointer-events-none select-none p-5" aria-hidden="true">
        <!-- Ghost header -->
        <div class="mb-5 flex items-center justify-between opacity-40">
          <div class="flex items-center gap-3">
            <div
              class="size-7 rounded border border-[var(--color-border)] bg-[var(--color-surface-overlay)]"
            />
            <span class="font-mono text-sm font-bold text-[var(--color-text-primary)]"
              >March 2026</span
            >
            <div
              class="size-7 rounded border border-[var(--color-border)] bg-[var(--color-surface-overlay)]"
            />
          </div>
          <div class="flex gap-1">
            <div class="h-6 w-14 rounded bg-[var(--color-surface-overlay)]" />
            <div class="h-6 w-10 rounded bg-[var(--color-surface-overlay)]" />
          </div>
        </div>

        <!-- Day headers -->
        <div class="mb-2 grid grid-cols-7 opacity-35">
          <div
            v-for="day in DAYS"
            :key="day"
            class="py-1 text-center font-mono text-[10px] uppercase tracking-wider text-[var(--color-text-muted)]"
          >
            {{ day }}
          </div>
        </div>

        <!-- Calendar grid -->
        <div class="grid grid-cols-7 gap-1 opacity-35">
          <template v-for="(week, wi) in WEEKS" :key="wi">
            <div
              v-for="(day, di) in week"
              :key="`${wi}-${di}`"
              :class="[
                'relative flex aspect-square flex-col items-center justify-center rounded-lg',
                day === null && 'invisible',
                day === TODAY &&
                  'bg-[var(--color-ieee-blue)]/15 border-[var(--color-ieee-blue)]/30 border',
                day !== TODAY && day !== null && 'hover:bg-[var(--color-surface-overlay)]',
              ]"
            >
              <span
                :class="[
                  'font-mono text-xs',
                  day === TODAY
                    ? 'font-bold text-[var(--color-ieee-blue)]'
                    : 'text-[var(--color-text-secondary)]',
                ]"
                >{{ day }}</span
              >
              <!-- Event dot -->
              <div
                v-if="day && GHOST_EVENT_DAYS.has(day)"
                class="bg-[var(--color-ieee-blue)]/60 absolute bottom-1 size-1 rounded-full"
              />
            </div>
          </template>
        </div>
      </div>
    </UiBaseCard>
  </section>
</template>
