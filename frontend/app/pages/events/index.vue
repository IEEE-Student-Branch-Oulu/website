<script setup lang="ts">
/**
 * Events Page ( /events )
 *
 * Layout:
 *   ┌─────────────────────────────────────────┐
 *   │  Page header (UiSectionHeader) + stats  │
 *   ├─────────────────────────────────────────┤
 *   │  FilterBar                              │
 *   ├──────────────────────┬──────────────────┤
 *   │                      │                  │
 *   │  Events grid         │  Calendar        │
 *   │  (main, 2/3 width)   │  placeholder     │
 *   │                      │  (sticky, 1/3)   │
 *   │                      │                  │
 *   └──────────────────────┴──────────────────┘
 *
 * On mobile: stacks vertically, calendar below filter.
 * Upcoming events always render before past events in the list.
 *
 * Uses:
 *   - UiSectionHeader for the page heading (eyebrow + title + subtitle)
 *   - UiBaseCard for sidebar boxes (quick links, event type legend)
 *   - UiBaseLink for sidebar quick links (internal + external)
 *   - UiBaseBadge for section count indicators
 */

import {
  DUMMY_EVENTS,
  EVENT_TYPE_META,
  type EventFilter,
  type EventItem,
  type EventType,
} from '~/composables/useEvents'

definePageMeta({ layout: 'default' })

useSeoMeta({
  title: 'Events',
  description: 'All IEEE Oulu workshops, tech talks, socials, and meetups — past and upcoming.',
})

// ── Filter state ───────────────────────────────────────────────
const activeFilter = ref<EventFilter>('upcoming')

// ── Computed: filtered + sorted events ────────────────────────
const allEvents = computed<EventItem[]>(() =>
  [...DUMMY_EVENTS].sort((a, b) => new Date(b.dateISO).getTime() - new Date(a.dateISO).getTime())
)

const filteredEvents = computed<EventItem[]>(() => {
  const f = activeFilter.value
  if (f === 'all') return allEvents.value
  if (f === 'upcoming' || f === 'past') return allEvents.value.filter((e) => e.status === f)
  return allEvents.value.filter((e) => e.type === (f as EventType))
})

// Upcoming always first, past after
const sortedFilteredEvents = computed<EventItem[]>(() => {
  const upcoming = filteredEvents.value
    .filter((e) => e.status === 'upcoming')
    .sort((a, b) => new Date(a.dateISO).getTime() - new Date(b.dateISO).getTime())
  const past = filteredEvents.value
    .filter((e) => e.status === 'past')
    .sort((a, b) => new Date(b.dateISO).getTime() - new Date(a.dateISO).getTime())
  return [...upcoming, ...past]
})

// ── Counts for filter badges ───────────────────────────────────
const counts = computed(() => ({
  all: DUMMY_EVENTS.length,
  upcoming: DUMMY_EVENTS.filter((e) => e.status === 'upcoming').length,
  past: DUMMY_EVENTS.filter((e) => e.status === 'past').length,
}))

// ── Visible section headings ───────────────────────────────────
const hasUpcoming = computed(() => sortedFilteredEvents.value.some((e) => e.status === 'upcoming'))
const hasPast = computed(() => sortedFilteredEvents.value.some((e) => e.status === 'past'))

const upcomingEvents = computed(() =>
  sortedFilteredEvents.value.filter((e) => e.status === 'upcoming')
)
const pastEvents = computed(() => sortedFilteredEvents.value.filter((e) => e.status === 'past'))

function resetFilter() {
  activeFilter.value = 'all'
}

// ── Reveal for page header ─────────────────────────────────────
const { el: headerEl, isVisible: headerVisible } = useReveal(0.1)
</script>

