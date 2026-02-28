<script setup lang="ts">
/**
 * Blog post page ( /blog/[slug] )
 *
 * Layout:
 *   ┌────────────────────────────────────────────────┐
 *   │  Reading progress bar (fixed, under navbar)    │
 *   ├──────────────────────────┬─────────────────────┤
 *   │                          │                     │
 *   │  Post header             │  Sticky TOC         │
 *   │  Post body               │  (desktop only)     │
 *   │                          │                     │
 *   │  Author card             │                     │
 *   │  Related posts           │                     │
 *   │                          │                     │
 *   └──────────────────────────┴─────────────────────┘
 *
 * Uses:
 *   - UiBaseCard for sidebar boxes (TOC, post details, share)
 *   - UiBaseLink for the "Back to all infodumps" navigation and Twitter share link
 *   - UiBaseButton for the copy link action button
 *
 * TODO: Replace DUMMY_FULL_POST with useFetch(`/api/v1/posts/${slug}`)
 */
import { DUMMY_FULL_POST, DUMMY_POSTS, useToc } from '~/composables/useBlog'

definePageMeta({ layout: 'default' })

const _route = useRoute()

// TODO: fetch real post by slug
// const { data: post } = await useFetch(`/api/v1/posts/${_route.params.slug}`)
const post = DUMMY_FULL_POST

// 404 guard (for when real API is wired)
if (!post) {
  throw createError({ statusCode: 404, statusMessage: 'Post not found' })
}

useSeoMeta({
  title: post.title,
  description: post.excerpt,
  ogTitle: post.title,
  ogDescription: post.excerpt,
})

// ── TOC scroll-spy ────────────────────────────────────────────
const { activeId } = useToc(post.headings)

// ── Related posts (same category, excluding current) ─────────
const relatedPosts = computed(() =>
  DUMMY_POSTS.filter((p) => p.category === post.category && p.slug !== post.slug).slice(0, 3)
)

function copyLink() {
  if (import.meta.client) {
    globalThis.navigator?.clipboard?.writeText(globalThis.location.href)
  }
}
</script>

<template>
  <div>
    <!-- Reading progress bar -->
    <BlogReadingProgress />

    <div class="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <div class="flex flex-col gap-12 lg:flex-row xl:gap-16">
        <!-- ── Main content column ────────────────────────── -->
        <article class="min-w-0 max-w-3xl flex-1">
          <!-- Post header -->
          <BlogPostHeader :post="post" />

          <!-- Post body -->
          <BlogPostBody :html="post.bodyHtml" :category="post.category" />

          <!-- Post footer divider -->
          <div class="my-12 flex items-center gap-4">
            <div class="h-px flex-1 bg-[var(--color-border)]" />
            <div
              class="size-1.5 rounded-full"
              style="background-color: var(--color-ieee-blue)"
              aria-hidden="true"
            />
            <div class="h-px flex-1 bg-[var(--color-border)]" />
          </div>

          <!-- Author card -->
          <BlogPostAuthor :post="post" />

          <!-- Related posts -->
          <section v-if="relatedPosts.length" class="mt-12" aria-labelledby="related-heading">
            <h2
              id="related-heading"
              class="mb-6 font-mono text-[11px] uppercase tracking-[0.15em] text-[var(--color-text-muted)]"
            >
              Related posts
            </h2>
            <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <BlogCard v-for="(p, i) in relatedPosts" :key="p.id" :post="p" :index="i" compact />
            </div>
          </section>

          <!-- Back link — uses UiBaseLink for consistent navigation -->
          <div class="mt-12">
            <UiBaseLink
              to="/blog"
              class="inline-flex items-center gap-2 text-sm font-medium text-[var(--color-text-secondary)] transition-colors duration-150 hover:text-[var(--color-text-primary)] focus-visible:underline focus-visible:outline-none"
            >
              <svg
                class="size-4"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                aria-hidden="true"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 12H5M12 5l-7 7 7 7" />
              </svg>
              Back to all infodumps
            </UiBaseLink>
          </div>
        </article>

        <!-- ── Sticky TOC sidebar (desktop only) ─────────── -->
        <aside class="hidden w-56 flex-shrink-0 lg:block xl:w-64" aria-label="Table of contents">
          <div class="sticky top-[calc(var(--nav-height)+2rem)] flex flex-col gap-6">
            <!-- TOC — uses UiBaseCard -->
            <UiBaseCard padding="sm" flat>
              <BlogPostToc
                :headings="post.headings"
                :active-id="activeId"
                :category="post.category"
              />
            </UiBaseCard>

            <!-- Post meta card — uses UiBaseCard -->
            <UiBaseCard padding="sm" flat class="flex flex-col gap-3">
              <p
                class="font-mono text-[10px] uppercase tracking-[0.15em] text-[var(--color-text-muted)]"
              >
                Post details
              </p>

              <div class="flex items-center justify-between">
                <span class="text-xs text-[var(--color-text-muted)]">Published</span>
                <time
                  :datetime="post.dateISO"
                  class="font-mono text-xs text-[var(--color-text-secondary)]"
                >
                  {{ post.date }}
                </time>
              </div>

              <div class="flex items-center justify-between">
                <span class="text-xs text-[var(--color-text-muted)]">Reading time</span>
                <span class="font-mono text-xs text-[var(--color-text-secondary)]">{{
                  post.readTime
                }}</span>
              </div>

              <div class="flex items-center justify-between">
                <span class="text-xs text-[var(--color-text-muted)]">Category</span>
                <BlogCategoryBadge :category="post.category" size="sm" />
              </div>
            </UiBaseCard>

            <!-- Share box — uses UiBaseCard + UiBaseLink + UiBaseButton -->
            <UiBaseCard padding="sm" flat>
              <p
                class="mb-3 font-mono text-[10px] uppercase tracking-[0.15em] text-[var(--color-text-muted)]"
              >
                Share
              </p>
              <div class="flex gap-2">
                <!-- Twitter share — uses UiBaseLink for consistent external link handling -->
                <UiBaseLink
                  :href="`https://twitter.com/intent/tweet?text=${encodeURIComponent(post.title)}&url=${encodeURIComponent('https://ieee-oulu.fi/blog/' + post.slug)}`"
                  external
                  class="flex flex-1 items-center justify-center gap-1.5 rounded-lg border border-[var(--color-border)] px-3 py-2 text-xs font-medium text-[var(--color-text-secondary)] transition-all duration-150 hover:bg-[var(--color-surface-overlay)] hover:text-[var(--color-text-primary)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-ieee-blue)]"
                >
                  𝕏 / Twitter
                </UiBaseLink>

                <!-- Copy link — uses UiBaseButton for consistent button styling -->
                <UiBaseButton
                  variant="ghost"
                  size="sm"
                  class="!rounded-lg border border-[var(--color-border)] !px-3 !py-2"
                  title="Copy link"
                  @click="copyLink()"
                >
                  <svg
                    class="size-4"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    aria-hidden="true"
                  >
                    <rect x="9" y="9" width="13" height="13" rx="2" />
                    <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1" />
                  </svg>
                </UiBaseButton>
              </div>
            </UiBaseCard>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>
