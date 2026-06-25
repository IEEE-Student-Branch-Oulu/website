<script setup lang="ts">
/**
 * Membership ( /about/membership )
 *
 * CTA-first layout: the "Apply" and "Log in" actions live in the hero so
 * nobody has to read or scroll to find them. Instructions, perks and FAQ
 * follow below for those who want the detail.
 */

useHead({ title: 'Membership - IEEE SB Oulu' })

const { isAuthenticated } = useAuth()

const steps = [
  {
    title: 'Become an IEEE member',
    body: 'Student branch members hold an active IEEE membership — about $14/year for students.',
    link: { label: 'Join IEEE', href: 'https://www.ieee.org/membership/students/' },
  },
  {
    title: 'Register here',
    body: "Fill in the short form with your IEEE number. We'll email you a verification link.",
  },
  {
    title: 'Get approved',
    body: 'The board reviews new members at its next meeting, usually within a week or two.',
  },
]

const perks = [
  'Workshops, hackathons and socials',
  'A member directory to find your people',
  'Networking with IEEE pros and industry',
  'Discounts on IEEE conferences & journals',
  'Room to lead, volunteer and build things',
  'A global network of 400,000+ engineers',
]

const faqs = [
  {
    q: 'Do I have to pay to join the student branch?',
    a: 'The branch itself is free. You just need an active IEEE membership ($14/year for students).',
  },
  {
    q: "Can I join if I'm not at the University of Oulu?",
    a: 'We mainly serve University of Oulu students, but others in the region are welcome to apply.',
  },
  {
    q: 'How long does approval take?',
    a: 'The board meets regularly through the year — most applications are reviewed within 1–2 weeks.',
  },
]
</script>