<template>
  <div class="min-h-screen bg-[var(--color-surface)]">
    <!-- ── Page header ──────────────────────────────────────── -->
    <div class="border-b border-[var(--color-border)] bg-[var(--color-surface-raised)]">
      <div class="mx-auto max-w-7xl px-4 py-12 sm:px-6 sm:py-16 lg:px-8">
        <div
          ref="headerEl"
          class="transition-all duration-500"
          :style="{
            opacity: headerVisible ? 1 : 0,
            transform: headerVisible ? 'translateY(0)' : 'translateY(12px)',
          }"
        >
          <div class="flex flex-col gap-6 sm:flex-row sm:items-end sm:justify-between">
            <!-- Section header — reusable component -->
            <UiSectionHeader
              eyebrow="IEEE Oulu · Events"
              title="Events & Meetups"
              subtitle="Workshops, tech talks, hackathons, and socials. All open to University of Oulu students."
              :level="1"
            />

            <!-- Stats -->
            <dl class="flex flex-shrink-0 gap-8">
              <div class="text-center">
                <dt
                  class="font-mono text-[10px] uppercase tracking-widest text-[var(--color-text-muted)]"
                >
                  Upcoming
                </dt>
                <dd class="font-mono text-3xl font-bold text-[var(--color-ieee-blue)]">
                  {{ counts.upcoming }}
                </dd>
              </div>
              <div class="text-center">
                <dt
                  class="font-mono text-[10px] uppercase tracking-widest text-[var(--color-text-muted)]"
                >
                  Total
                </dt>
                <dd class="font-mono text-3xl font-bold text-[var(--color-text-primary)]">
                  {{ counts.all }}
                </dd>
              </div>
            </dl>
          </div>
        </div>
      </div>
    </div>

    <!-- ── Main content ─────────────────────────────────────── -->
    <div class="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      <div class="flex flex-col gap-10 lg:flex-row">
        <!-- Left column: filters + event list (grows) -->
        <div class="min-w-0 flex-1">
          <!-- Filter bar -->
          <div class="mb-8">
            <EventsEventFilterBar v-model="activeFilter" :counts="counts" />
          </div>

          <!-- Results count -->
          <p class="mb-6 font-mono text-xs text-[var(--color-text-muted)]">
            <span class="font-semibold text-[var(--color-text-primary)]">{{
              sortedFilteredEvents.length
            }}</span>
            {{ sortedFilteredEvents.length === 1 ? 'event' : 'events' }} found
          </p>

          <!-- Empty state -->
          <EventsEventsEmptyState
            v-if="sortedFilteredEvents.length === 0"
            :active-filter="activeFilter"
            @reset="resetFilter"
          />

          <!-- Events list -->
          <div v-else class="flex flex-col gap-10">
            <!-- ── Upcoming section ── -->
            <section v-if="hasUpcoming" aria-labelledby="upcoming-heading">
              <div class="mb-5 flex items-center gap-4">
                <h2
                  id="upcoming-heading"
                  class="font-mono text-[11px] uppercase tracking-[0.15em] text-[var(--color-text-muted)]"
                >
                  Upcoming
                </h2>
                <div class="h-px flex-1 bg-[var(--color-border)]" aria-hidden="true" />
                <UiBaseBadge variant="green" dot>{{ upcomingEvents.length }}</UiBaseBadge>
              </div>

              <div class="grid grid-cols-1 gap-5 xl:grid-cols-2">
                <EventsEventCard
                  v-for="(event, i) in upcomingEvents"
                  :key="event.id"
                  :event="event"
                  :index="i"
                  :class="event.isHighlighted ? 'xl:col-span-2' : ''"
                />
              </div>
            </section>

            <!-- Separator between upcoming and past -->
            <div v-if="hasUpcoming && hasPast" class="flex items-center gap-4" aria-hidden="true">
              <div class="h-px flex-1 bg-[var(--color-border)]" />
              <span
                class="px-2 font-mono text-[10px] uppercase tracking-widest text-[var(--color-text-muted)]"
              >
                Past events
              </span>
              <div class="h-px flex-1 bg-[var(--color-border)]" />
            </div>

            <!-- ── Past section ── -->
            <section v-if="hasPast" aria-labelledby="past-heading">
              <div class="mb-5 flex items-center gap-4">
                <h2
                  id="past-heading"
                  class="font-mono text-[11px] uppercase tracking-[0.15em] text-[var(--color-text-muted)]"
                >
                  Archive
                </h2>
                <div class="h-px flex-1 bg-[var(--color-border)]" aria-hidden="true" />
                <span class="font-mono text-[10px] text-[var(--color-text-muted)]">
                  {{ pastEvents.length }}
                </span>
              </div>

              <div class="grid grid-cols-1 gap-4 xl:grid-cols-2">
                <EventsEventCard
                  v-for="(event, i) in pastEvents"
                  :key="event.id"
                  :event="event"
                  :index="i"
                />
              </div>
            </section>
          </div>
        </div>

        <!-- Right column: calendar (sticky, 1/3) -->
        <aside class="w-full flex-shrink-0 lg:w-80 xl:w-96" aria-label="Calendar sidebar">
          <div class="flex flex-col gap-5 lg:sticky lg:top-[calc(var(--nav-height)+1.5rem)]">
            <!-- Calendar placeholder -->
            <EventsCalendarPlaceholder />

            <!-- Quick links box — uses UiBaseCard + UiBaseLink -->
            <UiBaseCard padding="sm" flat>
              <p
                class="mb-4 px-1 font-mono text-[10px] uppercase tracking-widest text-[var(--color-text-muted)]"
              >
                Quick Links
              </p>
              <div class="flex flex-col gap-1">
                <UiBaseLink
                  href="https://discord.gg/your-server"
                  external
                  class="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-[var(--color-text-secondary)] transition-all duration-150 hover:bg-[var(--color-surface-overlay)] hover:text-[var(--color-text-primary)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-ieee-blue)]"
                >
                  <svg
                    class="size-4 flex-shrink-0"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                    aria-hidden="true"
                  >
                    <path
                      d="M20.317 4.37a19.791 19.791 0 00-4.885-1.515.074.074 0 00-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 00-5.487 0 12.64 12.64 0 00-.617-1.25.077.077 0 00-.079-.037A19.736 19.736 0 003.677 4.37a.07.07 0 00-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 00.031.057 19.9 19.9 0 005.993 3.03.078.078 0 00.084-.028c.462-.63.874-1.295 1.226-1.994a.076.076 0 00-.041-.106 13.107 13.107 0 01-1.872-.892.077.077 0 01-.008-.128 10.2 10.2 0 00.372-.292.074.074 0 01.077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 01.078.01c.12.098.246.198.373.292a.077.077 0 01-.006.127 12.299 12.299 0 01-1.873.892.077.077 0 00-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 00.084.028 19.839 19.839 0 006.002-3.03.077.077 0 00.032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 00-.031-.03z"
                    />
                  </svg>
                  Get notified on Discord
                </UiBaseLink>
                <UiBaseLink
                  href="https://t.me/your-channel"
                  external
                  class="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-[var(--color-text-secondary)] transition-all duration-150 hover:bg-[var(--color-surface-overlay)] hover:text-[var(--color-text-primary)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-ieee-blue)]"
                >
                  <svg
                    class="size-4 flex-shrink-0"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                    aria-hidden="true"
                  >
                    <path
                      d="M11.944 0A12 12 0 000 12a12 12 0 0012 12 12 12 0 0012-12A12 12 0 0012 0a12 12 0 00-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 01.171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"
                    />
                  </svg>
                  Follow on Telegram
                </UiBaseLink>
                <UiBaseLink
                  to="/#"
                  class="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-[var(--color-text-secondary)] transition-all duration-150 hover:bg-[var(--color-surface-overlay)] hover:text-[var(--color-text-primary)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-ieee-blue)]"
                >
                  <svg
                    class="size-4 flex-shrink-0"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    aria-hidden="true"
                  >
                    <circle cx="12" cy="12" r="10" />
                    <path stroke-linecap="round" d="M12 8h.01M12 12v4" />
                  </svg>
                  About IEEE Oulu
                </UiBaseLink>
              </div>
            </UiBaseCard>

            <!-- Type legend — uses UiBaseCard -->
            <UiBaseCard padding="sm" flat>
              <p
                class="mb-4 px-1 font-mono text-[10px] uppercase tracking-widest text-[var(--color-text-muted)]"
              >
                Event Types
              </p>
              <dl class="flex flex-col gap-2.5 px-1">
                <div
                  v-for="(meta, type) in EVENT_TYPE_META"
                  :key="type"
                  class="flex items-center gap-2.5"
                >
                  <div
                    :class="['h-2 w-2 flex-shrink-0 rounded-full', meta.accent]"
                    aria-hidden="true"
                  />
                  <dt class="sr-only">{{ meta.label }}</dt>
                  <dd class="text-xs text-[var(--color-text-secondary)]">{{ meta.label }}</dd>
                </div>
              </dl>
            </UiBaseCard>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>
