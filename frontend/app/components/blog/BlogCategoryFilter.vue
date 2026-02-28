<script setup lang="ts">
/**
 * BlogCategoryFilter
 *
 * Sidebar category filter for the blog index.
 * Shows each category with a post count and a colored left indicator.
 * "All" option always shown at top.
 *
 * Props:
 *   modelValue - currently active category (null = all)
 *   counts     - map of category → post count
 *
 * Emits:
 *   update:modelValue
 *
 * Usage:
 *   <BlogCategoryFilter v-model="activeCategory" :counts="categoryCounts" />
 */
import { CATEGORY_META, type PostCategory } from '~/composables/useBlog'

type CategoryFilter = PostCategory | null

interface Props {
  modelValue: CategoryFilter
  counts: Partial<Record<PostCategory, number>>
  total: number
}

defineProps<Props>()
const emit = defineEmits<{ 'update:modelValue': [value: CategoryFilter] }>()

const CATEGORIES = Object.entries(CATEGORY_META) as [
  PostCategory,
  (typeof CATEGORY_META)[PostCategory],
][]
</script>

<template>
  <nav aria-label="Filter by category">
    <p
      class="mb-3 font-mono text-[10px] uppercase tracking-[0.15em] text-[var(--color-text-muted)]"
    >
      Categories
    </p>

    <ul class="flex flex-col gap-0.5" role="list">
      <!-- All posts -->
      <li>
        <button
          type="button"
          :class="[
            'flex w-full items-center justify-between gap-3 rounded-lg px-3 py-2 text-sm transition-all duration-150',
            'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-ieee-blue)]',
            modelValue === null
              ? 'bg-[var(--color-surface-overlay)] font-medium text-[var(--color-text-primary)]'
              : 'text-[var(--color-text-secondary)] hover:bg-[var(--color-surface-overlay)] hover:text-[var(--color-text-primary)]',
          ]"
          :aria-current="modelValue === null ? 'page' : undefined"
          @click="emit('update:modelValue', null)"
        >
          <span class="flex items-center gap-2.5">
            <span class="size-1.5 rounded-full bg-[var(--color-text-muted)]" aria-hidden="true" />
            All posts
          </span>
          <span class="font-mono text-xs text-[var(--color-text-muted)]">{{ total }}</span>
        </button>
      </li>

      <!-- Category items -->
      <li v-for="[key, meta] in CATEGORIES" :key="key">
        <button
          type="button"
          :class="[
            'flex w-full items-center justify-between gap-3 rounded-lg px-3 py-2 text-sm transition-all duration-150',
            'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-ieee-blue)]',
            modelValue === key
              ? 'bg-[var(--color-surface-overlay)] font-medium'
              : 'text-[var(--color-text-secondary)] hover:bg-[var(--color-surface-overlay)] hover:text-[var(--color-text-primary)]',
          ]"
          :style="modelValue === key ? { color: meta.color } : {}"
          :aria-current="modelValue === key ? 'page' : undefined"
          @click="emit('update:modelValue', modelValue === key ? null : key)"
        >
          <span class="flex items-center gap-2.5 truncate">
            <!-- Color dot -->
            <span
              class="size-1.5 flex-shrink-0 rounded-full"
              :style="{ backgroundColor: meta.color }"
              aria-hidden="true"
            />
            <span class="truncate">{{ meta.label }}</span>
          </span>
          <span class="flex-shrink-0 font-mono text-xs text-[var(--color-text-muted)]">
            {{ counts[key] ?? 0 }}
          </span>
        </button>
      </li>
    </ul>
  </nav>
</template>
