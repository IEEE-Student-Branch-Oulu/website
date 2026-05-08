<script setup lang="ts">
useHead({ title: 'Privacy Policy - IEEE SB Oulu' })
</script>

<template>
  <div class="mx-auto max-w-3xl px-4 py-16">
    <div
      class="mb-4 rounded-lg border border-yellow-300 bg-yellow-50 p-3 text-sm text-yellow-800 dark:border-yellow-700 dark:bg-yellow-950 dark:text-yellow-200"
    >
      Draft v1.0 — The board will finalize this document. Last updated: May 2026.
    </div>

    <h1 class="mb-6 text-3xl font-bold text-[var(--color-text-primary)]">Privacy Policy</h1>

    <div
      class="prose prose-sm dark:prose-invert max-w-none space-y-4 text-[var(--color-text-secondary)]"
    >
      <p>Version 1.0</p>

      <h2 class="text-[var(--color-text-primary)]">What we collect</h2>
      <p>
        When you register, we collect: name, email, IEEE membership number, university, study
        details, and consent records.
      </p>

      <h2 class="text-[var(--color-text-primary)]">How we use it</h2>
      <p>
        Your data is used solely for managing student branch membership, communicating with members,
        and running events.
      </p>

      <h2 class="text-[var(--color-text-primary)]">Data storage</h2>
      <p>
        Data is stored on servers within the EU. Passwords are hashed with argon2id. Session tokens
        are hashed with SHA-256.
      </p>

      <h2 class="text-[var(--color-text-primary)]">Your rights (GDPR)</h2>
      <ul class="list-disc space-y-1 pl-5">
        <li><strong>Access:</strong> Export all your data from your dashboard.</li>
        <li><strong>Rectification:</strong> Edit your profile at any time.</li>
        <li>
          <strong>Erasure:</strong> Delete your account from your dashboard. Your data will be
          anonymized.
        </li>
        <li><strong>Portability:</strong> Export your data as JSON.</li>
      </ul>

      <h2 class="text-[var(--color-text-primary)]">Contact</h2>
      <p>For privacy questions, contact the student branch board.</p>
    </div>
  </div>
</template>
