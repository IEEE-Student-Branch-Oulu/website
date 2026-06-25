<script setup lang="ts">
/**
 * Blog Index ( /blog )
 *
 * Layout:
 *   ┌──────────────────────────────────────────────┐
 *   │  Page header (UiSectionHeader)               │
 *   ├──────────────────────────────────────────────┤
 *   │  Featured post (full width hero card)        │
 *   ├───────────────────────┬──────────────────────┤
 *   │                       │                      │
 *   │  Posts grid           │  Category sidebar    │
 *   │  (2/3 width)          │  (sticky, 1/3)       │
 *   │                       │                      │
 *   └───────────────────────┴──────────────────────┘
 *
 * Uses:
 *   - UiSectionHeader for the page heading (eyebrow + h1 + subtitle)
 *   - UiBaseCard for sidebar boxes (category filter, about section)
 *   - UiBaseCard + UiBaseButton for the empty state
 *   - UiBaseLink for the Discord link in the about sidebar
 */
import { useBlogApi, type PostCategory } from '~/composables/useBlog'

definePageMeta({ layout: 'default' })

useSeoMeta({
  title: 'Infodumps',
  description:
    'Workshop recaps, tutorials, tech notes, and branch news from the IEEE Oulu Student Branch.',
})

// ── Data ──────────────────────────────────────────────────────
const { list } = useBlogApi()
const { data } = await useAsyncData('blog-posts', () => list())
const allPosts = computed(() => data.value?.items ?? [])

// ── Filter state ──────────────────────────────────────────────
const activeCategory = ref<PostCategory | null>(null)

// ── Derived data ──────────────────────────────────────────────
const featuredPost = computed(() => allPosts.value.find((p) => p.featured) ?? allPosts.value[0])

const filteredPosts = computed(() => {
  if (!activeCategory.value) return allPosts.value
  return allPosts.value.filter((p) => p.category === activeCategory.value)
})

// Non-featured posts for the grid (the featured post gets its own hero slot
// only while no category filter is active).
const gridPosts = computed(() =>
  filteredPosts.value.filter(
    (p) => activeCategory.value !== null || p.id !== featuredPost.value?.id
  )
)

const categoryCounts = computed(() => {
  const counts: Partial<Record<PostCategory, number>> = {}
  allPosts.value.forEach((p) => {
    counts[p.category] = (counts[p.category] ?? 0) + 1
  })
  return counts
})

// ── Reveal ────────────────────────────────────────────────────
const { el: headerEl, isVisible: headerVisible } = useReveal(0.05)
</script>

<template>
  <div class="min-h-screen bg-[var(--color-surface)]">
    <!-- ── Page header ──────────────────────────────────────── -->
    <div class="border-b border-[var(--color-border)] bg-[var(--color-surface-raised)]">
      <div class="mx-auto max-w-7xl px-4 py-12 sm:px-6 sm:py-16 lg:px-8">
        <div
          ref="headerEl"
          class="transition-all duration-500"
          :style="{
            opacity: headerVisible ? 1 : 0,
            transform: headerVisible ? 'translateY(0)' : 'translateY(12px)',
          }"
        >
          <div class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
            <!-- Page heading — reusable SectionHeader component -->
            <UiSectionHeader
              eyebrow="IEEE Oulu · Blog"
              title="Infodumps"
              subtitle="Workshop recaps, tutorials, tech notes, and branch news — written by the board."
              :level="1"
            />
            <p class="flex-shrink-0 font-mono text-sm text-[var(--color-text-muted)]">
              {{ allPosts.length }} posts
            </p>
          </div>
        </div>
      </div>
    </div>

    <div class="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      <!-- ── Featured post ─────────────────────────────────── -->
      <div v-if="!activeCategory && featuredPost" class="mb-12">
        <BlogFeaturedPost :post="featuredPost" />
      </div>

      <!-- ── Main: grid + sidebar ──────────────────────────── -->
      <div class="flex flex-col gap-10 lg:flex-row">
        <!-- Posts grid -->
        <div class="min-w-0 flex-1">
          <!-- Active category header -->
          <div v-if="activeCategory" class="mb-6 flex items-center gap-3">
            <BlogCategoryBadge :category="activeCategory" size="md" />
            <span class="text-sm text-[var(--color-text-muted)]">
              {{ gridPosts.length }} {{ gridPosts.length === 1 ? 'post' : 'posts' }}
            </span>
            <button
              type="button"
              class="ml-auto text-xs text-[var(--color-text-muted)] underline underline-offset-4 transition-colors duration-150 hover:text-[var(--color-text-primary)] focus-visible:outline-none"
              @click="activeCategory = null"
            >
              Clear filter
            </button>
          </div>

          <!-- Empty state — uses UiBaseCard + UiBaseButton -->
          <UiBaseCard
            v-if="gridPosts.length === 0"
            padding="none"
            class="flex flex-col items-center justify-center border-dashed py-24 text-center"
          >
            <p
              class="mb-2 font-mono text-xs uppercase tracking-widest text-[var(--color-text-muted)]"
            >
              Nothing here yet
            </p>
            <p class="mb-5 text-sm text-[var(--color-text-secondary)]">
              No posts in this category.
            </p>
            <UiBaseButton variant="ghost" size="sm" @click="activeCategory = null">
              Show all posts
            </UiBaseButton>
          </UiBaseCard>

          <!-- Grid -->
          <div v-else class="grid grid-cols-1 gap-5 sm:grid-cols-2">
            <BlogCard v-for="(post, i) in gridPosts" :key="post.id" :post="post" :index="i" />
          </div>
        </div>

        <!-- Sidebar -->
        <aside class="w-full flex-shrink-0 lg:w-64 xl:w-72" aria-label="Blog sidebar">
          <div class="flex flex-col gap-6 lg:sticky lg:top-[calc(var(--nav-height)+1.5rem)]">
            <!-- Category filter — uses UiBaseCard -->
            <UiBaseCard padding="sm" flat>
              <BlogCategoryFilter
                v-model="activeCategory"
                :counts="categoryCounts"
                :total="allPosts.length"
              />
            </UiBaseCard>

            <!-- About this blog — uses UiBaseCard + UiBaseLink -->
            <UiBaseCard padding="sm" flat>
              <p
                class="mb-3 font-mono text-[10px] uppercase tracking-[0.15em] text-[var(--color-text-muted)]"
              >
                About Infodumps
              </p>
              <p class="text-sm leading-relaxed text-[var(--color-text-secondary)]">
                Written by IEEE Oulu board members and contributors. Covers everything from event
                recaps to deep technical tutorials.
              </p>
              <p class="mt-2 text-sm leading-relaxed text-[var(--color-text-secondary)]">
                Got something to share? Members can pitch a post — say hi on LinkedIn.
              </p>
              <UiBaseLink
                href="https://www.linkedin.com/company/ieeesb-oulu"
                external
                class="mt-4 inline-flex items-center gap-1.5 text-xs font-medium text-[var(--color-ieee-blue)] transition-colors duration-150 hover:text-[var(--color-ieee-blue-light)] focus-visible:underline focus-visible:outline-none"
              >
                Connect on LinkedIn
                <svg
                  class="size-3.5"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  aria-hidden="true"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M7 17L17 7M17 7H7M17 7v10"
                  />
                </svg>
              </UiBaseLink>
            </UiBaseCard>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>
