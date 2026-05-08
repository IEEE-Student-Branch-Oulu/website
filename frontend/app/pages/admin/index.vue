<script setup lang="ts">
definePageMeta({ middleware: 'admin' })
useHead({ title: 'Admin - IEEE SB Oulu' })
</script>

<template>
  <div class="mx-auto max-w-4xl px-4 py-16">
    <h1 class="mb-8 text-2xl font-bold text-[var(--color-text-primary)]">Admin Dashboard</h1>

    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <NuxtLink
        to="/admin/users"
        class="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-6 transition-shadow hover:shadow-md"
      >
        <h3 class="mb-1 font-semibold text-[var(--color-text-primary)]">Users</h3>
        <p class="text-sm text-[var(--color-text-secondary)]">
          Manage members, approve applications, change roles
        </p>
      </NuxtLink>

      <NuxtLink
        to="/admin/audit"
        class="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-6 transition-shadow hover:shadow-md"
      >
        <h3 class="mb-1 font-semibold text-[var(--color-text-primary)]">Audit Log</h3>
        <p class="text-sm text-[var(--color-text-secondary)]">View security-relevant actions</p>
      </NuxtLink>
    </div>
  </div>
</template>
