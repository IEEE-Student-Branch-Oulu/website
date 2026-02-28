<script setup lang="ts">
/**
 * BaseCard
 *
 * Flexible card container. Composes well with BaseBadge, BaseButton, etc.
 *
 * Props:
 *   hoverable - lifts on hover, changes border to ieee-blue tint
 *   flat      - no border, surface-raised background
 *   padding   - 'none' | 'sm' | 'md' | 'lg'
 *   as        - root element tag (div, article, li, etc.)
 *
 * Usage:
 *   <BaseCard hoverable as="article">...</BaseCard>
 *   <BaseCard flat padding="lg">...</BaseCard>
 */

interface Props {
  hoverable?: boolean
  flat?: boolean
  padding?: 'none' | 'sm' | 'md' | 'lg'
  as?: string
}

withDefaults(defineProps<Props>(), {
  hoverable: false,
  flat: false,
  padding: 'md',
  as: 'div',
})
</script>

<template>
  <component
    :is="as"
    :class="[
      'rounded-xl border transition-all duration-200',
      flat
        ? 'border-transparent bg-[var(--color-surface-raised)]'
        : 'border-[var(--color-border)] bg-[var(--color-surface)]',
      hoverable && [
        'cursor-pointer',
        'hover:-translate-y-1 hover:shadow-lg',
        'hover:border-[var(--color-ieee-blue)]/30',
        'dark:hover:border-[var(--color-ieee-blue)]/40',
      ],
      padding === 'none' && '',
      padding === 'sm' && 'p-4',
      padding === 'md' && 'p-6',
      padding === 'lg' && 'p-8',
    ]"
  >
    <slot />
  </component>
</template>
