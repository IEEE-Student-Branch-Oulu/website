<script setup lang="ts">
/**
 * SectionHeader
 *
 * Consistent section heading used across all pages.
 * Eyebrow → Title → Optional subtitle.
 *
 * Props:
 *   eyebrow  - small monospace label above the title (e.g. "Latest from the blog")
 *   title    - main section heading
 *   subtitle - optional descriptive text below the title
 *   align    - 'left' (default) | 'center'
 *
 * Usage:
 *   <SectionHeader
 *     eyebrow="Latest from the blog"
 *     title="Infodumps & News"
 *     subtitle="Deep dives, event recaps, and tutorials from the board."
 *   />
 */

interface Props {
  eyebrow?: string
  title: string
  subtitle?: string
  align?: 'left' | 'center'
}

withDefaults(defineProps<Props>(), { align: 'left' })
</script>

<template>
  <div :class="align === 'center' ? 'text-center' : ''">
    <!-- Eyebrow -->
    <p
      v-if="eyebrow"
      class="mb-3 font-mono text-[11px] uppercase tracking-[0.15em] text-[var(--color-ieee-blue)]"
    >
      {{ eyebrow }}
    </p>

    <!-- Title -->
    <h2 class="text-2xl font-bold tracking-tight text-[var(--color-text-primary)] sm:text-3xl">
      {{ title }}
    </h2>

    <!-- Subtitle -->
    <p
      v-if="subtitle"
      class="mt-3 max-w-2xl text-base leading-relaxed text-[var(--color-text-secondary)]"
      :class="align === 'center' ? 'mx-auto' : ''"
    >
      {{ subtitle }}
    </p>
  </div>
</template>
