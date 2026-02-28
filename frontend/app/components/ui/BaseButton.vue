<script setup lang="ts">
/**
 * BaseButton
 *
 * Reusable button with variant, size, and loading state support.
 *
 * Props:
 *   variant  - 'primary' | 'secondary' | 'ghost' | 'danger'
 *   size     - 'sm' | 'md' | 'lg'
 *   loading  - shows spinner, disables interaction
 *   disabled - standard disabled state
 *   href     - renders as <a> tag if provided
 *   external - adds target="_blank" rel="noopener noreferrer"
 *
 * Usage:
 *   <BaseButton variant="primary" size="md" @click="handleClick">
 *     Join Us
 *   </BaseButton>
 *   <BaseButton href="/events" variant="secondary">View Events</BaseButton>
 */

interface Props {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
  disabled?: boolean
  href?: string
  external?: boolean
  type?: 'button' | 'submit' | 'reset'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  loading: false,
  disabled: false,
  type: 'button',
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

const tag = computed(() => (props.href ? 'a' : 'button'))

const linkProps = computed(() => {
  if (!props.href) return {}
  return props.external
    ? { href: props.href, target: '_blank', rel: 'noopener noreferrer' }
    : { href: props.href }
})

const isDisabled = computed(() => props.disabled || props.loading)

const classes = computed(() => [
  // Base
  'inline-flex items-center justify-center gap-2 font-medium rounded-lg',
  'transition-all duration-150 cursor-pointer select-none',
  'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',

  // Size
  {
    'text-xs px-3 py-1.5 h-7': props.size === 'sm',
    'text-sm px-4 py-2 h-9': props.size === 'md',
    'text-base px-6 py-3 h-11': props.size === 'lg',
  },

  // Variant
  {
    // Primary — IEEE Blue fill
    'bg-[var(--color-ieee-blue)] text-white hover:bg-[var(--color-ieee-blue-light)] active:bg-[var(--color-ieee-blue-dark)] focus-visible:ring-[var(--color-ieee-blue)]':
      props.variant === 'primary',

    // Secondary — outlined
    'border border-[var(--color-ieee-blue)] text-[var(--color-ieee-blue)] hover:bg-[var(--color-ieee-blue)] hover:text-white focus-visible:ring-[var(--color-ieee-blue)]':
      props.variant === 'secondary',

    // Ghost — no border
    'text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] hover:bg-[var(--color-surface-overlay)] focus-visible:ring-[var(--color-border)]':
      props.variant === 'ghost',

    // Danger
    'bg-red-600 text-white hover:bg-red-700 active:bg-red-800 focus-visible:ring-red-500':
      props.variant === 'danger',
  },

  // Disabled / Loading
  {
    'opacity-50 cursor-not-allowed pointer-events-none': isDisabled.value,
  },
])
</script>

<template>
  <component
    :is="tag"
    v-bind="linkProps"
    :type="tag === 'button' ? type : undefined"
    :disabled="tag === 'button' ? isDisabled : undefined"
    :aria-disabled="isDisabled"
    :aria-busy="loading"
    :class="classes"
    @click="!isDisabled && emit('click', $event)"
  >
    <!-- Loading spinner -->
    <svg
      v-if="loading"
      class="animate-spin"
      :class="size === 'sm' ? 'size-3' : 'size-4'"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      aria-hidden="true"
    >
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
      <path
        class="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
      />
    </svg>

    <slot />
  </component>
</template>
