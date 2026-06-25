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
  EVENT_TYPE_META,
  useEventsApi,
  type EventFilter,
  type EventItem,
  type EventType,
} from '~/composables/useEvents'

definePageMeta({ layout: 'default' })

useSeoMeta({
  title: 'Events',
  description: 'All IEEE Oulu workshops, tech talks, socials, and meetups — past and upcoming.',
})

// ── Data ───────────────────────────────────────────────────────
const { list } = useEventsApi()
const { data } = await useAsyncData('events', () => list())
const events = computed<EventItem[]>(() => data.value?.items ?? [])

// ── Filter state ───────────────────────────────────────────────
const activeFilter = ref<EventFilter>('upcoming')

// ── Computed: filtered + sorted events ────────────────────────
const allEvents = computed<EventItem[]>(() =>
  [...events.value].sort((a, b) => new Date(b.dateISO).getTime() - new Date(a.dateISO).getTime())
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
  all: events.value.length,
  upcoming: events.value.filter((e) => e.status === 'upcoming').length,
  past: events.value.filter((e) => e.status === 'past').length,
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
                  to="/about/membership"
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
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
                  </svg>
                  Become a member
                </UiBaseLink>
                <UiBaseLink
                  href="https://www.linkedin.com/company/ieeesb-oulu"
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
                      d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"
                    />
                  </svg>
                  Follow on LinkedIn
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
