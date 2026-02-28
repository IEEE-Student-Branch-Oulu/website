<script setup lang="ts">
/**
 * BaseLink
 *
 * Wraps NuxtLink with consistent active state styling.
 * Used in Navbar and Footer for navigation items.
 *
 * Props:
 *   to       - internal route (uses NuxtLink)
 *   href     - external URL (renders as <a>)
 *   exact    - use exact active matching
 *
 * Usage:
 *   <BaseLink to="/events">Events</BaseLink>
 *   <BaseLink href="https://discord.gg/..." external>Discord</BaseLink>
 */

interface Props {
  to?: string
  href?: string
  exact?: boolean
  external?: boolean
  class?: string
}

withDefaults(defineProps<Props>(), {
  exact: false,
  external: false,
})
</script>

<template>
  <!-- External link -->
  <a v-if="href" :href="href" target="_blank" rel="noopener noreferrer" :class="$props.class">
    <slot />
  </a>

  <!-- Internal NuxtLink -->
  <NuxtLink
    v-else-if="to"
    :to="to"
    :exact-active-class="'nav-link--active'"
    :active-class="!exact ? 'nav-link--active' : undefined"
    :class="$props.class"
  >
    <slot />
  </NuxtLink>
</template>
