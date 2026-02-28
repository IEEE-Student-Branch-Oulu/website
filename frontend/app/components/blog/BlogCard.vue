<script setup lang="ts">
/**
 * BlogCard
 *
 * Card for displaying a blog post preview.
 * Used on the home page (LatestNewsRow) and the blog index page.
 * Accepts a BlogPost object as a single prop for easy API integration later.
 *
 * Props:
 *   post  - BlogPost data object
 *   index - position in a list (used for stagger animation delay)
 *
 * Usage:
 *   <BlogCard :post="post" :index="0" />
 */

export interface BlogPost {
  id: number
  title: string
  slug: string
  excerpt: string
  author: string
  authorInitials: string
  date: string // Display string: "Feb 12, 2026"
  category: string
  categoryVariant: 'blue' | 'green' | 'orange' | 'red' | 'purple' | 'default'
  readTime: string // "5 min read"
}

interface Props {
  post: BlogPost
  index?: number
}

const props = withDefaults(defineProps<Props>(), { index: 0 })

const { el, isVisible } = useReveal()

const delayMs = computed(() => props.index * 100)
</script>

<template>
  <article
    ref="el"
    class="group flex h-full flex-col transition-all duration-500"
    :style="{
      opacity: isVisible ? 1 : 0,
      transform: isVisible ? 'translateY(0)' : 'translateY(20px)',
      transitionDelay: `${delayMs}ms`,
    }"
  >
    <!-- <NuxtLink
      :to="`/blog/${post.slug}`"
      class="hover:border-[var(--color-ieee-blue)]/30 dark:hover:border-[var(--color-ieee-blue)]/40 flex h-full flex-col overflow-hidden rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] transition-all duration-200 hover:-translate-y-1 hover:shadow-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-ieee-blue)]"
      :aria-label="`Read: ${post.title}`"
    > -->
    <NuxtLink
      :to="`/#`"
      class="hover:border-[var(--color-ieee-blue)]/30 dark:hover:border-[var(--color-ieee-blue)]/40 flex h-full flex-col overflow-hidden rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] transition-all duration-200 hover:-translate-y-1 hover:shadow-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-ieee-blue)]"
      :aria-label="`Read: ${post.title}`"
    >
      <!-- Top accent bar (appears on hover) -->
      <div
        class="h-0.5 w-0 bg-gradient-to-r from-[var(--color-ieee-blue)] to-[var(--color-ieee-accent)] transition-all duration-300 ease-out group-hover:w-full"
        aria-hidden="true"
      />

      <div class="flex flex-1 flex-col p-6">
        <!-- Category badge -->
        <div class="mb-4">
          <UiBaseBadge :variant="post.categoryVariant">{{ post.category }}</UiBaseBadge>
        </div>

        <!-- Title -->
        <h3
          class="mb-3 text-base font-semibold leading-snug text-[var(--color-text-primary)] transition-colors duration-150 group-hover:text-[var(--color-ieee-blue)]"
        >
          {{ post.title }}
        </h3>

        <!-- Excerpt -->
        <p class="line-clamp-2 flex-1 text-sm leading-relaxed text-[var(--color-text-secondary)]">
          {{ post.excerpt }}
        </p>

        <!-- Footer: author + meta -->
        <div class="mt-5 flex items-center gap-3 border-t border-[var(--color-border-subtle)] pt-4">
          <!-- Author avatar -->
          <div
            class="bg-[var(--color-ieee-blue)]/10 border-[var(--color-ieee-blue)]/20 flex size-7 flex-shrink-0 items-center justify-center rounded-full border"
            aria-hidden="true"
          >
            <span class="font-mono text-[9px] font-bold text-[var(--color-ieee-blue)]">
              {{ post.authorInitials }}
            </span>
          </div>

          <div class="min-w-0 flex-1">
            <p class="truncate text-xs font-medium text-[var(--color-text-primary)]">
              {{ post.author }}
            </p>
            <p class="font-mono text-[11px] text-[var(--color-text-muted)]">{{ post.date }}</p>
          </div>

          <span class="flex-shrink-0 font-mono text-[11px] text-[var(--color-text-muted)]">
            {{ post.readTime }}
          </span>
        </div>
      </div>
    </NuxtLink>
  </article>
</template>
