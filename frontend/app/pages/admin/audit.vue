<script setup lang="ts">
definePageMeta({ middleware: 'admin' })
useHead({ title: 'Audit Log - Admin - IEEE SB Oulu' })

const { api } = useApi()
const toast = useToast()

interface AuditEntry {
  id: number
  actorUserId: number | null
  action: string
  targetUserId: number | null
  metadata: Record<string, unknown>
  ip: string | null
  createdAt: string
}

interface Page {
  items: AuditEntry[]
  total: number
}

const entries = ref<AuditEntry[]>([])
const total = ref(0)
const loading = ref(true)

async function load() {
  loading.value = true
  try {
    const data = await api<Page>('/admin/audit', { query: { limit: 50, offset: 0 } })
    entries.value = data.items
    total.value = data.total
  } catch {
    toast.error('Failed to load audit log.')
  } finally {
    loading.value = false
  }
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleString()
}

onMounted(() => load())
</script>

<template>
  <div class="mx-auto max-w-5xl px-4 py-16">
    <div class="mb-6 flex items-center justify-between">
      <h1 class="text-2xl font-bold text-[var(--color-text-primary)]">Audit Log ({{ total }})</h1>
      <NuxtLink to="/admin" class="text-sm text-[var(--color-ieee-blue)] hover:underline"
        >Back</NuxtLink
      >
    </div>

    <div v-if="loading" class="py-8 text-center text-[var(--color-text-tertiary)]">Loading...</div>

    <div v-else class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr
            class="border-b border-[var(--color-border)] text-left text-[var(--color-text-tertiary)]"
          >
            <th class="pb-2 pr-4 font-medium">Time</th>
            <th class="pb-2 pr-4 font-medium">Action</th>
            <th class="pb-2 pr-4 font-medium">Actor</th>
            <th class="pb-2 pr-4 font-medium">Target</th>
            <th class="pb-2 font-medium">IP</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="entry in entries"
            :key="entry.id"
            class="border-b border-[var(--color-border)] last:border-0"
          >
            <td class="py-3 pr-4 text-[var(--color-text-secondary)]">
              {{ formatDate(entry.createdAt) }}
            </td>
            <td class="py-3 pr-4">
              <UiBaseBadge variant="default">{{ entry.action }}</UiBaseBadge>
            </td>
            <td class="py-3 pr-4 text-[var(--color-text-secondary)]">
              {{ entry.actorUserId ?? '-' }}
            </td>
            <td class="py-3 pr-4 text-[var(--color-text-secondary)]">
              {{ entry.targetUserId ?? '-' }}
            </td>
            <td class="py-3 text-[var(--color-text-tertiary)]">{{ entry.ip ?? '-' }}</td>
          </tr>
        </tbody>
      </table>

      <p v-if="entries.length === 0" class="py-8 text-center text-[var(--color-text-tertiary)]">
        No audit entries yet.
      </p>
    </div>
  </div>
</template>
