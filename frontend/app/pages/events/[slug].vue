<script setup lang="ts">
/**
 * Event detail page ( /events/[slug] )
 *
 * Layout:
 *   ┌──────────────────────────────────────────────────┐
 *   │  Back nav                                        │
 *   ├──────────────────────────┬───────────────────────┤
 *   │                          │                       │
 *   │  Event header            │  Sticky sidebar       │
 *   │  (type badge, title,     │  (date/time card,     │
 *   │   description)           │   location card,      │
 *   │                          │   RSVP button)        │
 *   │  Tags                    │                       │
 *   │                          │                       │
 *   └──────────────────────────┴───────────────────────┘
 *
 * Uses:
 *   - UiBaseCard for sidebar boxes
 *   - UiBaseBadge for type/status/tag badges
 *   - UiBaseButton for RSVP CTA and back navigation
 *   - UiBaseLink for location link
 *
 * TODO: Replace DUMMY_EVENTS lookup with useFetch(`/api/v1/events/${slug}`)
 */
import { DUMMY_EVENTS, EVENT_TYPE_META } from '~/composables/useEvents'

definePageMeta({ layout: 'default' })

const route = useRoute()
const slug = route.params.slug as string

// TODO: fetch real event by slug
// const { data: event } = await useFetch(`/api/v1/events/${slug}`)
const event = DUMMY_EVENTS.find((e) => e.slug === slug)

// 404 guard
if (!event) {
  throw createError({ statusCode: 404, statusMessage: 'Event not found' })
}

const typeMeta = computed(() => EVENT_TYPE_META[event.type])
const isPast = computed(() => event.status === 'past')

useSeoMeta({
  title: event.title,
  description: event.description,
  ogTitle: event.title,
  ogDescription: event.description,
})

// Spots urgency level
const spotsUrgency = computed(() => {
  const left = event.spotsLeft
  if (!left) return null
  if (left <= 3) return 'critical'
  if (left <= 8) return 'low'
  return 'ok'
})

// Related events: same type, excluding current, max 3
const relatedEvents = computed(() =>
  DUMMY_EVENTS.filter((e) => e.type === event.type && e.slug !== event.slug).slice(0, 3)
)
</script>

