<script setup lang="ts">
definePageMeta({ middleware: 'admin' })
useHead({ title: 'Users - Admin - IEEE SB Oulu' })

const { api } = useApi()
const toast = useToast()

interface AdminUser {
  id: number
  email: string
  firstName: string
  lastName: string
  role: string
  status: string
  ieeeMembershipNumber: string
  createdAt: string
}

interface Page {
  items: AdminUser[]
  total: number
  limit: number
  offset: number
}

const filter = ref<string>('')
const users = ref<AdminUser[]>([])
const total = ref(0)
const loading = ref(true)

async function loadUsers() {
  loading.value = true
  try {
    const query: Record<string, string | number> = { limit: 50, offset: 0 }
    if (filter.value) query.status = filter.value
    const data = await api<Page>('/admin/users', { query })
    users.value = data.items
    total.value = data.total
  } catch {
    toast.error('Failed to load users.')
  } finally {
    loading.value = false
  }
}

async function approveUser(id: number) {
  try {
    await api(`/admin/users/${id}/approve`, { method: 'POST' })
    toast.success('User approved.')
    await loadUsers()
  } catch (e: unknown) {
    const err = e as { detail?: string }
    toast.error(err?.detail ?? 'Action failed.')
  }
}

async function rejectUser(id: number) {
  const reason = prompt('Rejection reason (optional):')
  try {
    await api(`/admin/users/${id}/reject`, { method: 'POST', body: { reason } })
    toast.success('User rejected.')
    await loadUsers()
  } catch (e: unknown) {
    const err = e as { detail?: string }
    toast.error(err?.detail ?? 'Action failed.')
  }
}

async function changeRole(id: number, newRole: string) {
  try {
    await api(`/admin/users/${id}/role`, { method: 'POST', body: { role: newRole } })
    toast.success('Role updated.')
    await loadUsers()
  } catch (e: unknown) {
    const err = e as { detail?: string }
    toast.error(err?.detail ?? 'Action failed.')
  }
}

async function suspendUser(id: number) {
  if (!confirm('Suspend this user? Their sessions will be revoked.')) return
  try {
    await api(`/admin/users/${id}/suspend`, { method: 'POST' })
    toast.success('User suspended.')
    await loadUsers()
  } catch (e: unknown) {
    const err = e as { detail?: string }
    toast.error(err?.detail ?? 'Action failed.')
  }
}

async function restoreUser(id: number) {
  try {
    await api(`/admin/users/${id}/restore`, { method: 'POST' })
    toast.success('User restored.')
    await loadUsers()
  } catch (e: unknown) {
    const err = e as { detail?: string }
    toast.error(err?.detail ?? 'Action failed.')
  }
}

async function exportUsers() {
  try {
    const query: Record<string, string> = {}
    if (filter.value) query.status = filter.value
    const config = useRuntimeConfig()
    const baseURL = config.public.apiBase as string
    const res = await $fetch.raw(`${baseURL}/admin/users/export`, {
      credentials: 'include',
      query,
    })
    const blob = new Blob([res._data as string], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download =
      res.headers.get('content-disposition')?.match(/filename="(.+)"/)?.[1] ?? 'members-export.csv'
    a.click()
    URL.revokeObjectURL(url)
    toast.success('Export downloaded.')
  } catch {
    toast.error('Export failed.')
  }
}

watch(filter, () => loadUsers())
onMounted(() => loadUsers())

const statusFilters = [
  { label: 'All', value: '' },
  { label: 'Pending', value: 'pending_approval' },
  { label: 'Active', value: 'active' },
  { label: 'Suspended', value: 'suspended' },
  { label: 'Rejected', value: 'rejected' },
]
</script>

<template>
  <div class="mx-auto max-w-5xl px-4 py-16">
    <div class="mb-6 flex items-center justify-between">
      <h1 class="text-2xl font-bold text-[var(--color-text-primary)]">Users ({{ total }})</h1>
      <div class="flex items-center gap-3">
        <UiBaseButton size="sm" variant="secondary" @click="exportUsers">Export CSV</UiBaseButton>
        <NuxtLink to="/admin" class="text-sm text-[var(--color-ieee-blue)] hover:underline"
          >Back</NuxtLink
        >
      </div>
    </div>

    <div class="mb-4 flex gap-2">
      <button
        v-for="f in statusFilters"
        :key="f.value"
        class="rounded-lg px-3 py-1.5 text-sm transition-colors"
        :class="
          filter === f.value
            ? 'bg-[var(--color-ieee-blue)] text-white'
            : 'bg-[var(--color-surface-overlay)] text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)]'
        "
        @click="filter = f.value"
      >
        {{ f.label }}
      </button>
    </div>

    <div v-if="loading" class="py-8 text-center text-[var(--color-text-tertiary)]">Loading...</div>

    <div v-else class="space-y-3">
      <div
        v-for="u in users"
        :key="u.id"
        class="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-4"
      >
        <div class="min-w-0">
          <p class="font-medium text-[var(--color-text-primary)]">
            {{ u.firstName }} {{ u.lastName }}
          </p>
          <p class="text-sm text-[var(--color-text-secondary)]">{{ u.email }}</p>
          <div class="mt-1 flex gap-2">
            <UiBaseBadge
              :variant="
                u.status === 'active' ? 'green' : u.status === 'suspended' ? 'red' : 'orange'
              "
            >
              {{ u.status }}
            </UiBaseBadge>
            <UiBaseBadge v-if="u.role === 'admin'" variant="blue">admin</UiBaseBadge>
          </div>
        </div>

        <div class="flex flex-wrap gap-2">
          <template v-if="u.status === 'pending_approval'">
            <UiBaseButton size="sm" variant="primary" @click="approveUser(u.id)"
              >Approve</UiBaseButton
            >
            <UiBaseButton size="sm" variant="danger" @click="rejectUser(u.id)">Reject</UiBaseButton>
          </template>
          <template v-if="u.status === 'active'">
            <UiBaseButton
              size="sm"
              variant="ghost"
              @click="changeRole(u.id, u.role === 'admin' ? 'member' : 'admin')"
            >
              {{ u.role === 'admin' ? 'Demote' : 'Promote' }}
            </UiBaseButton>
            <UiBaseButton size="sm" variant="danger" @click="suspendUser(u.id)"
              >Suspend</UiBaseButton
            >
          </template>
          <template v-if="u.status === 'suspended'">
            <UiBaseButton size="sm" variant="secondary" @click="restoreUser(u.id)"
              >Restore</UiBaseButton
            >
          </template>
        </div>
      </div>

      <p v-if="users.length === 0" class="py-8 text-center text-[var(--color-text-tertiary)]">
        No users match this filter.
      </p>
    </div>
  </div>
</template>
