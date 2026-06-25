/**
 * useBlog
 *
 * Shared types, category metadata, API client, and TOC scroll-spy.
 */

// ── Types ──────────────────────────────────────────────────────

export type PostCategory =
  | 'workshop-recap'
  | 'tutorial'
  | 'branch-news'
  | 'tech-notes'
  | 'event-recap'

export interface TocHeading {
  id: string
  text: string
  level: 2 | 3
}

export interface BlogPostMeta {
  id: number
  title: string
  slug: string
  excerpt: string
  category: PostCategory
  author: string
  authorInitials: string
  authorRole: string
  date: string // Display: "Feb 12, 2026"
  dateISO: string
  readTime: string
  tags: string[]
  featured?: boolean // Shows in hero slot
  coverImageUrl?: string | null
  eventSlug?: string | null // Optional link to a past event this post recaps
}

// The full post extends meta with rendered body content
export interface BlogPostFull extends BlogPostMeta {
  headings: TocHeading[]
  bodyHtml: string // Pre-rendered HTML (from markdown-it in production)
}

// Raw, editable post (markdown source) — admin forms only.
export interface BlogPostEdit {
  id: number
  slug: string
  title: string
  excerpt: string
  bodyMd: string
  category: PostCategory
  tags: string[]
  featured: boolean
  coverImageUrl?: string | null
  eventSlug?: string | null
  publishedOn: string
  authorName: string
  authorInitials: string
  authorRole: string
}

// Payload for create/update.
export interface BlogPostInput {
  title: string
  excerpt: string
  bodyMd: string
  category: PostCategory
  tags: string[]
  featured: boolean
  coverImageUrl?: string | null
  eventSlug?: string | null
  publishedOn?: string | null
}

export interface Paginated<T> {
  items: T[]
  total: number
  limit: number
  offset: number
}

// ── API client ─────────────────────────────────────────────────

export function useBlogApi() {
  const { api } = useApi()
  return {
    list: (category?: PostCategory | null, limit = 100) =>
      api<Paginated<BlogPostMeta>>('/posts', {
        query: { category: category ?? undefined, limit },
      }),
    get: (slug: string) => api<BlogPostFull>(`/posts/${slug}`),
    getRaw: (id: number) => api<BlogPostEdit>(`/posts/${id}/raw`),
    create: (body: BlogPostInput) => api<BlogPostFull>('/posts', { method: 'POST', body }),
    update: (id: number, body: Partial<BlogPostInput>) =>
      api<BlogPostFull>(`/posts/${id}`, { method: 'PUT', body }),
    remove: (id: number) => api<null>(`/posts/${id}`, { method: 'DELETE' }),
  }
}

// ── Category metadata ──────────────────────────────────────────

export const CATEGORY_META: Record<
  PostCategory,
  {
    label: string
    color: string // CSS var or Tailwind class for accent
    badgeClass: string // text + bg tailwind classes
    borderClass: string // border-left color
  }
> = {
  'workshop-recap': {
    label: 'Workshop Recap',
    color: 'var(--color-ieee-blue)',
    badgeClass: 'bg-[var(--color-ieee-blue)]/10 text-[var(--color-ieee-blue)]',
    borderClass: 'border-[var(--color-ieee-blue)]',
  },
  tutorial: {
    label: 'Tutorial',
    color: '#10b981',
    badgeClass: 'bg-emerald-500/10 text-emerald-700 dark:text-emerald-400',
    borderClass: 'border-emerald-500',
  },
  'branch-news': {
    label: 'Branch News',
    color: '#f59e0b',
    badgeClass: 'bg-amber-500/10 text-amber-700 dark:text-amber-400',
    borderClass: 'border-amber-500',
  },
  'tech-notes': {
    label: 'Tech Notes',
    color: '#8b5cf6',
    badgeClass: 'bg-purple-500/10 text-purple-700 dark:text-purple-400',
    borderClass: 'border-purple-500',
  },
  'event-recap': {
    label: 'Event Recap',
    color: '#f43f5e',
    badgeClass: 'bg-rose-500/10 text-rose-700 dark:text-rose-400',
    borderClass: 'border-rose-500',
  },
}

// ── TOC scroll-spy composable ──────────────────────────────────

/**
 * useToc
 *
 * Tracks which heading is currently in the viewport as the user scrolls.
 * Returns the ID of the active heading for TOC highlighting.
 *
 * Usage:
 *   const { activeId } = useToc(headings)
 *   // bind :class="{ active: activeId === heading.id }" on TOC items
 */
export function useToc(headings: TocHeading[]) {
  const activeId = ref<string>(headings[0]?.id ?? '')

  onMounted(() => {
    const observers: IntersectionObserver[] = []

    headings.forEach(({ id }) => {
      const el = document.getElementById(id)
      if (!el) return

      const observer = new IntersectionObserver(
        ([entry]) => {
          if (entry?.isIntersecting) activeId.value = id
        },
        {
          rootMargin: '-20% 0px -70% 0px', // Triggers when heading is in upper 30% of viewport
          threshold: 0,
        }
      )

      observer.observe(el)
      observers.push(observer)
    })

    onUnmounted(() => observers.forEach((o) => o.disconnect()))
  })

  return { activeId }
}

/**
 * useReadingProgress
 *
 * Tracks scroll position as a 0–100 percentage for a reading progress bar.
 *
 * Usage:
 *   const { progress } = useReadingProgress()
 *   <div :style="{ width: progress + '%' }" />
 */
export function useReadingProgress() {
  const progress = ref(0)

  onMounted(() => {
    const update = () => {
      const scrollTop = window.scrollY
      const docHeight = document.documentElement.scrollHeight - window.innerHeight
      progress.value = docHeight > 0 ? Math.min((scrollTop / docHeight) * 100, 100) : 0
    }

    window.addEventListener('scroll', update, { passive: true })
    onUnmounted(() => window.removeEventListener('scroll', update))
  })

  return { progress }
}
