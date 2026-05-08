<script setup lang="ts">
definePageMeta({ middleware: 'active-member' })
useHead({ title: 'Member Directory - IEEE SB Oulu' })

const { api } = useApi()

interface DirectoryMember {
  id: number
  firstName: string
  lastName: string
  university: string
  studyLevel: string | null
  studyProgram: string | null
  bio: string | null
}

interface Page {
  items: DirectoryMember[]
  total: number
  limit: number
  offset: number
}

const members = ref<DirectoryMember[]>([])
const total = ref(0)
const loading = ref(true)

const studyLevelLabels: Record<string, string> = {
  bsc: "Bachelor's",
  msc: "Master's",
  phd: 'PhD',
  postdoc: 'Postdoc',
  other: 'Other',
}

async function loadMembers() {
  loading.value = true
  try {
    const data = await api<Page>('/members/', { query: { limit: 50, offset: 0 } })
    members.value = data.items
    total.value = data.total
  } catch {
    members.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => loadMembers())
</script>

<template>
  <div class="mx-auto max-w-4xl px-4 py-16">
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-[var(--color-text-primary)]">Member Directory</h1>
      <p class="mt-1 text-sm text-[var(--color-text-secondary)]">
        Members who have opted in to be listed publicly. {{ total }} member{{
          total !== 1 ? 's' : ''
        }}
        visible.
      </p>
    </div>

    <div v-if="loading" class="py-12 text-center text-[var(--color-text-tertiary)]">Loading...</div>

    <div v-else-if="members.length === 0" class="py-12 text-center">
      <p class="text-[var(--color-text-tertiary)]">
        No members have opted in to the directory yet.
      </p>
      <p class="mt-2 text-sm text-[var(--color-text-tertiary)]">
        You can make your profile visible in
        <NuxtLink to="/members/profile" class="text-[var(--color-ieee-blue)] hover:underline"
          >Profile Settings</NuxtLink
        >.
      </p>
    </div>

    <div v-else class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="m in members"
        :key="m.id"
        class="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-5"
      >
        <h3 class="font-medium text-[var(--color-text-primary)]">
          {{ m.firstName }} {{ m.lastName }}
        </h3>
        <p class="mt-1 text-sm text-[var(--color-text-secondary)]">{{ m.university }}</p>
        <div v-if="m.studyLevel || m.studyProgram" class="mt-2 flex flex-wrap gap-2">
          <UiBaseBadge v-if="m.studyLevel" variant="blue">
            {{ studyLevelLabels[m.studyLevel] ?? m.studyLevel }}
          </UiBaseBadge>
          <span v-if="m.studyProgram" class="text-xs text-[var(--color-text-tertiary)]">
            {{ m.studyProgram }}
          </span>
        </div>
        <p v-if="m.bio" class="mt-3 line-clamp-3 text-sm text-[var(--color-text-secondary)]">
          {{ m.bio }}
        </p>
      </div>
    </div>
  </div>
</template>
