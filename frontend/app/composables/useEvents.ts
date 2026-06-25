/**
 * Event types, shared interfaces, and dummy data.
 * When the API is ready, delete the dummy data and import from the API composable.
 */

export type EventStatus = 'upcoming' | 'past' | 'ongoing'
export type EventType = 'workshop' | 'talk' | 'social' | 'meeting' | 'hackathon' | 'excursion'
export type EventFilter = 'all' | 'upcoming' | 'past' | EventType

export interface EventItem {
  id: number
  title: string
  slug: string
  description: string
  dateISO: string // ISO 8601 — for sorting and countdown
  dateDisplay: string // "Sat, Mar 15, 2026"
  timeDisplay: string // "13:00 – 17:00 EET"
  location: string
  locationUrl?: string // Google Maps link? Maybe mazemap?
  type: EventType
  status: EventStatus
  rsvpLink?: string
  capacity?: number
  spotsLeft?: number
  tags: string[]
  speakerName?: string
  speakerTitle?: string
  isHighlighted?: boolean // pinned / featured event
  coverImageUrl?: string | null
}

// Raw, editable event — admin forms only.
export interface EventEdit {
  id: number
  slug: string
  title: string
  description: string
  startsAt: string // ISO
  endsAt?: string | null
  location: string
  locationUrl?: string | null
  type: EventType
  rsvpLink?: string | null
  capacity?: number | null
  speakerName?: string | null
  speakerTitle?: string | null
  isHighlighted: boolean
  tags: string[]
  coverImageUrl?: string | null
}

// Payload for create/update.
export interface EventInput {
  title: string
  description: string
  startsAt: string
  endsAt?: string | null
  location: string
  locationUrl?: string | null
  type: EventType
  rsvpLink?: string | null
  capacity?: number | null
  speakerName?: string | null
  speakerTitle?: string | null
  isHighlighted: boolean
  tags: string[]
  coverImageUrl?: string | null
}

// `Paginated<T>` is defined in useBlog.ts and auto-imported.

// ── API client ─────────────────────────────────────────────────

export function useEventsApi() {
  const { api } = useApi()
  return {
    list: (status?: 'upcoming' | 'past' | 'ongoing', limit = 100) =>
      api<Paginated<EventItem>>('/events', { query: { status, limit } }),
    get: (slug: string) => api<EventItem>(`/events/${slug}`),
    getNext: () => api<EventItem>('/events/next'),
    getRaw: (id: number) => api<EventEdit>(`/events/${id}/raw`),
    create: (body: EventInput) => api<EventItem>('/events', { method: 'POST', body }),
    update: (id: number, body: Partial<EventInput>) =>
      api<EventItem>(`/events/${id}`, { method: 'PUT', body }),
    remove: (id: number) => api<null>(`/events/${id}`, { method: 'DELETE' }),
  }
}

// ── Type metadata (label, colors) ───────────────────────────────
export const EVENT_TYPE_META: Record<
  EventType,
  {
    label: string
    badgeVariant: 'blue' | 'green' | 'orange' | 'red' | 'purple' | 'default'
    accent: string // Tailwind bg class for the card stripe
  }
> = {
  workshop: { label: 'Workshop', badgeVariant: 'blue', accent: 'bg-[var(--color-ieee-blue)]' },
  talk: { label: 'Tech Talk', badgeVariant: 'purple', accent: 'bg-purple-500' },
  social: { label: 'Social', badgeVariant: 'green', accent: 'bg-emerald-500' },
  meeting: { label: 'Gen. Meeting', badgeVariant: 'default', accent: 'bg-slate-400' },
  hackathon: { label: 'Hackathon', badgeVariant: 'red', accent: 'bg-red-500' },
  excursion: { label: 'Excursion', badgeVariant: 'orange', accent: 'bg-orange-500' },
}
