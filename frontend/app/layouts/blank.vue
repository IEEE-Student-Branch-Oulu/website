<script setup lang="ts">
/**
 * blank.vue
 *
 * Minimal layout with no navbar or footer.
 * Used for: /admin, /login, error pages, full-screen experiences.
 *
 * Usage in a page:
 *   definePageMeta({ layout: 'blank' })
 */

const { init } = useColorMode()
onMounted(() => init())
</script>

<template>
  <div class="flex min-h-screen flex-col">
    <slot />
  </div>
</template>
