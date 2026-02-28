<script setup lang="ts">
/**
 * HeroSection
 *
 * Full-viewport hero section.
 *
 * Design:
 *   - CSS dot-grid background evokes circuit boards / graph paper
 *   - Left-aligned editorial layout
 *   - Staggered fade-up entrance animations (no JS needed)
 *   - Inline stats bar at the bottom
 *
 * No props — content is static copywriting.
 * When the API is ready, the "next event" badge can be wired to real data.
 */

const stats = [
  { value: '130+', label: 'Members' },
  { value: '47', label: 'Events Hosted' },
  { value: '3', label: 'Active Years' },
  { value: '2', label: 'Regional Awards' },
]
</script>

<template>
  <section
    class="relative flex min-h-[calc(100vh-var(--nav-height))] flex-col justify-center overflow-hidden"
    aria-label="Introduction"
  >
    <!-- Dot grid background -->
    <div class="hero-bg pointer-events-none absolute inset-0" aria-hidden="true" />

    <!-- Blue radial glow — top right -->
    <div
      class="bg-[var(--color-ieee-blue)]/5 dark:bg-[var(--color-ieee-blue)]/8 pointer-events-none absolute -right-40 -top-40 h-[600px] w-[600px] rounded-full blur-3xl"
      aria-hidden="true"
    />

    <!-- Content -->
    <div class="relative mx-auto w-full max-w-7xl px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
      <div class="max-w-3xl">
        <!-- Eyebrow label -->
        <p
          class="hero-item mb-6 font-mono text-[11px] uppercase tracking-[0.18em] text-[var(--color-ieee-blue)]"
          style="animation-delay: 0ms"
        >
          IEEE Oulu · Student Branch · Est. 2026
        </p>

        <!-- Headline -->
        <h1
          class="hero-item mb-6 text-5xl font-bold leading-[1.05] tracking-tight sm:text-6xl lg:text-7xl"
          style="animation-delay: 80ms"
        >
          Building with <br />
          <span class="text-[var(--color-ieee-blue)]">Arctic Attitude</span>
          <br />
          at Uni Oulu.
        </h1>

        <!-- Subheadline -->
        <p
          class="hero-item mb-10 max-w-xl text-lg leading-relaxed text-[var(--color-text-secondary)] sm:text-xl"
          style="animation-delay: 160ms"
        >
          The official IEEE Student Branch for the scientifically minded. Join us for hands-on
          workshops, deep-dive tech talks, and a community of engineers who actually ship things.
        </p>

        <!-- CTAs -->
        <div class="hero-item mb-16 flex flex-wrap gap-3" style="animation-delay: 240ms">
          <UiBaseButton to="/events" variant="primary" size="lg">
            View Upcoming Events
          </UiBaseButton>
          <UiBaseButton
            href="https://discord.gg/your-server"
            variant="secondary"
            size="lg"
            external
          >
            Join us
            <!-- Arrow icon -->
            <svg
              class="size-4"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              aria-hidden="true"
            >
              <path stroke-linecap="round" stroke-linejoin="round" d="M7 17L17 7M17 7H7M17 7v10" />
            </svg>
          </UiBaseButton>
        </div>

        <!-- Stats bar -->
        <div class="hero-item" style="animation-delay: 340ms">
          <!-- Divider -->
          <div class="mb-8 flex items-center gap-4">
            <div class="h-px flex-1 bg-[var(--color-border)]" />
            <div class="size-1 rounded-full bg-[var(--color-ieee-blue)]" aria-hidden="true" />
            <div class="h-px w-8 bg-[var(--color-border)]" />
          </div>

          <dl class="flex flex-wrap gap-x-10 gap-y-4">
            <div v-for="stat in stats" :key="stat.label" class="flex flex-col gap-0.5">
              <dt
                class="font-mono text-[11px] uppercase tracking-widest text-[var(--color-text-muted)]"
              >
                {{ stat.label }}
              </dt>
              <dd class="font-mono text-2xl font-bold text-[var(--color-text-primary)]">
                {{ stat.value }}
              </dd>
            </div>
          </dl>
        </div>
      </div>
    </div>

    <!-- Bottom fade -->
    <div
      class="pointer-events-none absolute bottom-0 left-0 right-0 h-24 bg-gradient-to-t from-[var(--color-surface)] to-transparent"
      aria-hidden="true"
    />
  </section>
</template>

<style scoped>
/* Dot grid — changes opacity in dark mode via CSS variable */
.hero-bg {
  background-image: radial-gradient(circle, rgba(0, 98, 155, 0.14) 1.5px, transparent 1.5px);
  background-size: 28px 28px;
}

:global(.dark) .hero-bg {
  background-image: radial-gradient(circle, rgba(0, 163, 224, 0.1) 1.5px, transparent 1.5px);
}

/* Staggered entrance animation */
@keyframes heroFadeUp {
  from {
    opacity: 0;
    transform: translateY(14px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hero-item {
  animation: heroFadeUp 0.55s ease both;
}
</style>
