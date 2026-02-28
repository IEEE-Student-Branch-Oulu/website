<script setup lang="ts">
/**
 * app.vue
 *
 * Root application component.
 * - Injects the anti-flash script for dark mode (runs before paint)
 * - Adds transition CSS globally
 * - NuxtRouteAnnouncer for screen reader accessibility
 */

useHead({
  // Anti-flash: apply dark class BEFORE first paint to prevent white flash
  // This runs as an inline script in <head> — must be serializable
  script: [
    {
      innerHTML: `
        (function() {
          try {
            var stored = localStorage.getItem('ieee-oulu-color-mode');
            var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            var isDark = stored === 'dark' || ((!stored || stored === 'system') && prefersDark);
            if (isDark) document.documentElement.classList.add('dark');
          } catch(e) {}
        })();
      `,
      type: 'text/javascript',
    },
  ],
  link: [{ rel: 'stylesheet', href: '/assets/css/transitions.css' }],
})
</script>

<template>
  <div>
    <!-- Screen reader route announcer (accessibility) -->
    <NuxtRouteAnnouncer />

    <!-- Skip to main content link (keyboard accessibility) -->
    <a
      href="#main-content"
      class="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-[100] focus:rounded-lg focus:bg-[var(--color-ieee-blue)] focus:px-4 focus:py-2 focus:text-sm focus:font-medium focus:text-white"
    >
      Skip to main content
    </a>

    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>
