<script setup lang="ts">
/**
 * EventCard
 *
 * The primary event display unit for the events page.
 *
 * Design language:
 *   - Left accent stripe colored by event type
 *   - Date "stamp" top-right — like a postmark or mission tag
 *   - Upcoming: full color, glowing border on hover, RSVP CTA
 *   - Past: slightly muted, "View Recap" CTA if available
 *   - Featured/highlighted events get a subtle top glow
 *
 * Props:
 *   event - EventItem object
 *   index - position in list (for stagger animation)
 *   compact - smaller variant for side column
 *
 * Usage:
 *   <EventCard :event="event" :index="0" />
 *   <EventCard :event="event" compact />
 */
import { EVENT_TYPE_META, type EventItem } from '~/composables/useEvents'

interface Props {
  event: EventItem
  index?: number
  compact?: boolean
}

const props = withDefaults(defineProps<Props>(), { index: 0, compact: false })

const { el, isVisible } = useReveal()
const typeMeta = computed(() => EVENT_TYPE_META[props.event.type])

const delayMs = computed(() => Math.min(props.index * 80, 400))

// Spots urgency level
const spotsUrgency = computed(() => {
  const left = props.event.spotsLeft
  if (!left) return null
  if (left <= 3) return 'critical'
  if (left <= 8) return 'low'
  return 'ok'
})

const isPast = computed(() => props.event.status === 'past')
</script>

