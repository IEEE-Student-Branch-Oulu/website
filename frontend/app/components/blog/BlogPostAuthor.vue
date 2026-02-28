<script setup lang="ts">
/**
 * BlogPostAuthor
 *
 * Author card rendered at the bottom of every post.
 * Shows initials avatar, name, role, and a link to see their other posts.
 *
 * Uses:
 *   - UiBaseCard for the aside container (consistent card styling)
 *   - UiBaseLink for the "More posts" navigation link
 *
 * Props:
 *   post - BlogPostMeta (uses author fields)
 *
 * Usage:
 *   <BlogPostAuthor :post="post" />
 */
import { CATEGORY_META, type BlogPostMeta } from '~/composables/useBlog'

interface Props {
  post: BlogPostMeta
}

const props = defineProps<Props>()
const meta = computed(() => CATEGORY_META[props.post.category])
</script>

<template>
  <UiBaseCard as="aside" flat padding="md" aria-label="About the author">
    <p
      class="mb-5 font-mono text-[10px] uppercase tracking-[0.15em] text-[var(--color-text-muted)]"
    >
      Written by
    </p>

    <div class="flex items-start gap-4">
      <!-- Large avatar -->
      <div
        class="flex size-14 flex-shrink-0 items-center justify-center rounded-2xl border-2"
        :style="{
          backgroundColor: `color-mix(in srgb, ${meta.color} 12%, transparent)`,
          borderColor: `color-mix(in srgb, ${meta.color} 30%, transparent)`,
        }"
        aria-hidden="true"
      >
        <span class="font-mono text-lg font-bold" :style="{ color: meta.color }">
          {{ post.authorInitials }}
        </span>
      </div>

      <!-- Info -->
      <div class="min-w-0 flex-1">
        <p class="mb-0.5 text-base font-bold text-[var(--color-text-primary)]">
          {{ post.author }}
        </p>
        <p class="mb-3 text-sm text-[var(--color-text-secondary)]">
          {{ post.authorRole }}, IEEE Oulu Student Branch
        </p>

        <!-- See their posts link — uses UiBaseLink for consistent navigation -->
        <UiBaseLink
          :to="`/blog?author=${encodeURIComponent(post.author)}`"
          class="inline-flex items-center gap-1.5 text-xs font-medium transition-colors duration-150 focus-visible:underline focus-visible:outline-none"
          :style="{ color: meta.color }"
        >
          More posts by {{ post.author.split(' ')[0] }}
          <svg
            class="size-3.5"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            aria-hidden="true"
          >
            <path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        </UiBaseLink>
      </div>
    </div>
  </UiBaseCard>
</template>
