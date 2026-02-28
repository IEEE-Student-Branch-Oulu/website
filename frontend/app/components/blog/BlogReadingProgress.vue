<script setup lang="ts">
/**
 * BlogReadingProgress
 *
 * Thin reading progress bar fixed at the top of the page (under the navbar).
 * Uses useReadingProgress from useBlog composable.
 *
 * No props — self-contained, just drop it into a layout.
 *
 * Usage:
 *   <BlogReadingProgress />   (place at top of post page template)
 */
import { useReadingProgress } from '~/composables/useBlog'

const { progress } = useReadingProgress()
</script>

<template>
  <div
    class="fixed left-0 right-0 z-40 h-0.5 bg-transparent"
    style="top: var(--nav-height)"
    aria-hidden="true"
    role="presentation"
  >
    <div
      class="h-full bg-gradient-to-r from-[var(--color-ieee-blue)] to-[var(--color-ieee-accent)] transition-[width] duration-75 ease-linear"
      :style="{ width: `${progress}%` }"
    />
  </div>
</template>
