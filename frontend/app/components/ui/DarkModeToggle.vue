<script setup lang="ts">
/**
 * DarkModeToggle
 *
 * Animated sun/moon toggle button.
 * Reads and updates state from useColorMode composable.
 *
 * Usage:
 *   <DarkModeToggle />
 */

const { isDark, toggle } = useColorMode()
</script>

<template>
  <button
    type="button"
    :aria-label="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
    :title="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
    class="relative flex size-9 items-center justify-center rounded-lg text-[var(--color-text-secondary)] transition-all duration-150 hover:bg-[var(--color-surface-overlay)] hover:text-[var(--color-text-primary)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-ieee-blue)] focus-visible:ring-offset-1"
    @click="toggle"
  >
    <Transition
      enter-active-class="transition-all duration-200 ease-out"
      enter-from-class="opacity-0 rotate-90 scale-50"
      enter-to-class="opacity-100 rotate-0 scale-100"
      leave-active-class="transition-all duration-200 ease-in"
      leave-from-class="opacity-100 rotate-0 scale-100"
      leave-to-class="opacity-0 -rotate-90 scale-50"
      mode="out-in"
    >
      <!-- Moon icon (shown in light mode) -->
      <svg
        v-if="!isDark"
        key="moon"
        xmlns="http://www.w3.org/2000/svg"
        class="size-5"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        stroke-width="2"
        aria-hidden="true"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"
        />
      </svg>

      <!-- Sun icon (shown in dark mode) -->
      <svg
        v-else
        key="sun"
        xmlns="http://www.w3.org/2000/svg"
        class="size-5"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        stroke-width="2"
        aria-hidden="true"
      >
        <circle cx="12" cy="12" r="5" />
        <path
          stroke-linecap="round"
          d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42
             M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"
        />
      </svg>
    </Transition>
  </button>
</template>
