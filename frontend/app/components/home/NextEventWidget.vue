<script setup lang="ts">
/**
 * NextEventWidget
 *
 * Featured section for the next upcoming event.
 * Renders a live countdown timer using useCountdown composable.
 *
 * Design:
 *   - Full-width IEEE Blue gradient section — creates strong visual break
 *   - Left: event metadata. Right: monospace countdown + RSVP CTA
 *   - Responsive: stacks on mobile, side-by-side on desktop
 *
 * For V1, event data is hardcoded dummy data.
 * TODO: Replace with `useFetch('/api/v1/events/next')` when API is ready.
 */

// ── Dummy data — replace with API call ───────────────────────
const event = {
  title: 'AI & Machine Learning Workshop',
  description:
    "A hands-on introduction to ML fundamentals. We'll train a simple classifier from scratch using Python and scikit-learn — no prior ML experience required. Bring your laptop.",
  dateISO: '2026-03-15T13:00:00',
  dateDisplay: 'Saturday, March 15, 2026',
  timeDisplay: '13:00 – 17:00 EET',
  location: 'Linnanmaa Campus, Room TS101',
  type: 'Workshop',
  typeVariant: 'orange' as const,
  rsvpLink: 'https://forms.gle/your-rsvp-form',
}

const { formatted, time } = useCountdown(event.dateISO)

const countdownUnits = computed(() => [
  { value: formatted.value.days, label: 'Days' },
  { value: formatted.value.hours, label: 'Hrs' },
  { value: formatted.value.minutes, label: 'Min' },
  { value: formatted.value.seconds, label: 'Sec' },
])
</script>

<template>
  <section
    class="relative overflow-hidden bg-[var(--color-ieee-blue)]"
    aria-labelledby="next-event-heading"
  >
    <!-- Subtle grid overlay on blue bg -->
    <div
      class="next-event-grid pointer-events-none absolute inset-0 opacity-20"
      aria-hidden="true"
    />

    <!-- Blue glow blobs -->
    <div
      class="pointer-events-none absolute -left-20 -top-20 h-72 w-72 rounded-full bg-white/5 blur-3xl"
      aria-hidden="true"
    />
    <div
      class="bg-[var(--color-ieee-blue-dark)]/60 pointer-events-none absolute -bottom-20 -right-20 h-96 w-96 rounded-full blur-3xl"
      aria-hidden="true"
    />

    <div class="relative mx-auto max-w-7xl px-4 py-16 sm:px-6 sm:py-20 lg:px-8">
      <div class="grid grid-cols-1 items-center gap-12 lg:grid-cols-2 lg:gap-16">
        <!-- Left: Event details -->
        <div>
          <!-- Section label -->
          <div class="mb-6 flex items-center gap-3">
            <p class="font-mono text-[11px] uppercase tracking-[0.18em] text-white/60">
              Next Event
            </p>
            <UiBaseBadge variant="green" dot size="sm" class="!bg-emerald-400/20 !text-emerald-200">
              Upcoming
            </UiBaseBadge>
          </div>

          <!-- Event type + title -->
          <div class="mb-2">
            <UiBaseBadge variant="orange" size="sm">{{ event.type }}</UiBaseBadge>
          </div>
          <h2
            id="next-event-heading"
            class="mb-5 text-3xl font-bold leading-tight text-white sm:text-4xl"
          >
            {{ event.title }}
          </h2>

          <!-- Description -->
          <p class="mb-8 max-w-lg text-base leading-relaxed text-white/70">
            {{ event.description }}
          </p>

          <!-- Meta: date + location -->
          <dl class="mb-10 flex flex-col gap-3">
            <div class="flex items-start gap-3">
              <!-- Calendar icon -->
              <svg
                class="mt-0.5 size-4 flex-shrink-0 text-white/50"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                aria-hidden="true"
              >
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
                <line x1="16" y1="2" x2="16" y2="6" />
                <line x1="8" y1="2" x2="8" y2="6" />
                <line x1="3" y1="10" x2="21" y2="10" />
              </svg>
              <div>
                <dt class="sr-only">Date and time</dt>
                <dd class="font-mono text-sm text-white/90">
                  {{ event.dateDisplay }}
                </dd>
                <dd class="mt-0.5 font-mono text-xs text-white/60">
                  {{ event.timeDisplay }}
                </dd>
              </div>
            </div>

            <div class="flex items-start gap-3">
              <!-- Location icon -->
              <svg
                class="mt-0.5 size-4 flex-shrink-0 text-white/50"
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
                <dt class="sr-only">Location</dt>
                <dd class="text-sm text-white/90">{{ event.location }}</dd>
              </div>
            </div>
          </dl>

          <!-- RSVP button -->
          <a
            :href="event.rsvpLink"
            target="_blank"
            rel="noopener noreferrer"
            class="inline-flex items-center gap-2 rounded-lg bg-white px-6 py-3 text-sm font-semibold text-[var(--color-ieee-blue)] transition-all duration-150 hover:bg-white/90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-offset-2 focus-visible:ring-offset-[var(--color-ieee-blue)] active:bg-white/80"
          >
            RSVP — It's Free
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
          </a>
        </div>

        <!-- Right: Countdown timer -->
        <div class="flex flex-col items-start lg:items-end">
          <p class="mb-6 font-mono text-[11px] uppercase tracking-[0.18em] text-white/50">
            Starts in
          </p>

          <!-- Countdown display -->
          <div
            v-if="!time.isExpired"
            class="grid w-full max-w-sm grid-cols-4 gap-3 sm:gap-4 lg:max-w-none"
          >
            <div
              v-for="unit in countdownUnits"
              :key="unit.label"
              class="flex flex-col items-center gap-2"
            >
              <!-- Number -->
              <div
                class="flex aspect-square w-full max-w-[80px] items-center justify-center rounded-xl border border-white/20 bg-white/10 backdrop-blur-sm"
              >
                <span
                  class="font-mono text-2xl font-bold tabular-nums leading-none text-white sm:text-3xl"
                >
                  {{ unit.value }}
                </span>
              </div>
              <!-- Label -->
              <span class="font-mono text-[10px] uppercase tracking-widest text-white/50">
                {{ unit.label }}
              </span>
            </div>
          </div>

          <!-- Expired state -->
          <div v-else class="text-center">
            <p class="font-mono text-lg text-white/70">This event has passed.</p>
            <NuxtLink
              to="/#"
              class="mt-2 block text-sm text-white underline underline-offset-4 hover:text-white/80"
            >
              View all events →
            </NuxtLink>
          </div>

          <!-- Decorative separator -->
          <div class="mt-10 flex w-full max-w-sm items-center gap-3 lg:max-w-none">
            <div class="h-px flex-1 bg-white/10" />
            <span class="font-mono text-[10px] uppercase tracking-widest text-white/30">
              View all events
            </span>
            <NuxtLink
              to="/events"
              class="font-mono text-[10px] text-white/60 transition-colors duration-150 hover:text-white focus-visible:underline focus-visible:outline-none"
            >
              /events →
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.next-event-grid {
  background-image: radial-gradient(circle, rgba(255, 255, 255, 0.15) 1px, transparent 1px);
  background-size: 24px 24px;
}
</style>