<template>
  <div class="min-h-screen bg-[var(--color-surface)]">
    <div class="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      <!-- ── Back navigation ────────────────────────────────── -->
      <div class="mb-8">
        <UiBaseLink
          to="/events"
          class="inline-flex items-center gap-2 text-sm font-medium text-[var(--color-text-secondary)] transition-colors duration-150 hover:text-[var(--color-text-primary)] focus-visible:underline focus-visible:outline-none"
        >
          <svg
            class="size-4"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            aria-hidden="true"
          >
            <path stroke-linecap="round" stroke-linejoin="round" d="M19 12H5M12 5l-7 7 7 7" />
          </svg>
          Back to all events
        </UiBaseLink>
      </div>

      <!-- ── Main layout ────────────────────────────────────── -->
      <div class="flex flex-col gap-10 lg:flex-row xl:gap-14">
        <!-- ── Content column ───────────────────────────────── -->
        <article class="min-w-0 max-w-3xl flex-1">
          <!-- Top badges -->
          <div class="mb-5 flex flex-wrap items-center gap-2">
            <UiBaseBadge :variant="typeMeta.badgeVariant">
              {{ typeMeta.label }}
            </UiBaseBadge>
            <UiBaseBadge v-if="!isPast" variant="green" dot> Upcoming </UiBaseBadge>
            <UiBaseBadge v-else variant="default"> Past </UiBaseBadge>
            <UiBaseBadge v-if="event.isHighlighted && !isPast" variant="blue">
              Featured
            </UiBaseBadge>
          </div>

          <!-- Title -->
          <h1
            class="mb-4 text-3xl font-bold leading-tight tracking-tight text-[var(--color-text-primary)] sm:text-4xl"
          >
            {{ event.title }}
          </h1>

          <!-- Speaker (talks only) -->
          <p
            v-if="event.speakerName"
            class="mb-6 text-base font-medium text-[var(--color-ieee-blue)]"
          >
            {{ event.speakerName }}
            <span class="font-normal text-[var(--color-text-muted)]">
              · {{ event.speakerTitle }}
            </span>
          </p>

          <!-- Accent stripe -->
          <div
            :class="[typeMeta.accent, 'mb-8 h-1 w-16 rounded-full']"
            :style="isPast ? 'opacity: 0.4' : ''"
            aria-hidden="true"
          />

          <!-- Description -->
          <div class="prose prose-sm max-w-none text-[var(--color-text-secondary)]">
            <p class="text-base leading-relaxed sm:text-lg">
              {{ event.description }}
            </p>
          </div>

          <!-- Tags -->
          <div v-if="event.tags.length" class="mt-8 flex flex-wrap gap-2" aria-label="Tags">
            <UiBaseBadge v-for="tag in event.tags" :key="tag" variant="default" size="sm">
              #{{ tag.toLowerCase().replace(/\s/g, '-') }}
            </UiBaseBadge>
          </div>

          <!-- Divider -->
          <div class="my-12 flex items-center gap-4">
            <div class="h-px flex-1 bg-[var(--color-border)]" />
            <div
              class="size-1.5 rounded-full"
              style="background-color: var(--color-ieee-blue)"
              aria-hidden="true"
            />
            <div class="h-px flex-1 bg-[var(--color-border)]" />
          </div>

          <!-- Related events -->
          <section v-if="relatedEvents.length" aria-labelledby="related-events-heading">
            <h2
              id="related-events-heading"
              class="mb-6 font-mono text-[11px] uppercase tracking-[0.15em] text-[var(--color-text-muted)]"
            >
              More {{ typeMeta.label }} events
            </h2>
            <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <EventsEventCard
                v-for="(e, i) in relatedEvents"
                :key="e.id"
                :event="e"
                :index="i"
                compact
              />
            </div>
          </section>
        </article>

        <!-- ── Sidebar ──────────────────────────────────────── -->
        <aside class="w-full flex-shrink-0 lg:w-72 xl:w-80" aria-label="Event details">
          <div class="flex flex-col gap-5 lg:sticky lg:top-[calc(var(--nav-height)+2rem)]">
            <!-- Date & Time card -->
            <UiBaseCard padding="sm" flat>
              <p
                class="mb-4 font-mono text-[10px] uppercase tracking-[0.15em] text-[var(--color-text-muted)]"
              >
                Date & Time
              </p>

              <div class="flex flex-col gap-3">
                <div class="flex items-center gap-3">
                  <svg
                    class="size-4 flex-shrink-0 text-[var(--color-text-muted)]"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    aria-hidden="true"
                  >
                    <rect x="3" y="4" width="18" height="18" rx="2" />
                    <line x1="16" y1="2" x2="16" y2="6" />
                    <line x1="8" y1="2" x2="8" y2="6" />
                    <line x1="3" y1="10" x2="21" y2="10" />
                  </svg>
                  <time
                    :datetime="event.dateISO"
                    class="text-sm font-medium text-[var(--color-text-primary)]"
                  >
                    {{ event.dateDisplay }}
                  </time>
                </div>

                <div class="flex items-center gap-3">
                  <svg
                    class="size-4 flex-shrink-0 text-[var(--color-text-muted)]"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    aria-hidden="true"
                  >
                    <circle cx="12" cy="12" r="10" />
                    <polyline points="12,6 12,12 16,14" />
                  </svg>
                  <span class="font-mono text-sm text-[var(--color-text-secondary)]">
                    {{ event.timeDisplay }}
                  </span>
                </div>
              </div>
            </UiBaseCard>

            <!-- Location card -->
            <UiBaseCard padding="sm" flat>
              <p
                class="mb-4 font-mono text-[10px] uppercase tracking-[0.15em] text-[var(--color-text-muted)]"
              >
                Location
              </p>

              <div class="flex items-start gap-3">
                <svg
                  class="mt-0.5 size-4 flex-shrink-0 text-[var(--color-text-muted)]"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  aria-hidden="true"
                >
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z" />
                  <circle cx="12" cy="10" r="3" />
                </svg>
                <div>
                  <UiBaseLink
                    v-if="event.locationUrl"
                    :href="event.locationUrl"
                    external
                    class="text-sm font-medium text-[var(--color-text-primary)] transition-colors duration-150 hover:text-[var(--color-ieee-blue)] hover:underline focus-visible:underline focus-visible:outline-none"
                  >
                    {{ event.location }}
                  </UiBaseLink>
                  <span v-else class="text-sm font-medium text-[var(--color-text-primary)]">
                    {{ event.location }}
                  </span>
                </div>
              </div>
            </UiBaseCard>

            <!-- Capacity card (if applicable) -->
            <UiBaseCard v-if="!isPast && event.capacity" padding="sm" flat>
              <p
                class="mb-4 font-mono text-[10px] uppercase tracking-[0.15em] text-[var(--color-text-muted)]"
              >
                Capacity
              </p>

              <div class="flex items-center gap-3">
                <svg
                  class="size-4 flex-shrink-0 text-[var(--color-text-muted)]"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  aria-hidden="true"
                >
                  <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2" />
                  <circle cx="9" cy="7" r="4" />
                  <path d="M23 21v-2a4 4 0 00-3-3.87" />
                  <path d="M16 3.13a4 4 0 010 7.75" />
                </svg>
                <span
                  :class="[
                    'font-mono text-sm font-medium',
                    spotsUrgency === 'critical' ? 'text-red-500' : '',
                    spotsUrgency === 'low' ? 'text-orange-500' : '',
                    spotsUrgency === 'ok' || !spotsUrgency
                      ? 'text-[var(--color-text-secondary)]'
                      : '',
                  ]"
                >
                  <template v-if="event.spotsLeft !== undefined">
                    <span v-if="spotsUrgency === 'critical'"
                      >Only {{ event.spotsLeft }} spots left!</span
                    >
                    <span v-else>{{ event.spotsLeft }} / {{ event.capacity }} spots available</span>
                  </template>
                  <template v-else> {{ event.capacity }} spots total </template>
                </span>
              </div>

              <!-- Simple capacity bar -->
              <div
                v-if="event.spotsLeft !== undefined && event.capacity"
                class="mt-3 h-1.5 w-full overflow-hidden rounded-full bg-[var(--color-surface-overlay)]"
                role="progressbar"
                :aria-valuenow="event.capacity - event.spotsLeft"
                :aria-valuemin="0"
                :aria-valuemax="event.capacity"
                :aria-label="`${event.capacity - event.spotsLeft} of ${event.capacity} spots filled`"
              >
                <div
                  :class="[
                    'h-full rounded-full transition-all duration-500',
                    spotsUrgency === 'critical' ? 'bg-red-500' : '',
                    spotsUrgency === 'low' ? 'bg-orange-500' : '',
                    spotsUrgency === 'ok' ? 'bg-[var(--color-ieee-blue)]' : '',
                    !spotsUrgency ? 'bg-[var(--color-ieee-blue)]' : '',
                  ]"
                  :style="{
                    width: `${((event.capacity - event.spotsLeft) / event.capacity) * 100}%`,
                  }"
                />
              </div>
            </UiBaseCard>

            <!-- RSVP CTA (upcoming only) -->
            <UiBaseButton
              v-if="!isPast && event.rsvpLink"
              variant="primary"
              size="md"
              :href="event.rsvpLink"
              external
              class="w-full justify-center"
            >
              RSVP for this event
              <svg
                class="size-4"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                aria-hidden="true"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M7 17L17 7M17 7H7M17 7v10"
                />
              </svg>
            </UiBaseButton>

            <!-- Past event notice -->
            <UiBaseCard v-if="isPast" padding="sm" flat>
              <div class="flex items-center gap-3 text-[var(--color-text-muted)]">
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
                <p class="text-xs">This event has already taken place.</p>
              </div>
            </UiBaseCard>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>
