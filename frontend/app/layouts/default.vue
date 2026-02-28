<script setup lang="ts">
/**
 * default.vue
 *
 * The main site layout. Wraps every page unless a page
 * explicitly declares a different layout.
 *
 * Structure:
 *   <AppNavbar />   ← fixed, overlaps page content
 *   <main>          ← padded top to clear the navbar
 *     <slot />      ← page content renders here
 *   </main>
 *   <AppFooter />
 *
 * Usage in a page:
 *   definePageMeta({ layout: 'default' })  // optional, this is the default
 */

// Initialize color mode from storage on client mount
const { init } = useColorMode()
onMounted(() => init())
</script>

<template>
  <div class="flex min-h-screen flex-col">
    <LayoutsAppNavbar />

    <main id="main-content" class="flex-1" style="padding-top: var(--nav-height)" tabindex="-1">
      <slot />
    </main>

    <LayoutsAppFooter />
  </div>
</template>
