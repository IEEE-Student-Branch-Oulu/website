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
 *   level    - 1 | 2 — controls the heading tag and text size
 *              level 1 renders <h1> with larger text (for page headings)
 *              level 2 renders <h2> with standard text (for sections)
 *
 * Usage:
 *   <SectionHeader
 *     eyebrow="IEEE Oulu · Events"
 *     title="Events & Meetups"
 *     subtitle="Workshops, tech talks, hackathons, and socials."
 *     :level="1"
 *   />
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
  level?: 1 | 2
}

withDefaults(defineProps<Props>(), { align: 'left', level: 2 })
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
    <component
      :is="level === 1 ? 'h1' : 'h2'"
      :class="[
        'font-bold tracking-tight text-[var(--color-text-primary)]',
        level === 1 ? 'text-4xl sm:text-5xl' : 'text-2xl sm:text-3xl',
      ]"
    >
      {{ title }}
    </component>

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
