<script setup lang="ts">
definePageMeta({ middleware: 'auth' })
useHead({ title: 'Dashboard - IEEE SB Oulu' })

const { user, fetchMe, logout } = useAuth()
const { api } = useApi()
const toast = useToast()

await callOnce(fetchMe)

const renewLoading = ref(false)

async function renewMembership() {
  renewLoading.value = true
  try {
    await api('/members/me/renew', { method: 'POST' })
    toast.success('Renewal submitted for board review.')
    await fetchMe()
  } catch (e: unknown) {
    const err = e as { detail?: string }
    toast.error(err?.detail ?? 'Renewal failed.')
  } finally {
    renewLoading.value = false
  }
}

async function exportData() {
  try {
    const data = await api<Record<string, unknown>>('/members/me/export')
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'ieee-sb-oulu-export.json'
    a.click()
    URL.revokeObjectURL(url)
    toast.success('Data exported.')
  } catch {
    toast.error('Export failed.')
  }
}

async function deleteAccount() {
  if (!confirm('Are you sure you want to delete your account? This cannot be undone.')) return
  try {
    await api('/members/me', { method: 'DELETE' })
    toast.success('Account deleted.')
    await navigateTo('/')
  } catch {
    toast.error('Deletion failed.')
  }
}

async function doLogout() {
  await logout()
  await navigateTo('/')
}
</script>

<template>
  <div class="mx-auto max-w-2xl px-4 py-16">
    <div class="mb-8 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-[var(--color-text-primary)]">
          Welcome, {{ user?.firstName }}
        </h1>
        <p class="text-sm text-[var(--color-text-secondary)]">{{ user?.email }}</p>
      </div>
      <UiBaseButton variant="ghost" size="sm" @click="doLogout">Log out</UiBaseButton>
    </div>

    <AuthStatusTracker v-if="user" :status="user.status" class="mb-8" />

    <!-- Membership periods -->
    <div
      v-if="user?.membershipPeriods?.length"
      class="mb-8 rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-6"
    >
      <h3 class="mb-4 text-lg font-semibold text-[var(--color-text-primary)]">
        Membership History
      </h3>
      <div class="space-y-3">
        <div
          v-for="period in user.membershipPeriods"
          :key="period.id"
          class="flex items-center justify-between rounded-lg border border-[var(--color-border)] px-4 py-3"
        >
          <div>
            <span class="font-medium text-[var(--color-text-primary)]">
              {{ period.periodYear }}-{{ period.periodYear + 1 }}
            </span>
            <span class="ml-2 text-xs text-[var(--color-text-tertiary)]">
              IEEE #{{ period.ieeeMembershipNumber }}
            </span>
          </div>
          <UiBaseBadge
            :variant="
              period.status === 'approved'
                ? 'green'
                : period.status === 'rejected'
                  ? 'red'
                  : 'orange'
            "
          >
            {{ period.status }}
          </UiBaseBadge>
        </div>
      </div>

      <UiBaseButton
        v-if="user.status === 'active'"
        variant="secondary"
        size="sm"
        class="mt-4"
        :loading="renewLoading"
        @click="renewMembership"
      >
        Renew for current year
      </UiBaseButton>
    </div>

    <!-- Profile link -->
    <div class="mb-8 rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-6">
      <h3 class="mb-2 text-lg font-semibold text-[var(--color-text-primary)]">Profile</h3>
      <p class="mb-4 text-sm text-[var(--color-text-secondary)]">
        Update your personal information and visibility settings.
      </p>
      <div class="flex gap-3">
        <UiBaseButton href="/members/profile" variant="secondary" size="sm"
          >Edit Profile</UiBaseButton
        >
        <UiBaseButton href="/members/directory" variant="ghost" size="sm"
          >Member Directory</UiBaseButton
        >
      </div>
    </div>

    <!-- GDPR section -->
    <div class="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-6">
      <h3 class="mb-2 text-lg font-semibold text-[var(--color-text-primary)]">Your Data</h3>
      <p class="mb-4 text-sm text-[var(--color-text-secondary)]">
        Export or delete your data in accordance with GDPR.
      </p>
      <div class="flex gap-3">
        <UiBaseButton variant="secondary" size="sm" @click="exportData">Export Data</UiBaseButton>
        <UiBaseButton variant="danger" size="sm" @click="deleteAccount"
          >Delete Account</UiBaseButton
        >
      </div>
    </div>
  </div>
</template>
