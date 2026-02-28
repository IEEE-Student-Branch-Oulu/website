<script setup lang="ts">
/**
 * LatestNewsRow
 *
 * Displays the 3 most recent blog posts as a card grid.
 * Shows branch activity and drives traffic to the blog.
 *
 * For V1, uses hardcoded dummy data.
 * TODO: Replace with `useFetch('/api/v1/posts?limit=3')` when API is ready.
 */

import type { BlogPost } from '~/components/blog/BlogCard.vue'

// ── Dummy data — replace with API call ───────────────────────
const posts: BlogPost[] = [
  {
    id: 1,
    title: 'How We Built a Radar System with GNU Radio and a $20 SDR Dongle',
    slug: 'gnu-radio-sdr-radar-workshop',
    excerpt:
      'At our February workshop, 18 students built a working radar that could detect passing objects using nothing but an RTL-SDR dongle, GNU Radio, and a lot of caffeine.',
    author: 'Juhani Virtanen',
    authorInitials: 'JV',
    date: 'Feb 12, 2026',
    category: 'Workshop Recap',
    categoryVariant: 'blue',
    readTime: '6 min read',
  },
  {
    id: 2,
    title: 'Linux Ricing for Engineers: A Practical Guide to a Actually Usable Terminal',
    slug: 'linux-ricing-guide-engineers',
    excerpt:
      "Your dev environment should be as well-engineered as your code. Here's how to set up a fast, beautiful terminal workflow with Neovim, tmux, and a tiling WM — without losing a week to dotfiles.",
    author: 'Mikael Korhonen',
    authorInitials: 'MK',
    date: 'Feb 3, 2026',
    category: 'Tutorial',
    categoryVariant: 'green',
    readTime: '11 min read',
  },
  {
    id: 3,
    title: 'IEEE Oulu Wins Best Student Branch Activity Award at Finland Section Annual Meeting',
    slug: 'ieee-oulu-best-activity-award-2025',
    excerpt:
      'At the IEEE Finland Section Annual Meeting in Helsinki, the Oulu Student Branch was recognised for outstanding technical activity and membership growth in 2025.',
    author: 'IEEE Oulu Board',
    authorInitials: 'IB',
    date: 'Feb 1, 2026',
    category: 'Branch News',
    categoryVariant: 'orange',
    readTime: '3 min read',
  },
]

const { el, isVisible } = useReveal()
</script>

<template>
  <section
    class="bg-[var(--color-surface-raised)] py-20 sm:py-28"
    aria-labelledby="blog-section-heading"
  >
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <!-- Header row -->
      <div
        ref="el"
        class="mb-12 flex flex-col gap-6 transition-all duration-500 sm:flex-row sm:items-end sm:justify-between"
        :style="{
          opacity: isVisible ? 1 : 0,
          transform: isVisible ? 'translateY(0)' : 'translateY(16px)',
        }"
      >
        <UiSectionHeader
          eyebrow="Latest from the blog"
          title="Infodumps & News"
          subtitle="Event recaps, tech tutorials, and branch updates written by the board."
        />

        <NuxtLink
          to="/#"
          class="inline-flex flex-shrink-0 items-center gap-2 whitespace-nowrap text-sm font-medium text-[var(--color-ieee-blue)] transition-colors duration-150 hover:text-[var(--color-ieee-blue-light)] focus-visible:underline focus-visible:outline-none"
        >
          View all posts
          <svg
            class="size-4"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            aria-hidden="true"
          >
            <path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        </NuxtLink>
      </div>

      <!-- Cards grid -->
      <div
        class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3"
        role="list"
        aria-label="Recent blog posts"
      >
        <div v-for="(post, index) in posts" :key="post.id" role="listitem">
          <BlogCard :post="post" :index="index" />
        </div>
      </div>
    </div>
  </section>
</template>
