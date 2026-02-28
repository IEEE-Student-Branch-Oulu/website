<script setup lang="ts">
/**
 * AppFooter
 *
 * Site-wide footer.
 * - IEEE boilerplate and copyright (auto-updates year)
 * - Links to University of Oulu pages
 * - Social media links
 * - Branch contact info
 *
 * No props — all config is internal.
 * Update links in the config arrays below.
 */

const currentYear = new Date().getFullYear()

const navLinks = [
  { label: 'Home', to: '/' },
  { label: 'About', to: '/#' },
  { label: 'Events', to: '/events' },
  { label: 'News', to: '/#' },
]

const universityLinks = [
  { label: 'University of Oulu', href: 'https://www.oulu.fi/en' },
  { label: 'Student Union (OYY)', href: 'https://oyy.fi/en' },
  {
    label: 'Faculty of ITEE',
    href: 'https://www.oulu.fi/en/university/faculties-and-units/faculty-information-technology-and-electrical-engineering',
  },
  { label: 'IEEE Finland Section', href: 'https://www.ieee.fi' },
]

const socialLinks = [
  { name: 'Discord', href: 'https://discord.gg/your-server', icon: 'discord' as const },
  { name: 'Telegram', href: 'https://t.me/your-channel', icon: 'telegram' as const },
  { name: 'LinkedIn', href: 'https://linkedin.com/company/your-page', icon: 'linkedin' as const },
  { name: 'GitHub', href: 'https://github.com/ieee-oulu', icon: 'github' as const },
]
</script>

<template>
  <footer
    class="mt-auto border-t border-[var(--color-border)] bg-[var(--color-surface-raised)]"
    aria-label="Site footer"
  >
    <!-- Main footer content -->
    <div class="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 gap-10 sm:grid-cols-2 lg:grid-cols-4">
        <!-- Column 1: Brand -->
        <div class="flex flex-col gap-4 lg:col-span-1">
          <IconsIeeeLogo size="md" />
          <p class="max-w-xs text-sm leading-relaxed text-[var(--color-text-muted)]">
            IEEE Student Branch at the University of Oulu. Connecting engineering students,
            advancing technology, building community.
          </p>
          <IconsSocialIcons :links="socialLinks" />
        </div>

        <!-- Column 2: Navigation -->
        <div>
          <h3
            class="mb-4 text-xs font-semibold uppercase tracking-widest text-[var(--color-text-muted)]"
          >
            Navigation
          </h3>
          <ul class="flex flex-col gap-2.5" role="list">
            <li v-for="link in navLinks" :key="link.to">
              <NuxtLink
                :to="link.to"
                class="text-sm text-[var(--color-text-secondary)] transition-colors duration-150 hover:text-[var(--color-ieee-blue)] focus-visible:underline focus-visible:outline-none"
              >
                {{ link.label }}
              </NuxtLink>
            </li>
          </ul>
        </div>

        <!-- Column 3: University links -->
        <div>
          <h3
            class="mb-4 text-xs font-semibold uppercase tracking-widest text-[var(--color-text-muted)]"
          >
            University
          </h3>
          <ul class="flex flex-col gap-2.5" role="list">
            <li v-for="link in universityLinks" :key="link.href">
              <a
                :href="link.href"
                target="_blank"
                rel="noopener noreferrer"
                class="group inline-flex items-center gap-1.5 text-sm text-[var(--color-text-secondary)] transition-colors duration-150 hover:text-[var(--color-ieee-blue)] focus-visible:underline focus-visible:outline-none"
              >
                {{ link.label }}
                <!-- External link indicator -->
                <svg
                  class="size-3 -translate-y-0.5 opacity-0 transition-all duration-150 group-hover:opacity-100"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  aria-hidden="true"
                >
                  <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6" />
                  <polyline points="15,3 21,3 21,9" />
                  <line x1="10" y1="14" x2="21" y2="3" />
                </svg>
              </a>
            </li>
          </ul>
        </div>

        <!-- Column 4: Contact / IEEE -->
        <div>
          <h3
            class="mb-4 text-xs font-semibold uppercase tracking-widest text-[var(--color-text-muted)]"
          >
            Contact
          </h3>
          <address class="flex flex-col gap-2.5 not-italic">
            <p class="text-sm text-[var(--color-text-secondary)]">
              Linnanmaa Campus<br />
              Pentti Kaiteran katu 1<br />
              90570 Oulu, Finland
            </p>
            <a
              href="mailto:ieee@oulu.fi"
              class="text-sm text-[var(--color-text-secondary)] transition-colors duration-150 hover:text-[var(--color-ieee-blue)] focus-visible:underline focus-visible:outline-none"
            >
              ieee@oulu.fi
            </a>
          </address>
        </div>
      </div>
    </div>

    <!-- Bottom bar -->
    <div class="border-t border-[var(--color-border)]">
      <div
        class="mx-auto flex max-w-7xl flex-col items-center justify-between gap-3 px-4 py-4 sm:flex-row sm:px-6 lg:px-8"
      >
        <p class="text-center text-xs text-[var(--color-text-muted)] sm:text-left">
          © {{ currentYear }} IEEE Oulu Student Branch. All rights reserved.
        </p>
        <p class="text-center text-xs text-[var(--color-text-muted)] sm:text-right">
          Part of
          <a
            href="https://www.ieee.org"
            target="_blank"
            rel="noopener noreferrer"
            class="text-[var(--color-ieee-blue)] hover:underline focus-visible:underline focus-visible:outline-none"
          >
            IEEE
          </a>
          ·
          <a
            href="https://www.ieee.fi"
            target="_blank"
            rel="noopener noreferrer"
            class="text-[var(--color-ieee-blue)] hover:underline focus-visible:underline focus-visible:outline-none"
          >
            Finland Section
          </a>
        </p>
      </div>
    </div>
  </footer>
</template>
