<script setup lang="ts">
import { useBlogApi, type BlogPostInput } from '~/composables/useBlog'
import type { ApiError } from '~/composables/useApi'

definePageMeta({ middleware: 'admin' })

const route = useRoute()
const id = Number(route.params.id)

const { getRaw, update } = useBlogApi()
const { data: post, error: loadError } = await useAsyncData(`admin-post-${id}`, () => getRaw(id))

if (loadError.value || !post.value) {
  throw createError({ statusCode: 404, statusMessage: 'Post not found' })
}

useHead({ title: `Edit: ${post.value.title} - IEEE SB Oulu` })

const submitting = ref(false)
const error = ref<string | null>(null)

async function onSubmit(payload: BlogPostInput) {
  submitting.value = true
  error.value = null
  try {
    const updated = await update(id, payload)
    await navigateTo(`/blog/${updated.slug}`)
  } catch (e) {
    error.value = (e as ApiError)?.detail ?? 'Failed to update post.'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="mx-auto max-w-4xl px-4 py-16">
    <h1 class="mb-8 text-2xl font-bold text-[var(--color-text-primary)]">Edit post</h1>
    <AdminPostForm :initial="post" :submitting="submitting" :error="error" @submit="onSubmit" />
  </div>
</template>