<template>
  <div>
    <!-- ── Hero: CTA above the fold ─────────────────────────────── -->
    <section class="relative overflow-hidden border-b border-[var(--color-border)]">
      <!-- Dot grid + glow, matching the home hero -->
      <div class="membership-bg pointer-events-none absolute inset-0" aria-hidden="true" />
      <div
        class="bg-[var(--color-ieee-blue)]/5 dark:bg-[var(--color-ieee-blue)]/8 pointer-events-none absolute -right-40 -top-40 h-[600px] w-[600px] rounded-full blur-3xl"
        aria-hidden="true"
      />

      <div class="relative mx-auto max-w-5xl px-4 py-20 text-center sm:px-6 sm:py-28 lg:px-8">
        <p
          class="mb-5 inline-flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.18em] text-[var(--color-ieee-blue)]"
        >
          <span class="size-1.5 animate-pulse rounded-full bg-[var(--color-ieee-blue)]" />
          Membership · Open now
        </p>

        <h1
          class="mx-auto mb-5 max-w-2xl text-4xl font-bold leading-[1.05] tracking-tight sm:text-5xl lg:text-6xl"
        >
          Join IEEE Oulu
        </h1>

        <p
          class="mx-auto mb-10 max-w-xl text-lg leading-relaxed text-[var(--color-text-secondary)]"
        >
          One global network, one local community — and a membership that takes about five minutes
          to start. Here's how it works.
        </p>

        <!-- Primary actions -->
        <div class="flex flex-col items-center justify-center gap-3 sm:flex-row">
          <UiBaseButton to="/auth/register" variant="primary" size="lg">
            Apply for Membership
            <svg
              class="size-4"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              aria-hidden="true"
            >
              <path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M12 5l7 7-7 7" />
            </svg>
          </UiBaseButton>

          <UiBaseButton v-if="!isAuthenticated" to="/auth/login" variant="ghost" size="lg">
            Already a member? Log in
          </UiBaseButton>
          <UiBaseButton v-else to="/members" variant="ghost" size="lg">
            Go to my dashboard
          </UiBaseButton>
        </div>

        <p class="mt-5 text-xs text-[var(--color-text-muted)]">
          Free to join the branch · requires an IEEE membership (~$14/year for students)
        </p>
      </div>
    </section>

    <!-- ── How it works ─────────────────────────────────────────── -->
    <section class="mx-auto max-w-5xl px-4 py-16 sm:px-6 lg:px-8">
      <UiSectionHeader
        eyebrow="Three steps"
        title="How to join"
        subtitle="No long forms, no waiting around. Here's the whole process."
        class="mb-10"
      />

      <ol class="grid grid-cols-1 gap-5 sm:grid-cols-3">
        <li
          v-for="(step, i) in steps"
          :key="step.title"
          class="relative rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-6"
        >
          <span
            class="bg-[var(--color-ieee-blue)]/10 mb-4 flex size-9 items-center justify-center rounded-lg font-mono text-sm font-bold text-[var(--color-ieee-blue)]"
          >
            {{ i + 1 }}
          </span>
          <h3 class="mb-2 font-semibold text-[var(--color-text-primary)]">{{ step.title }}</h3>
          <p class="text-sm leading-relaxed text-[var(--color-text-secondary)]">{{ step.body }}</p>
          <UiBaseLink
            v-if="step.link"
            :href="step.link.href"
            external
            class="mt-3 inline-flex items-center gap-1.5 text-xs font-medium text-[var(--color-ieee-blue)] hover:text-[var(--color-ieee-blue-light)] focus-visible:underline focus-visible:outline-none"
          >
            {{ step.link.label }}
            <svg
              class="size-3.5"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              aria-hidden="true"
            >
              <path stroke-linecap="round" stroke-linejoin="round" d="M7 17L17 7M17 7H7M17 7v10" />
            </svg>
          </UiBaseLink>
        </li>
      </ol>
    </section>

    <!-- ── Perks + renewal ──────────────────────────────────────── -->
    <section class="border-y border-[var(--color-border)] bg-[var(--color-surface-raised)]">
      <div
        class="mx-auto grid max-w-5xl grid-cols-1 gap-10 px-4 py-16 sm:px-6 lg:grid-cols-2 lg:gap-16 lg:px-8"
      >
        <div>
          <h2 class="mb-5 text-2xl font-bold text-[var(--color-text-primary)]">What you get</h2>
          <ul class="flex flex-col gap-3">
            <li
              v-for="perk in perks"
              :key="perk"
              class="flex items-start gap-3 text-sm text-[var(--color-text-secondary)]"
            >
              <svg
                class="mt-0.5 size-4 flex-shrink-0 text-[var(--color-ieee-blue)]"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2.5"
                aria-hidden="true"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M20 6L9 17l-5-5" />
              </svg>
              {{ perk }}
            </li>
          </ul>
        </div>

        <div class="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-6">
          <h2 class="mb-3 text-lg font-bold text-[var(--color-text-primary)]">
            Renewing each year
          </h2>
          <p class="text-sm leading-relaxed text-[var(--color-text-secondary)]">
            Membership runs with the academic year, September to August. When a new year starts, you
            can renew from your dashboard in one click — we already have your details, so there's
            nothing to fill in again. The board signs off renewals at its first meeting of the year.
          </p>
        </div>
      </div>
    </section>

    <!-- ── FAQ ──────────────────────────────────────────────────── -->
    <section class="mx-auto max-w-3xl px-4 py-16 sm:px-6 lg:px-8">
      <h2 class="mb-6 text-2xl font-bold text-[var(--color-text-primary)]">Common questions</h2>
      <div class="flex flex-col gap-3">
        <details
          v-for="faq in faqs"
          :key="faq.q"
          class="group rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] p-4"
        >
          <summary
            class="flex cursor-pointer items-center justify-between gap-4 font-medium text-[var(--color-text-primary)]"
          >
            {{ faq.q }}
            <svg
              class="size-4 flex-shrink-0 text-[var(--color-text-muted)] transition-transform duration-200 group-open:rotate-180"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              aria-hidden="true"
            >
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 9l6 6 6-6" />
            </svg>
          </summary>
          <p class="mt-3 text-sm leading-relaxed text-[var(--color-text-secondary)]">{{ faq.a }}</p>
        </details>
      </div>

      <!-- Closing CTA -->
      <div
        class="mt-12 flex flex-col items-center gap-4 rounded-2xl border border-[var(--color-border)] bg-[var(--color-surface-raised)] p-8 text-center"
      >
        <p class="text-lg font-semibold text-[var(--color-text-primary)]">Ready to join?</p>
        <UiBaseButton to="/auth/register" variant="primary" size="lg">
          Apply for Membership
        </UiBaseButton>
      </div>
    </section>
  </div>
</template>

<style scoped>
.membership-bg {
  background-image: radial-gradient(circle, rgba(0, 98, 155, 0.12) 1.5px, transparent 1.5px);
  background-size: 28px 28px;
}

:global(.dark) .membership-bg {
  background-image: radial-gradient(circle, rgba(0, 163, 224, 0.09) 1.5px, transparent 1.5px);
}
</style>
