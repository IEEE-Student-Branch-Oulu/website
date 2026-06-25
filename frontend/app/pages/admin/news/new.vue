<script setup lang="ts">
import { useBlogApi, type BlogPostInput } from '~/composables/useBlog'
import type { ApiError } from '~/composables/useApi'

definePageMeta({ middleware: 'admin' })
useHead({ title: 'New post - IEEE SB Oulu' })

const { create } = useBlogApi()
const submitting = ref(false)
const error = ref<string | null>(null)

async function onSubmit(payload: BlogPostInput) {
  submitting.value = true
  error.value = null
  try {
    const post = await create(payload)
    await navigateTo(`/blog/${post.slug}`)
  } catch (e) {
    error.value = (e as ApiError)?.detail ?? 'Failed to create post.'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="mx-auto max-w-4xl px-4 py-16">
    <h1 class="mb-8 text-2xl font-bold text-[var(--color-text-primary)]">New post</h1>
    <AdminPostForm :submitting="submitting" :error="error" @submit="onSubmit" />
  </div>
</template>
