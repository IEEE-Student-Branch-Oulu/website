<script setup lang="ts">
/**
 * BlogFeaturedPost
 *
 * Hero card for the featured post at the top of the blog index.
 * Full-width, cinematic, typographically dominant.
 *
 * Design:
 *   - Wide card, left border in category color
 *   - Large typographic title with generous line height
 *   - Author block + tags row
 *   - "Read article" CTA that slides right on hover
 *
 * Uses:
 *   - UiBaseCard for the card shell (consistent border, radius, transitions)
 *   - UiBaseBadge for the "Featured" flag and post tags
 *   - BlogCategoryBadge for the category pill
 *
 * Props:
 *   post - BlogPostMeta (the featured post)
 *
 * Usage:
 *   <BlogFeaturedPost :post="featuredPost" />
 */
import { CATEGORY_META, type BlogPostMeta } from '~/composables/useBlog'

interface Props {
  post: BlogPostMeta
}

const props = defineProps<Props>()
const meta = computed(() => CATEGORY_META[props.post.category])

const { el, isVisible } = useReveal(0.1)
</script>

<template>
  <div
    ref="el"
    class="duration-600 transition-all"
    :style="{
      opacity: isVisible ? 1 : 0,
      transform: isVisible ? 'translateY(0)' : 'translateY(20px)',
    }"
  >
    <NuxtLink
      :to="`/blog/${post.slug}`"
      class="group block"
      :aria-label="`Featured: ${post.title}`"
    >
      <UiBaseCard padding="none" hoverable class="overflow-hidden hover:shadow-2xl">
        <div class="flex flex-col lg:flex-row">
          <!-- Left: color accent panel -->
          <div
            class="relative h-2 flex-shrink-0 transition-all duration-300 lg:h-auto lg:w-2 group-hover:lg:w-3"
            :style="{ backgroundColor: meta.color }"
            aria-hidden="true"
          />

          <!-- Content -->
          <div class="flex-1 p-7 sm:p-9 lg:p-10">
            <!-- Top row -->
            <div class="mb-5 flex flex-wrap items-center gap-3">
              <!-- Featured flag — uses UiBaseBadge -->
              <UiBaseBadge variant="default" dot> Featured </UiBaseBadge>
              <BlogCategoryBadge :category="post.category" size="sm" />
            </div>

            <!-- Title — large editorial treatment -->
            <h2
              class="mb-5 font-bold leading-[1.08] tracking-tight text-[var(--color-text-primary)] transition-colors duration-150"
              :class="'text-2xl sm:text-3xl lg:text-4xl'"
            >
              {{ post.title }}
            </h2>

            <!-- Excerpt -->
            <p
              class="mb-7 line-clamp-2 max-w-2xl text-base leading-relaxed text-[var(--color-text-secondary)]"
            >
              {{ post.excerpt }}
            </p>

            <!-- Tags — uses UiBaseBadge for consistent tag styling -->
            <div class="mb-8 flex flex-wrap gap-1.5">
              <UiBaseBadge
                v-for="tag in post.tags.slice(0, 5)"
                :key="tag"
                variant="default"
                size="sm"
                class="hover:border-[var(--color-ieee-blue)]/40 border border-[var(--color-border)] !bg-transparent transition-colors duration-150"
              >
                #{{ tag.toLowerCase().replace(/\s/g, '-') }}
              </UiBaseBadge>
            </div>

            <!-- Footer row -->
            <div class="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
              <!-- Author -->
              <div class="flex items-center gap-3">
                <div
                  class="flex size-9 flex-shrink-0 items-center justify-center rounded-full border"
                  :style="{
                    backgroundColor: `color-mix(in srgb, ${meta.color} 12%, transparent)`,
                    borderColor: `color-mix(in srgb, ${meta.color} 25%, transparent)`,
                  }"
                  aria-hidden="true"
                >
                  <span class="font-mono text-xs font-bold" :style="{ color: meta.color }">
                    {{ post.authorInitials }}
                  </span>
                </div>
                <div>
                  <p class="text-sm font-semibold text-[var(--color-text-primary)]">
                    {{ post.author }}
                  </p>
                  <p class="font-mono text-xs text-[var(--color-text-muted)]">
                    {{ post.authorRole }} · {{ post.date }} · {{ post.readTime }}
                  </p>
                </div>
              </div>

              <!-- CTA -->
              <span
                class="inline-flex items-center gap-2 text-sm font-semibold transition-all duration-200"
                :style="{ color: meta.color }"
              >
                Read article
                <svg
                  class="size-4 transition-transform duration-200 group-hover:translate-x-1"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  aria-hidden="true"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M12 5l7 7-7 7" />
                </svg>
              </span>
            </div>
          </div>
        </div>
      </UiBaseCard>
    </NuxtLink>
  </div>
</template>
