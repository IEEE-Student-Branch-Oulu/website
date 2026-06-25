<script setup lang="ts">
import { useBlogApi } from '~/composables/useBlog'

definePageMeta({ middleware: 'admin' })
useHead({ title: 'Manage News - IEEE SB Oulu' })

const { list, remove } = useBlogApi()
const { data, refresh } = await useAsyncData('admin-posts', () => list())
const posts = computed(() => data.value?.items ?? [])

const deleting = ref<number | null>(null)

async function onDelete(id: number, title: string) {
  if (!globalThis.confirm(`Delete "${title}"? This cannot be undone.`)) return
  deleting.value = id
  try {
    await remove(id)
    await refresh()
  } finally {
    deleting.value = null
  }
}
</script>

<template>
  <div class="mx-auto max-w-4xl px-4 py-16">
    <div class="mb-8 flex items-center justify-between">
      <h1 class="text-2xl font-bold text-[var(--color-text-primary)]">News & Infodumps</h1>
      <UiBaseButton href="/admin/news/new" variant="primary" size="sm">New post</UiBaseButton>
    </div>

    <p v-if="!posts.length" class="text-sm text-[var(--color-text-secondary)]">
      No posts yet. Create your first one.
    </p>

    <ul v-else class="flex flex-col gap-3">
      <li
        v-for="post in posts"
        :key="post.id"
        class="flex items-center justify-between gap-4 rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-4"
      >
        <div class="min-w-0">
          <p class="truncate font-medium text-[var(--color-text-primary)]">{{ post.title }}</p>
          <p class="text-xs text-[var(--color-text-muted)]">
            {{ post.date }} · {{ post.category }}
          </p>
        </div>
        <div class="flex flex-shrink-0 gap-2">
          <UiBaseButton :href="`/blog/${post.slug}`" variant="ghost" size="sm">View</UiBaseButton>
          <UiBaseButton :href="`/admin/news/${post.id}`" variant="secondary" size="sm">
            Edit
          </UiBaseButton>
          <UiBaseButton
            variant="danger"
            size="sm"
            :loading="deleting === post.id"
            @click="onDelete(post.id, post.title)"
          >
            Delete
          </UiBaseButton>
        </div>
      </li>
    </ul>
  </div>
</template>
