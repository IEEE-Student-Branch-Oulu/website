<script setup lang="ts">
/**
 * BlogPostHeader
 *
 * Full post header block rendered above the article body.
 * Contains: category, title, author block, date/time meta, tags.
 *
 * Uses:
 *   - UiBaseLink for the "All posts" back link (consistent navigation link)
 *   - UiBaseBadge for post tags (consistent badge styling)
 *   - BlogCategoryBadge for the category pill
 *
 * Props:
 *   post - BlogPostMeta (or BlogPostFull — both work, uses only meta fields)
 *
 * Usage:
 *   <BlogPostHeader :post="post" />
 */
import { CATEGORY_META, type BlogPostMeta } from '~/composables/useBlog'

interface Props {
  post: BlogPostMeta
}

const props = defineProps<Props>()
const meta = computed(() => CATEGORY_META[props.post.category])
</script>

<template>
  <header class="mb-10">
    <!-- Category badge + back link -->
    <div class="mb-5 flex flex-wrap items-center gap-3">
      <!-- Back link — uses UiBaseLink for consistent navigation -->
      <UiBaseLink
        to="/blog"
        class="inline-flex items-center gap-1.5 font-mono text-[11px] uppercase tracking-wider text-[var(--color-text-muted)] transition-colors duration-150 hover:text-[var(--color-text-primary)] focus-visible:underline focus-visible:outline-none"
      >
        <svg
          class="size-3"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2.5"
          aria-hidden="true"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M19 12H5M12 5l-7 7 7 7" />
        </svg>
        All posts
      </UiBaseLink>

      <span class="text-[var(--color-border)]" aria-hidden="true">/</span>
      <BlogCategoryBadge :category="post.category" size="sm" />
    </div>

    <!-- Title -->
    <h1
      class="mb-6 text-3xl font-bold leading-[1.1] tracking-tight text-[var(--color-text-primary)] sm:text-4xl"
    >
      {{ post.title }}
    </h1>

    <!-- Excerpt -->
    <p class="mb-8 max-w-3xl text-lg leading-relaxed text-[var(--color-text-secondary)]">
      {{ post.excerpt }}
    </p>

    <!-- Meta row -->
    <div
      class="flex flex-wrap items-center gap-x-6 gap-y-4 border-b-2 pb-8"
      :style="{ borderColor: meta.color }"
    >
      <!-- Author -->
      <div class="flex items-center gap-3">
        <div
          class="flex size-10 flex-shrink-0 items-center justify-center rounded-full border-2"
          :style="{
            backgroundColor: `color-mix(in srgb, ${meta.color} 12%, transparent)`,
            borderColor: `color-mix(in srgb, ${meta.color} 30%, transparent)`,
          }"
          aria-hidden="true"
        >
          <span class="font-mono text-xs font-bold" :style="{ color: meta.color }">
            {{ post.authorInitials }}
          </span>
        </div>
        <div>
          <p class="text-sm font-semibold text-[var(--color-text-primary)]">{{ post.author }}</p>
          <p class="font-mono text-xs text-[var(--color-text-muted)]">{{ post.authorRole }}</p>
        </div>
      </div>

      <!-- Divider -->
      <div class="hidden h-8 w-px bg-[var(--color-border)] sm:block" aria-hidden="true" />

      <!-- Date & read time -->
      <div
        class="flex flex-wrap items-center gap-4 font-mono text-xs text-[var(--color-text-muted)]"
      >
        <time :datetime="post.dateISO">{{ post.date }}</time>
        <span>·</span>
        <span>{{ post.readTime }}</span>
      </div>
    </div>

    <!-- Tags — uses UiBaseBadge for consistent tag styling -->
    <div class="mt-6 flex flex-wrap gap-2" aria-label="Tags">
      <UiBaseBadge
        v-for="tag in post.tags"
        :key="tag"
        variant="default"
        size="sm"
        class="hover:border-[var(--color-ieee-blue)]/40 border border-[var(--color-border)] !bg-transparent !text-[var(--color-text-muted)] transition-colors duration-150"
      >
        #{{ tag.toLowerCase().replace(/\s/g, '-') }}
      </UiBaseBadge>
    </div>
  </header>
</template>
