<script setup lang="ts">
/**
 * BaseBadge
 *
 * Pill-shaped tag for categories, statuses, and labels.
 * Uses IBM Plex Mono for that technical label aesthetic.
 *
 * Props:
 *   variant - color scheme
 *   size    - 'sm' | 'md'
 *   dot     - show a pulsing status dot (useful for "live" / "upcoming")
 *
 * Usage:
 *   <BaseBadge variant="blue">Workshop</BaseBadge>
 *   <BaseBadge variant="green" dot>Upcoming</BaseBadge>
 */

interface Props {
  variant?: 'default' | 'blue' | 'green' | 'orange' | 'red' | 'purple'
  size?: 'sm' | 'md'
  dot?: boolean
}

withDefaults(defineProps<Props>(), {
  variant: 'default',
  size: 'sm',
  dot: false,
})
</script>

<template>
  <span
    :class="[
      'inline-flex items-center gap-1.5 whitespace-nowrap rounded-md font-mono font-medium uppercase tracking-widest',
      size === 'sm' ? 'px-2 py-0.5 text-[10px]' : 'px-2.5 py-1 text-xs',
      variant === 'default' &&
        'bg-[var(--color-surface-overlay)] text-[var(--color-text-secondary)]',
      variant === 'blue' &&
        'bg-[var(--color-ieee-blue)]/10 dark:bg-[var(--color-ieee-blue)]/20 text-[var(--color-ieee-blue)]',
      variant === 'green' && 'bg-emerald-500/10 text-emerald-700 dark:text-emerald-400',
      variant === 'orange' && 'bg-orange-500/10 text-orange-700 dark:text-orange-400',
      variant === 'red' && 'bg-red-500/10 text-red-700 dark:text-red-400',
      variant === 'purple' && 'bg-purple-500/10 text-purple-700 dark:text-purple-400',
    ]"
  >
    <!-- Status dot -->
    <span v-if="dot" class="relative flex size-1.5" aria-hidden="true">
      <span
        class="absolute inline-flex size-full animate-ping rounded-full opacity-75"
        :class="[
          variant === 'green' ? 'bg-emerald-500' : '',
          variant === 'blue' ? 'bg-[var(--color-ieee-blue)]' : '',
          variant === 'orange' ? 'bg-orange-500' : '',
          !['green', 'blue', 'orange'].includes(variant) ? 'bg-current' : '',
        ]"
      />
      <span
        class="relative inline-flex size-1.5 rounded-full"
        :class="[
          variant === 'green' ? 'bg-emerald-500' : '',
          variant === 'blue' ? 'bg-[var(--color-ieee-blue)]' : '',
          variant === 'orange' ? 'bg-orange-500' : '',
          !['green', 'blue', 'orange'].includes(variant) ? 'bg-current' : '',
        ]"
      />
    </span>

    <slot />
  </span>
</template>
