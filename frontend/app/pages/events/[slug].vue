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
 */
import { EVENT_TYPE_META, useEventsApi } from '~/composables/useEvents'
import { useBlogApi } from '~/composables/useBlog'

definePageMeta({ layout: 'default' })

const route = useRoute()
const slug = route.params.slug as string

const { get, list } = useEventsApi()
const { data: eventRef, error } = await useAsyncData(`event-${slug}`, () => get(slug))

// 404 guard
if (error.value || !eventRef.value) {
  throw createError({ statusCode: 404, statusMessage: 'Event not found' })
}

const event = eventRef.value

const typeMeta = computed(() => EVENT_TYPE_META[event.type])
const isPast = computed(() => event.status === 'past')

useSeoMeta({
  title: event.title,
  description: event.description,
  ogTitle: event.title,
  ogDescription: event.description,
})

// Related events: same type, excluding current, max 3
const { data: allEvents } = await useAsyncData('events-related', () => list())
const relatedEvents = computed(() =>
  (allEvents.value?.items ?? [])
    .filter((e) => e.type === event.type && e.slug !== event.slug)
    .slice(0, 3)
)

// Recap post linked to this event (if any).
const { list: listPosts } = useBlogApi()
const { data: recapData } = await useAsyncData(`event-recap-${slug}`, () => listPosts())
const recapPost = computed(() => (recapData.value?.items ?? []).find((p) => p.eventSlug === slug))
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

          <!-- Cover image -->
          <img
            v-if="event.coverImageUrl"
            :src="event.coverImageUrl"
            :alt="event.title"
            class="mb-8 w-full rounded-xl border border-[var(--color-border)] object-cover"
          />

          <!-- Description -->
          <div class="prose prose-sm max-w-none text-[var(--color-text-secondary)]">
            <p class="text-base leading-relaxed sm:text-lg">
              {{ event.description }}
            </p>
          </div>

          <!-- Read the recap (past events with a linked recap post) -->
          <UiBaseButton
            v-if="recapPost"
            variant="secondary"
            size="md"
            :href="`/blog/${recapPost.slug}`"
            class="mt-8"
          >
            Read the recap
            <svg
              class="size-4"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              aria-hidden="true"
            >
              <path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M12 5l7 7-7 7" />
            </svg>
          </UiBaseButton>

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
