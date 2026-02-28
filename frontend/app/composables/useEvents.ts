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

// ── Dummy data — replace with useFetch('/api/v1/events') ─────────
export const DUMMY_EVENTS: EventItem[] = [
  {
    id: 1,
    title: 'AI & Machine Learning Workshop',
    slug: 'ai-ml-workshop-march-2026',
    description:
      'A hands-on introduction to ML fundamentals. Train a real classifier from scratch using Python and scikit-learn. No prior ML experience required — just bring a laptop with Python installed.',
    dateISO: '2026-03-15T13:00:00',
    dateDisplay: 'Sat, Mar 15, 2026',
    timeDisplay: '13:00 – 17:00 EET',
    location: 'Linnanmaa Campus, Room TS101',
    locationUrl: 'https://maps.google.com/?q=University+of+Oulu',
    type: 'workshop',
    status: 'upcoming',
    rsvpLink: 'https://forms.gle/placeholder',
    capacity: 30,
    spotsLeft: 7,
    tags: ['Python', 'ML', 'scikit-learn'],
    isHighlighted: true,
  },
  {
    id: 2,
    title: 'Spring General Meeting 2026',
    slug: 'spring-general-meeting-2026',
    description:
      'Our spring general meeting. Agenda: board activity reports, budget overview, summer plans, and open floor for member proposals. Free pizza after.',
    dateISO: '2026-03-22T17:00:00',
    dateDisplay: 'Sun, Mar 22, 2026',
    timeDisplay: '17:00 – 19:00 EET',
    location: 'Linnanmaa Campus, Room L2',
    type: 'meeting',
    status: 'upcoming',
    rsvpLink: 'https://forms.gle/placeholder',
    tags: ['Official', 'Open to all'],
  },
  {
    id: 3,
    title: 'Game Night & Social Mixer',
    slug: 'game-night-april-2026',
    description:
      'Decompress from the thesis grind. Board games, video games, and good people. No agenda, no slides. Just show up.',
    dateISO: '2026-04-04T18:00:00',
    dateDisplay: 'Sat, Apr 4, 2026',
    timeDisplay: '18:00 – 22:00 EET',
    location: 'OTK Student Club, Linnanmaa',
    type: 'social',
    status: 'upcoming',
    tags: ['Free', 'Casual'],
  },
  {
    id: 4,
    title: '6G & Beyond: A Tech Talk with Nokia Bell Labs',
    slug: '6g-tech-talk-nokia-april-2026',
    description:
      'A researcher from Nokia Bell Labs walks through the architecture and radio physics challenges of 6G. Q&A afterwards. Strong ties to telecom thesis topics.',
    dateISO: '2026-04-17T14:00:00',
    dateDisplay: 'Fri, Apr 17, 2026',
    timeDisplay: '14:00 – 15:30 EET',
    location: 'Linnanmaa Campus, Auditorium L10',
    type: 'talk',
    status: 'upcoming',
    rsvpLink: 'https://forms.gle/placeholder',
    tags: ['6G', 'Nokia', 'Wireless'],
    speakerName: 'Dr. Aino Mäkinen',
    speakerTitle: 'Senior Researcher, Nokia Bell Labs',
    isHighlighted: true,
  },
  {
    id: 5,
    title: 'GNU Radio & SDR Workshop',
    slug: 'gnu-radio-sdr-workshop-feb-2026',
    description:
      'Built a working radar system with a $20 RTL-SDR dongle and GNU Radio. 18 attendees went from zero to detecting passing cars in four hours.',
    dateISO: '2026-02-08T13:00:00',
    dateDisplay: 'Sat, Feb 8, 2026',
    timeDisplay: '13:00 – 17:00 EET',
    location: 'Linnanmaa Campus, Room TS101',
    type: 'workshop',
    status: 'past',
    tags: ['SDR', 'GNU Radio', 'RF'],
  },
  {
    id: 6,
    title: 'Winter Social & Christmas Dinner',
    slug: 'winter-social-dec-2025',
    description:
      'End-of-year celebration. Good food, board game tournament, and the annual "Worst Commit Message of the Year" award.',
    dateISO: '2025-12-13T18:00:00',
    dateDisplay: 'Sat, Dec 13, 2025',
    timeDisplay: '18:00 – 23:00 EET',
    location: 'Restaurant Laseri, Oulu',
    type: 'social',
    status: 'past',
    tags: ['Annual', 'Dinner'],
  },
  {
    id: 7,
    title: 'Embedded Systems Hackathon',
    slug: 'embedded-hackathon-nov-2025',
    description:
      '24-hour hackathon focused on embedded systems. Teams of 2–3 built projects using STM32 boards provided by the branch. Winner built an autonomous plant-watering system.',
    dateISO: '2025-11-01T10:00:00',
    dateDisplay: 'Sat, Nov 1, 2025',
    timeDisplay: '10:00 – Nov 2, 10:00 EET',
    location: 'Linnanmaa Campus, Fab Lab',
    type: 'hackathon',
    status: 'past',
    tags: ['STM32', '24h', 'Hardware'],
    isHighlighted: true,
  },
  {
    id: 8,
    title: 'Nokia Factory Excursion',
    slug: 'nokia-excursion-oct-2025',
    description:
      "A guided tour of Nokia's Oulu R&D facility. Students saw 5G base station prototyping labs and met engineers working on antenna design.",
    dateISO: '2025-10-14T09:00:00',
    dateDisplay: 'Tue, Oct 14, 2025',
    timeDisplay: '09:00 – 13:00 EET',
    location: 'Nokia Oulu R&D Campus',
    type: 'excursion',
    status: 'past',
    tags: ['Nokia', '5G', 'Industry'],
  },
]
