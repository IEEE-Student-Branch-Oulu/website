<script setup lang="ts">
/**
 * BlogCard
 *
 * Card for displaying a blog post preview.
 * Used on the home page (LatestNewsRow) and the blog index.
 *
 * Design:
 *   - Left accent stripe colored by category (not type — unique to blog)
 *   - Category badge, title, excerpt, author + meta footer
 *   - Hover: title turns category-color, card lifts, accent stripe grows
 *
 * Uses:
 *   - UiBaseCard for the card shell (consistent border, radius, hover transitions)
 *   - BlogCategoryBadge for the category pill (wraps UiBaseBadge)
 *
 * Props:
 *   post     - BlogPostMeta
 *   index    - stagger delay position
 *   compact  - smaller variant (used in related posts row)
 *
 * Usage:
 *   <BlogCard :post="post" :index="0" />
 */
import { CATEGORY_META, type BlogPostMeta } from '~/composables/useBlog'

interface Props {
  post: BlogPostMeta
  index?: number
  compact?: boolean
}

const props = withDefaults(defineProps<Props>(), { index: 0, compact: false })

const { el, isVisible } = useReveal()
const meta = computed(() => CATEGORY_META[props.post.category])
const delayMs = computed(() => Math.min(props.index * 90, 360))
</script>

<template>
  <article
    ref="el"
    class="group h-full transition-all duration-500"
    :style="{
      opacity: isVisible ? 1 : 0,
      transform: isVisible ? 'translateY(0)' : 'translateY(18px)',
      transitionDelay: `${delayMs}ms`,
    }"
  >
    <NuxtLink :to="`/blog/${post.slug}`" class="block h-full" :aria-label="`Read: ${post.title}`">
      <!-- Card shell — uses UiBaseCard for consistent styling -->
      <UiBaseCard
        padding="none"
        hoverable
        class="flex h-full flex-col overflow-hidden hover:shadow-xl"
      >
        <!-- Category-colored top stripe — slides in on hover -->
        <div class="relative h-0.5 overflow-hidden bg-[var(--color-border-subtle)]">
          <div
            class="absolute inset-y-0 left-0 w-0 transition-all duration-500 ease-out group-hover:w-full"
            :style="{ background: `linear-gradient(to right, ${meta.color}, transparent)` }"
            aria-hidden="true"
          />
        </div>

        <div :class="['flex flex-1 flex-col', compact ? 'p-4' : 'p-5']">
          <!-- Category badge -->
          <div class="mb-3">
            <BlogCategoryBadge :category="post.category" />
          </div>

          <!-- Title -->
          <h3
            :class="[
              'mb-3 font-bold leading-snug text-[var(--color-text-primary)] transition-colors duration-150',
              compact ? 'line-clamp-2 text-sm' : 'line-clamp-3 text-base',
            ]"
            :style="{ '--hover-color': meta.color }"
          >
            <span class="transition-colors duration-150 group-hover:text-[var(--hover-color)]">
              {{ post.title }}
            </span>
          </h3>

          <!-- Excerpt (not in compact mode) -->
          <p
            v-if="!compact"
            class="mb-4 line-clamp-2 flex-1 text-sm leading-relaxed text-[var(--color-text-secondary)]"
          >
            {{ post.excerpt }}
          </p>

          <div v-else class="flex-1" />

          <!-- Footer -->
          <div
            class="mt-auto flex items-center gap-2.5 border-t border-[var(--color-border-subtle)] pt-3.5"
          >
            <!-- Avatar -->
            <div
              class="flex size-6 flex-shrink-0 items-center justify-center rounded-full border"
              :style="{
                backgroundColor: `color-mix(in srgb, ${meta.color} 12%, transparent)`,
                borderColor: `color-mix(in srgb, ${meta.color} 25%, transparent)`,
              }"
              aria-hidden="true"
            >
              <span class="font-mono text-[8px] font-bold" :style="{ color: meta.color }">{{
                post.authorInitials
              }}</span>
            </div>

            <div class="min-w-0 flex-1">
              <p class="truncate text-xs font-medium text-[var(--color-text-primary)]">
                {{ post.author }}
              </p>
            </div>

            <!-- Read time + date -->
            <div class="flex-shrink-0 text-right">
              <p class="font-mono text-[10px] text-[var(--color-text-muted)]">
                {{ post.readTime }}
              </p>
              <p class="font-mono text-[10px] text-[var(--color-text-muted)]">{{ post.date }}</p>
            </div>
          </div>
        </div>
      </UiBaseCard>
    </NuxtLink>
  </article>
</template>
