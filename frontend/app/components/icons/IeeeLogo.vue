<script setup lang="ts">
import { computed } from 'vue'
import { useColorMode } from '~/composables/useColorMode'

/**
 * IeeeLogo
 *
 * IEEE Oulu Student Branch logo using cropped .webp images.
 * Swaps between light and dark variants based on the current color mode.
 * Both images have identical content bounds so there is no position jump.
 *
 * Props:
 * size - 'sm' | 'md' | 'lg'
 *
 * Usage:
 * <IeeeLogo size="md" />
 */

interface Props {
  size?: 'sm' | 'md' | 'lg'
}

withDefaults(defineProps<Props>(), { size: 'md' })

const sizeClasses: Record<string, string> = {
  sm: 'h-8',
  md: 'h-10',
  lg: 'h-10 md:h-12',
}

const { isDark } = useColorMode()

const logoSrc = computed(() => {
  return isDark.value ? '/ieeesboulu-dark-logo.webp' : '/ieeesboulu-light-logo.webp'
})
</script>

<template>
  <NuxtLink
    to="/"
    class="group flex items-center focus-visible:outline-none"
    aria-label="IEEE Oulu — Home"
  >
    <img
      :src="logoSrc"
      alt="IEEE Oulu Student Branch"
      :class="[sizeClasses[size], 'w-auto object-contain transition-opacity duration-300']"
    />
  </NuxtLink>
</template>
