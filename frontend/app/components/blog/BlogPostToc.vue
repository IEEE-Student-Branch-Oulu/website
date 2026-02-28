<script setup lang="ts">
/**
 * BlogPostToc
 *
 * Sticky table of contents for post pages.
 * Shows h2 and h3 headings; highlights the active one using scroll-spy.
 * Clicking an item smooth-scrolls to the heading.
 *
 * Props:
 *   headings  - TocHeading[] from BlogPostFull
 *   activeId  - currently active heading ID (from useToc)
 *
 * Usage:
 *   const { activeId } = useToc(post.headings)
 *   <BlogPostToc :headings="post.headings" :active-id="activeId" />
 */
import { CATEGORY_META, type TocHeading, type PostCategory } from '~/composables/useBlog'

interface Props {
  headings: TocHeading[]
  activeId: string
  category?: PostCategory
}

const props = withDefaults(defineProps<Props>(), { category: 'workshop-recap' })

const accentColor = computed(() =>
  props.category ? CATEGORY_META[props.category].color : 'var(--color-ieee-blue)'
)

function scrollTo(id: string) {
  const el = document.getElementById(id)
  if (!el) return
  const offset = 80 + 16 // nav height + some breathing room
  const top = el.getBoundingClientRect().top + window.scrollY - offset
  window.scrollTo({ top, behavior: 'smooth' })
}
</script>

<template>
  <nav aria-label="Table of contents">
    <p
      class="mb-4 font-mono text-[10px] uppercase tracking-[0.15em] text-[var(--color-text-muted)]"
    >
      On this page
    </p>

    <ul class="relative flex flex-col gap-0.5" role="list">
      <!-- Active indicator line -->
      <div
        class="absolute bottom-0 left-0 top-0 w-px bg-[var(--color-border)]"
        aria-hidden="true"
      />

      <li v-for="heading in headings" :key="heading.id">
        <button
          type="button"
          :class="[
            'w-full py-1 text-left transition-all duration-150',
            'focus-visible:underline focus-visible:outline-none',
            heading.level === 3 ? 'pl-5' : 'pl-3',
            activeId === heading.id
              ? 'font-medium text-[var(--color-text-primary)]'
              : 'text-[var(--color-text-muted)] hover:text-[var(--color-text-secondary)]',
          ]"
          :style="activeId === heading.id ? { color: accentColor } : {}"
          @click="scrollTo(heading.id)"
        >
          <!-- Active marker dot -->
          <span
            v-if="activeId === heading.id"
            class="absolute left-[-2.5px] mt-[0.4em] size-[5px] rounded-full transition-all duration-200"
            :style="{ backgroundColor: accentColor }"
            aria-hidden="true"
          />
          <span class="text-xs leading-relaxed">{{ heading.text }}</span>
        </button>
      </li>
    </ul>
  </nav>
</template>
