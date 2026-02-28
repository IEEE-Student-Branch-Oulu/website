/**
 * useBlog
 *
 * Shared types, category metadata, dummy post data, and TOC scroll-spy.
 * TODO: Replace DUMMY_POSTS and fetching logic with useFetch('/api/v1/posts')
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
}

// The full post extends meta with rendered body content
export interface BlogPostFull extends BlogPostMeta {
  headings: TocHeading[]
  bodyHtml: string // Pre-rendered HTML (from markdown-it in production)
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

// ── Dummy post data ────────────────────────────────────────────

export const DUMMY_POSTS: BlogPostMeta[] = [
  {
    id: 1,
    title: 'How We Built a Working Radar System with a $20 SDR Dongle and GNU Radio',
    slug: 'gnu-radio-sdr-radar-workshop',
    excerpt:
      "Eighteen students, one afternoon, zero prior radar experience. Here's how we turned cheap hardware and open-source signal processing software into a working object detection system — and what we learned along the way.",
    category: 'workshop-recap',
    author: 'Juhani Virtanen',
    authorInitials: 'JV',
    authorRole: 'Technical Officer',
    date: 'Feb 12, 2026',
    dateISO: '2026-02-12',
    readTime: '9 min read',
    tags: ['SDR', 'GNU Radio', 'RF', 'Python', 'Workshop'],
    featured: true,
  },
  {
    id: 2,
    title: "Linux Ricing for Engineers: A Practical Guide to a Terminal You'll Actually Enjoy",
    slug: 'linux-ricing-guide-engineers',
    excerpt:
      "Your dev environment is the tool you use more than any other. Here's a no-nonsense guide to a fast, beautiful, keyboard-driven workflow using Neovim, tmux, and a tiling WM — built around engineering tasks, not aesthetics for their own sake.",
    category: 'tutorial',
    author: 'Mikael Korhonen',
    authorInitials: 'MK',
    authorRole: 'IT Officer',
    date: 'Feb 3, 2026',
    dateISO: '2026-02-03',
    readTime: '14 min read',
    tags: ['Linux', 'Neovim', 'tmux', 'Workflow', 'Terminal'],
  },
  {
    id: 3,
    title: 'IEEE Oulu Wins Best Student Branch Activity Award at Finland Section Annual Meeting',
    slug: 'ieee-oulu-best-activity-award-2025',
    excerpt:
      "At the IEEE Finland Section Annual Meeting in Helsinki, the Oulu Student Branch was recognised for outstanding technical activity and membership growth in 2025. Here's what we submitted, and what it means for the branch going forward.",
    category: 'branch-news',
    author: 'IEEE Oulu Board',
    authorInitials: 'IB',
    authorRole: 'Executive Board',
    date: 'Feb 1, 2026',
    dateISO: '2026-02-01',
    readTime: '4 min read',
    tags: ['IEEE Finland', 'Award', 'Announcement'],
  },
  {
    id: 4,
    title: '6G Is Not Just Faster 5G — Notes from the Nokia Bell Labs Talk',
    slug: '6g-nokia-tech-talk-notes',
    excerpt:
      "Dr. Aino Mäkinen's talk dismantled a lot of assumptions. 6G isn't about raw throughput — it's about sensing, positioning, and native AI integration at the radio level. Here's what we took away.",
    category: 'tech-notes',
    author: 'Aleksi Heikkinen',
    authorInitials: 'AH',
    authorRole: 'Chair',
    date: 'Jan 20, 2026',
    dateISO: '2026-01-20',
    readTime: '7 min read',
    tags: ['6G', 'Nokia', 'Wireless', 'AI'],
  },
  {
    id: 5,
    title: 'Embedded Hackathon 2025: What Got Built, What Broke, and What We Learned',
    slug: 'embedded-hackathon-2025-recap',
    excerpt:
      '24 hours, 8 teams, STM32 boards, and exactly one working oscilloscope between them. The results were impressive. The process was chaos. This is how it went.',
    category: 'event-recap',
    author: 'Juhani Virtanen',
    authorInitials: 'JV',
    authorRole: 'Technical Officer',
    date: 'Nov 8, 2025',
    dateISO: '2025-11-08',
    readTime: '11 min read',
    tags: ['Hackathon', 'STM32', 'Embedded', 'Hardware'],
  },
  {
    id: 6,
    title: 'How to Write Your First IEEE Conference Paper Without Losing Your Mind',
    slug: 'writing-ieee-conference-paper-guide',
    excerpt:
      "LaTeX, IEEEtran, citations, figures, page limits. It's a lot. This is the guide we wish we had before our first submission — from structuring your contribution to surviving the review process.",
    category: 'tutorial',
    author: 'Elina Saarinen',
    authorInitials: 'ES',
    authorRole: 'Secretary',
    date: 'Oct 30, 2025',
    dateISO: '2025-10-30',
    readTime: '12 min read',
    tags: ['LaTeX', 'IEEE', 'Research', 'Academic Writing'],
  },
]

// ── Full post content (single post used for [slug].vue demo) ──

export const DUMMY_FULL_POST: BlogPostFull = {
  ...DUMMY_POSTS[0]!,
  headings: [
    { id: 'background', text: 'Background & Motivation', level: 2 },
    { id: 'hardware', text: 'The Hardware Stack', level: 2 },
    { id: 'rtl-sdr', text: 'RTL-SDR: What it Actually Is', level: 3 },
    { id: 'setup', text: 'Setting Up GNU Radio', level: 2 },
    { id: 'installing', text: 'Installation', level: 3 },
    { id: 'flowgraph', text: 'Building the Flowgraph', level: 3 },
    { id: 'the-physics', text: 'The Physics (Just Enough)', level: 2 },
    { id: 'results', text: 'Results & Limitations', level: 2 },
    { id: 'takeaways', text: 'Key Takeaways', level: 2 },
  ],
  bodyHtml: `
<p>Radar sounds like expensive defence industry hardware. For most of IEEE history, it was. But the combination of cheap software-defined radio hardware and mature open-source signal processing libraries has changed that equation completely — and our February workshop was proof.</p>

<p>In four hours, 18 students with no prior RF experience built a system that could reliably detect objects passing in front of an antenna. Here's how we did it, what broke, and what anyone can replicate at home for under €25.</p>

<h2 id="background">Background & Motivation</h2>

<p>The idea came from a throwaway comment at our December social: <em>"could we actually build a radar with one of those TV dongles?"</em>. A few weeks of reading later, the answer was clearly yes — and the workshop was born.</p>

<p>The goal wasn't to build production-grade radar. It was to make the underlying physics and signal processing tangible. There's a specific moment when an abstract concept like Doppler shift becomes real — when you move your hand in front of an antenna and watch a frequency peak appear on a spectrum. That's what we were after.</p>

<blockquote>
<p>"Understanding comes from doing. Reading about Doppler shift is fine; watching it appear in real-time on a spectrum analyser connected to hardware you built yourself is something else entirely."</p>
</blockquote>

<h2 id="hardware">The Hardware Stack</h2>

<p>The full parts list per student station came to €23:</p>

<ul>
<li>RTL-SDR v3 dongle (€18 from various suppliers)</li>
<li>Two cheap 2.4GHz patch antennas (€3 combined)</li>
<li>SMA to MCX adapter (€2)</li>
<li>Laptop with Ubuntu 22.04 or Debian 12</li>
</ul>

<p>We ordered 10 dongles in bulk from a reliable supplier three weeks in advance. The antennas were repurposed from old WiFi routers — good enough for a demonstration, not for production.</p>

<h3 id="rtl-sdr">RTL-SDR: What it Actually Is</h3>

<p>The RTL-SDR is a USB device originally designed as a DVB-T TV tuner. In 2012, it was discovered that the chip inside (Realtek RTL2832U) could be put into a raw I/Q sampling mode, turning it into a wideband software-defined radio receiver. It covers roughly 24 MHz to 1.766 GHz with a tunable bandwidth of up to 3.2 MHz.</p>

<p>It can't transmit — it's receive-only. For a continuous-wave radar demonstration, this means we need a separate transmitter, which we handled with a second device running a simple signal generator in GNU Radio.</p>

<h2 id="setup">Setting Up GNU Radio</h2>

<p>GNU Radio is the open-source toolkit that does the heavy lifting. It provides a visual programming environment (GRC — GNU Radio Companion) where you build "flowgraphs" by connecting signal processing blocks. It's Python under the hood, and every block can be extended or replaced with custom Python code.</p>

<h3 id="installing">Installation</h3>

<p>On Ubuntu/Debian, the simplest path is:</p>

<pre><code class="language-bash"># Install GNU Radio and the RTL-SDR source blocks
sudo apt update
sudo apt install gnuradio gr-osmosdr rtl-sdr

# Blacklist the kernel DVB driver so it doesn't grab the dongle
echo 'blacklist dvb_usb_rtl28xxu' | sudo tee /etc/modprobe.d/blacklist-rtl.conf
sudo modprobe -r dvb_usb_rtl28xxu

# Verify the dongle is detected
rtl_test -t</code></pre>

<p>Expected output from <code>rtl_test</code>:</p>

<pre><code class="language-text">Found 1 device(s):
  0:  Realtek, RTL2838UHIDIR, SN: 00000001

Using device 0: Generic RTL2832U OEM
Found Rafael Micro R820T tuner
Supported gain values (29): 0.0 1.0 2.0 ...
Sampling at 2048000 S/s.
No E4000 tuner found, aborting.</code></pre>

<h3 id="flowgraph">Building the Flowgraph</h3>

<p>The core radar flowgraph has four stages:</p>

<ol>
<li><strong>RTL-SDR Source</strong> — tunes to our transmit frequency, outputs raw I/Q samples</li>
<li><strong>Multiply</strong> — mixes the received signal with a local oscillator copy (the Doppler processing step)</li>
<li><strong>Low-pass Filter</strong> — removes high-frequency mixing products, isolates the Doppler shift</li>
<li><strong>FFT Sink</strong> — displays the frequency spectrum in real time</li>
</ol>

<p>In GRC, this looks like connecting four boxes with lines. The magic is that this simple graph implements the core of a continuous-wave Doppler radar.</p>

<pre><code class="language-python"># The equivalent Python (what GRC generates under the hood)
import numpy as np
from gnuradio import gr, blocks, filter, fft

class radar_flowgraph(gr.top_block):
    def __init__(self):
        super().__init__()

        samp_rate = 2.048e6  # 2.048 MS/s
        center_freq = 2.4e9  # 2.4 GHz (WiFi band, unoccupied channel)

        # RTL-SDR source
        self.rtlsdr_source = osmosdr.source()
        self.rtlsdr_source.set_sample_rate(samp_rate)
        self.rtlsdr_source.set_center_freq(center_freq)
        self.rtlsdr_source.set_gain(30)  # dB

        # Low-pass filter (isolate DC ± 10 kHz — Doppler range for walking speed)
        self.lpf = filter.fir_filter_ccf(
            decimation=1,
            taps=filter.firdes.low_pass(1, samp_rate, 10e3, 1e3)
        )

        # FFT display sink
        self.fft_sink = fft.logpwrfft_c(
            sample_rate=samp_rate,
            fft_size=1024,
            ref_scale=2,
            frame_rate=30,
            avg_alpha=0.5,
            average=True
        )

        # Wire it up
        self.connect(self.rtlsdr_source, self.lpf, self.fft_sink)</code></pre>

<h2 id="the-physics">The Physics (Just Enough)</h2>

<p>Continuous-wave radar works on the Doppler effect. When you transmit a continuous signal at frequency <em>f</em> and an object moves toward you at velocity <em>v</em>, the reflected signal comes back at a slightly shifted frequency:</p>

<p>The Doppler shift is: <code>Δf = 2v·f / c</code></p>

<p>Where <em>c</em> is the speed of light. For a hand moving at 1 m/s toward a 2.4 GHz transmitter, the Doppler shift is about 16 Hz — small, but easily detectable with GNU Radio's FFT.</p>

<p>When you mix the received signal with the transmitted signal (the multiply block in our flowgraph), any reflected components appear at the Doppler frequency rather than at DC. Moving your hand shows up as a peak that drifts left or right depending on direction of motion. This is what made the workshop click for people — it's immediately intuitive once you see it.</p>

<h2 id="results">Results & Limitations</h2>

<p>The system reliably detected:</p>

<ul>
<li>Hand movement at up to ~2 metres from the antenna</li>
<li>Directional motion (toward vs away from antenna)</li>
<li>Approximate speed (peak position in the FFT)</li>
</ul>

<p>It could <em>not</em> detect:</p>

<ul>
<li>Range (CW radar without chirp can't measure distance)</li>
<li>Multiple objects simultaneously (targets alias onto each other)</li>
<li>Slow-moving objects (below ~0.1 m/s lost in noise)</li>
</ul>

<p>Some stations had issues with RF interference from the building's WiFi network at 2.4 GHz — we'll move to a less congested frequency for the next iteration. The original plan was 5.8 GHz, but we couldn't get the antennas in time.</p>

<h2 id="takeaways">Key Takeaways</h2>

<p>A few things that surprised us running this workshop:</p>

<p>First, the <strong>bottleneck wasn't the hardware — it was the USB</strong>. Several laptops with USB 2.0 ports dropped samples under load, causing gaps in the spectrum display. Dedicated USB 3.0 ports fixed this. Worth checking before any workshop like this.</p>

<p>Second, <strong>GNU Radio Companion (GRC) is genuinely approachable</strong>. Students who had never touched signal processing connected a working flowgraph in under 30 minutes. The visual metaphor of signal flow maps well to how RF engineers think.</p>

<p>Third, and most importantly: <strong>the moment when the theory becomes real matters enormously</strong>. Multiple students said the Doppler workshop changed how they understood their antenna and wave propagation lectures. There's something irreplaceable about hardware that responds to you in real time.</p>

<p>We're planning a follow-up session on FMCW radar (the kind that can measure range) using a Raspberry Pi and a 24 GHz radar module. Watch the events page.</p>
  `,
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
