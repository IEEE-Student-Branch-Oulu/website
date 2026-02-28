<script setup lang="ts">
/**
 * AppNavbar
 *
 * Site-wide navigation bar.
 * - Scrolled state: adds backdrop blur + shadow
 * - Mobile: full-screen slide-down menu
 * - Closes mobile menu on route change
 * - Dark mode toggle integrated
 *
 * No props required — all config is internal.
 * To update nav links, edit the `navLinks` array below.
 */

interface NavLink {
  label: string
  to: string
  exact?: boolean
}

const navLinks: NavLink[] = [
  { label: 'Home', to: '/', exact: true },
  { label: 'About', to: '/#' },
  { label: 'Events', to: '/events' },
  { label: 'News', to: '/blog' },
]

const socialLinks = [
  { name: 'Discord', href: 'https://discord.gg/your-server', icon: 'discord' as const },
  { name: 'Telegram', href: 'https://t.me/your-channel', icon: 'telegram' as const },
  { name: 'LinkedIn', href: 'https://linkedin.com/company/your-page', icon: 'linkedin' as const },
  { name: 'GitHub', href: 'https://github.com/ieee-oulu', icon: 'github' as const },
]

// ── State ──────────────────────────────────────────────────────
const mobileOpen = ref(false)
const isScrolled = ref(false)
const route = useRoute()

// ── Scroll detection ───────────────────────────────────────────
onMounted(() => {
  const handleScroll = () => {
    isScrolled.value = window.scrollY > 12
  }
  window.addEventListener('scroll', handleScroll, { passive: true })
  onUnmounted(() => window.removeEventListener('scroll', handleScroll))
})

// ── Close mobile menu on route change ─────────────────────────
watch(
  () => route.path,
  () => {
    mobileOpen.value = false
  }
)

// ── Lock body scroll when mobile menu is open ─────────────────
watch(mobileOpen, (open) => {
  if (import.meta.client) {
    document.body.style.overflow = open ? 'hidden' : ''
  }
})

function toggleMobile() {
  mobileOpen.value = !mobileOpen.value
}
</script>

<template>
  <header
    class="fixed left-0 right-0 top-0 z-50 transition-all duration-300"
    :class="[
      isScrolled
        ? 'border-b border-[var(--color-border)] bg-[var(--color-surface)] shadow-sm'
        : 'bg-transparent',
    ]"
  >
    <nav
      class="mx-auto flex w-full max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8"
      aria-label="Main navigation"
    >
      <IconsIeeeLogo size="lg" />

      <!-- Desktop nav links (hidden on mobile) -->
      <ul class="hidden items-center gap-1 md:flex" role="list">
        <li v-for="link in navLinks" :key="link.to">
          <NuxtLink
            :to="link.to"
            class="group relative rounded-md px-3 py-2 text-sm font-medium text-[var(--color-text-secondary)] transition-all duration-150 hover:bg-[var(--color-surface-overlay)] hover:text-[var(--color-text-primary)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-ieee-blue)]"
            :exact-active-class="'!text-[var(--color-ieee-blue)]'"
          >
            {{ link.label }}
            <!-- Active indicator line -->
            <span
              class="absolute bottom-0.5 left-3 right-3 h-0.5 scale-x-0 rounded-full bg-[var(--color-ieee-blue)] transition-transform duration-150 group-[.router-link-active]:scale-x-100"
              aria-hidden="true"
            />
          </NuxtLink>
        </li>
      </ul>

      <!-- Right side: dark toggle + CTA + hamburger -->
      <div class="flex items-center gap-2">
        <!-- Dark mode toggle — always visible -->
        <UiDarkModeToggle />

        <!-- Join Us CTA — hidden on small mobile -->
        <UiBaseButton
          href="https://discord.gg/your-server"
          variant="primary"
          size="sm"
          external
          class="hidden sm:inline-flex"
        >
          Join Us
        </UiBaseButton>

        <!-- Hamburger — visible on mobile only -->
        <button
          type="button"
          class="flex size-9 flex-col items-center justify-center gap-1.5 rounded-lg text-[var(--color-text-secondary)] transition-all duration-150 hover:bg-[var(--color-surface-overlay)] hover:text-[var(--color-text-primary)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-ieee-blue)] md:hidden"
          :aria-expanded="mobileOpen"
          aria-controls="mobile-menu"
          :aria-label="mobileOpen ? 'Close menu' : 'Open menu'"
          @click="toggleMobile"
        >
          <!-- Animated hamburger lines -->
          <span
            class="block h-0.5 w-5 origin-center rounded-full bg-current transition-all duration-300"
            :class="mobileOpen ? 'translate-y-2 rotate-45' : ''"
            aria-hidden="true"
          />
          <span
            class="block h-0.5 w-5 rounded-full bg-current transition-all duration-300"
            :class="mobileOpen ? 'scale-x-0 opacity-0' : ''"
            aria-hidden="true"
          />
          <span
            class="block h-0.5 w-5 origin-center rounded-full bg-current transition-all duration-300"
            :class="mobileOpen ? '-translate-y-2 -rotate-45' : ''"
            aria-hidden="true"
          />
        </button>
      </div>
    </nav>

    <!-- Mobile menu -->
    <Transition
      enter-active-class="transition-all duration-300 ease-out"
      enter-from-class="opacity-0 -translate-y-2"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition-all duration-200 ease-in"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 -translate-y-2"
    >
      <div
        v-if="mobileOpen"
        id="mobile-menu"
        class="absolute left-0 right-0 top-full border-b border-[var(--color-border)] bg-[var(--color-surface)] shadow-lg md:hidden"
      >
        <!-- Nav links -->
        <ul class="px-4 py-2" role="list">
          <li v-for="link in navLinks" :key="link.to">
            <NuxtLink
              :to="link.to"
              class="flex items-center gap-3 rounded-lg px-3 py-3 text-base font-medium text-[var(--color-text-secondary)] transition-all duration-150 hover:bg-[var(--color-surface-overlay)] hover:text-[var(--color-text-primary)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-ieee-blue)]"
              :exact-active-class="'!text-[var(--color-ieee-blue)] !bg-[var(--color-surface-overlay)]'"
            >
              {{ link.label }}
            </NuxtLink>
          </li>
        </ul>

        <!-- Divider -->
        <div class="mx-4 border-t border-[var(--color-border)]" />

        <!-- Bottom row: social + CTA -->
        <div class="flex items-center justify-between px-4 py-3">
          <IconsSocialIcons :links="socialLinks" size="sm" />
          <UiBaseButton href="https://discord.gg/your-server" variant="primary" size="sm" external>
            Join Us
          </UiBaseButton>
        </div>
      </div>
    </Transition>
  </header>
</template>