<template>
  <article
    ref="el"
    class="group relative transition-all duration-500"
    :style="{
      opacity: isVisible ? 1 : 0,
      transform: isVisible ? 'translateY(0)' : 'translateY(18px)',
      transitionDelay: `${delayMs}ms`,
    }"
    :aria-label="event.title"
  >
    <!-- Highlighted glow (upcoming featured only) -->
    <div
      v-if="event.isHighlighted && !isPast"
      class="from-[var(--color-ieee-blue)]/20 absolute -inset-px rounded-xl bg-gradient-to-br to-transparent opacity-0 blur-sm transition-opacity duration-300 group-hover:opacity-100"
      aria-hidden="true"
    />

    <!-- Card shell -->
    <div
      :class="[
        'relative flex overflow-hidden rounded-xl border transition-all duration-200',
        isPast
          ? 'border-[var(--color-border)] bg-[var(--color-surface)] opacity-75 hover:opacity-100'
          : 'hover:border-[var(--color-ieee-blue)]/40 border-[var(--color-border)] bg-[var(--color-surface)] hover:-translate-y-0.5 hover:shadow-lg',
        event.isHighlighted && !isPast && 'border-[var(--color-ieee-blue)]/25',
        compact ? 'flex-row items-stretch' : 'flex-col',
      ]"
    >
      <!-- Left accent stripe -->
      <div
        :class="[
          typeMeta.accent,
          'flex-shrink-0',
          compact ? 'w-1 rounded-l-xl' : 'h-1 w-full rounded-t-xl',
          isPast && 'opacity-40',
        ]"
        aria-hidden="true"
      />

      <!-- Content -->
      <div :class="['flex flex-1 flex-col', compact ? 'p-4' : 'p-5 sm:p-6']">
        <!-- Top row: badges + date stamp -->
        <div class="mb-4 flex items-start justify-between gap-3">
          <!-- Left: type + status badges -->
          <div class="flex flex-wrap items-center gap-2">
            <UiBaseBadge :variant="typeMeta.badgeVariant">
              {{ typeMeta.label }}
            </UiBaseBadge>
            <UiBaseBadge v-if="!isPast" variant="green" dot> Upcoming </UiBaseBadge>
            <UiBaseBadge v-else variant="default"> Past </UiBaseBadge>
          </div>

          <!-- Right: Date stamp -->
          <div
            :class="[
              'flex-shrink-0 text-right font-mono leading-tight',
              isPast ? 'opacity-50' : '',
            ]"
            aria-hidden="true"
          >
            <p class="text-[10px] uppercase tracking-widest text-[var(--color-text-muted)]">
              {{ event.dateDisplay.split(',')[0] }}
            </p>
            <p class="text-sm font-bold text-[var(--color-text-primary)]">
              {{ event.dateDisplay.split(', ')[1] }}
            </p>
          </div>
        </div>

        <!-- Title -->
        <h3
          :class="[
            'mb-2 font-bold leading-snug',
            compact ? 'text-sm' : 'text-lg sm:text-xl',
            isPast
              ? 'text-[var(--color-text-secondary)]'
              : 'text-[var(--color-text-primary)] transition-colors duration-150 group-hover:text-[var(--color-ieee-blue)]',
          ]"
        >
          {{ event.title }}
        </h3>

        <!-- Speaker (talks only) -->
        <p
          v-if="event.speakerName && !compact"
          class="mb-2 text-sm font-medium text-[var(--color-ieee-blue)]"
        >
          {{ event.speakerName }}
          <span class="font-normal text-[var(--color-text-muted)]">
            · {{ event.speakerTitle }}</span
          >
        </p>

        <!-- Description -->
        <p
          v-if="!compact"
          class="mb-5 line-clamp-2 text-sm leading-relaxed text-[var(--color-text-secondary)]"
        >
          {{ event.description }}
        </p>

        <!-- Meta row: time + location -->
        <dl :class="['flex flex-col gap-1.5', compact ? 'mb-3' : 'mb-5']">
          <!-- Time -->
          <div class="flex items-center gap-2">
            <svg
              class="size-3.5 flex-shrink-0 text-[var(--color-text-muted)]"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              aria-hidden="true"
            >
              <circle cx="12" cy="12" r="10" />
              <polyline points="12,6 12,12 16,14" />
            </svg>
            <dt class="sr-only">Time</dt>
            <dd class="font-mono text-xs text-[var(--color-text-secondary)]">
              {{ event.timeDisplay }}
            </dd>
          </div>

          <!-- Location -->
          <div class="flex items-center gap-2">
            <svg
              class="size-3.5 flex-shrink-0 text-[var(--color-text-muted)]"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              aria-hidden="true"
            >
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z" />
              <circle cx="12" cy="10" r="3" />
            </svg>
            <dt class="sr-only">Location</dt>
            <dd class="truncate text-xs text-[var(--color-text-secondary)]">
              <a
                v-if="event.locationUrl"
                :href="event.locationUrl"
                target="_blank"
                rel="noopener noreferrer"
                class="transition-colors duration-150 hover:text-[var(--color-ieee-blue)] hover:underline focus-visible:underline focus-visible:outline-none"
                @click.stop
                >{{ event.location }}</a
              >
              <span v-else>{{ event.location }}</span>
            </dd>
          </div>
        </dl>

        <!-- Tags -->
        <div
          v-if="event.tags.length && !compact"
          class="mb-5 flex flex-wrap gap-1.5"
          aria-label="Tags"
        >
          <span
            v-for="tag in event.tags"
            :key="tag"
            class="rounded border border-[var(--color-border)] px-1.5 py-0.5 font-mono text-[10px] text-[var(--color-text-muted)]"
          >
            #{{ tag.toLowerCase().replace(/\s/g, '-') }}
          </span>
        </div>

        <!-- Footer: spots left + CTA -->
        <div
          class="mt-auto flex items-center justify-between gap-4 border-t border-[var(--color-border-subtle)] pt-4"
        >
          <!-- Spots left indicator -->
          <div v-if="!isPast && event.spotsLeft !== undefined" class="flex items-center gap-1.5">
            <svg
              class="size-3.5"
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
                'font-mono text-xs font-medium',
                spotsUrgency === 'critical' ? 'text-red-500' : '',
                spotsUrgency === 'low' ? 'text-orange-500' : '',
                spotsUrgency === 'ok' ? 'text-[var(--color-text-muted)]' : '',
              ]"
            >
              <span v-if="spotsUrgency === 'critical'">Only {{ event.spotsLeft }} spots left!</span>
              <span v-else-if="spotsUrgency === 'low'">{{ event.spotsLeft }} spots left</span>
              <span v-else>{{ event.spotsLeft }} / {{ event.capacity }} spots</span>
            </span>
          </div>

          <!-- Past: read recap label -->
          <div v-else-if="isPast" class="font-mono text-xs text-[var(--color-text-muted)]">
            Archived
          </div>

          <div v-else class="flex-1" />

          <!-- CTA -->
          <NuxtLink
            v-if="isPast"
            :to="`/events/${event.slug}`"
            class="inline-flex items-center gap-1.5 text-xs font-medium text-[var(--color-text-secondary)] transition-colors duration-150 hover:text-[var(--color-text-primary)] focus-visible:underline focus-visible:outline-none"
          >
            View recap
            <svg
              class="size-3.5"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.5"
              aria-hidden="true"
            >
              <path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M12 5l7 7-7 7" />
            </svg>
          </NuxtLink>

          <a
            v-else-if="event.rsvpLink"
            :href="event.rsvpLink"
            target="_blank"
            rel="noopener noreferrer"
            :class="[
              'inline-flex items-center gap-1.5 rounded-lg px-4 py-1.5 text-xs font-semibold',
              'bg-[var(--color-ieee-blue)] text-white',
              'hover:bg-[var(--color-ieee-blue-light)] active:bg-[var(--color-ieee-blue-dark)]',
              'transition-all duration-150',
              'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-ieee-blue)] focus-visible:ring-offset-2',
            ]"
            @click.stop
          >
            RSVP
            <svg
              class="size-3.5"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              aria-hidden="true"
            >
              <path stroke-linecap="round" stroke-linejoin="round" d="M7 17L17 7M17 7H7M17 7v10" />
            </svg>
          </a>

          <NuxtLink
            v-else
            :to="`/events/${event.slug}`"
            class="inline-flex items-center gap-1.5 text-xs font-medium text-[var(--color-ieee-blue)] transition-colors duration-150 hover:text-[var(--color-ieee-blue-light)] focus-visible:underline focus-visible:outline-none"
          >
            Details
            <svg
              class="size-3.5"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.5"
              aria-hidden="true"
            >
              <path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M12 5l7 7-7 7" />
            </svg>
          </NuxtLink>
        </div>
      </div>
    </div>
  </article>
</template>
