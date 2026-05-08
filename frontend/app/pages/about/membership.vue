<script setup lang="ts">
useHead({ title: 'Membership - IEEE SB Oulu' })
</script>

<template>
  <div class="mx-auto max-w-3xl px-4 py-16">
    <h1 class="mb-6 text-3xl font-bold text-[var(--color-text-primary)]">Become a Member</h1>

    <div
      class="prose prose-sm dark:prose-invert max-w-none space-y-6 text-[var(--color-text-secondary)]"
    >
      <p class="text-lg">
        IEEE Student Branch Oulu is a community of engineering and technology students at the
        University of Oulu. Joining us connects you with a global network of 400,000+ IEEE members.
      </p>

      <h2 class="text-[var(--color-text-primary)]">How to join</h2>

      <div class="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-6">
        <ol class="list-decimal space-y-4 pl-5">
          <li>
            <strong class="text-[var(--color-text-primary)]">Become an IEEE member first</strong>
            <p>
              All student branch members must hold an active IEEE membership. Student membership
              costs around $14/year.
            </p>
            <UiBaseButton
              href="https://www.ieee.org/membership/students/"
              variant="secondary"
              size="sm"
              external
              class="mt-2"
            >
              Join IEEE
            </UiBaseButton>
          </li>
          <li>
            <strong class="text-[var(--color-text-primary)]">Register on our website</strong>
            <p>
              Fill out the membership form with your IEEE number. You'll receive an email
              verification link.
            </p>
          </li>
          <li>
            <strong class="text-[var(--color-text-primary)]">Board approval</strong>
            <p>
              The board reviews applications, typically at the next board meeting. You'll be
              notified by email.
            </p>
          </li>
        </ol>
      </div>

      <h2 class="text-[var(--color-text-primary)]">Annual renewal</h2>
      <p>
        Memberships follow the academic year (September to August). At the start of each year,
        active members can renew with a single click — no need to re-enter your information. The
        board approves renewals at their first meeting of the year.
      </p>

      <h2 class="text-[var(--color-text-primary)]">What you get</h2>
      <ul class="list-disc space-y-1 pl-5">
        <li>Access to workshops, hackathons, and social events</li>
        <li>Member directory to connect with peers</li>
        <li>Networking with IEEE professionals and industry partners</li>
        <li>Discounts on IEEE conferences and publications</li>
        <li>Leadership and volunteering opportunities</li>
      </ul>

      <h2 class="text-[var(--color-text-primary)]">FAQ</h2>

      <details class="rounded-lg border border-[var(--color-border)] p-4">
        <summary class="cursor-pointer font-medium text-[var(--color-text-primary)]">
          Do I need to pay to join the student branch?
        </summary>
        <p class="mt-2">
          The student branch itself is free. However, you need an active IEEE membership ($14/year
          for students).
        </p>
      </details>

      <details class="rounded-lg border border-[var(--color-border)] p-4">
        <summary class="cursor-pointer font-medium text-[var(--color-text-primary)]">
          Can non-University of Oulu students join?
        </summary>
        <p class="mt-2">
          Our branch primarily serves University of Oulu students, but others in the region are
          welcome to apply.
        </p>
      </details>

      <details class="rounded-lg border border-[var(--color-border)] p-4">
        <summary class="cursor-pointer font-medium text-[var(--color-text-primary)]">
          How long does approval take?
        </summary>
        <p class="mt-2">
          The board meets regularly throughout the academic year. Most applications are reviewed
          within 1-2 weeks.
        </p>
      </details>
    </div>

    <div class="mt-8">
      <UiBaseButton href="/auth/register" variant="primary" size="lg"
        >Apply for Membership</UiBaseButton
      >
    </div>
  </div>
</template>
