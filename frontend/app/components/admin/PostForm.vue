<script setup lang="ts">
/**
 * PostForm
 *
 * Shared create/edit form for blog posts (and event recaps). Emits a
 * BlogPostInput payload on submit; the parent page handles the API call.
 */
import {
  CATEGORY_META,
  type BlogPostEdit,
  type BlogPostInput,
  type PostCategory,
} from '~/composables/useBlog'

const props = defineProps<{
  initial?: BlogPostEdit | null
  submitting?: boolean
  error?: string | null
}>()

const emit = defineEmits<{ submit: [value: BlogPostInput] }>()

const title = ref(props.initial?.title ?? '')
const excerpt = ref(props.initial?.excerpt ?? '')
const bodyMd = ref(props.initial?.bodyMd ?? '')
const category = ref<PostCategory>(props.initial?.category ?? 'branch-news')
const tagsText = ref((props.initial?.tags ?? []).join(', '))
const featured = ref(props.initial?.featured ?? false)
const coverImageUrl = ref<string | null>(props.initial?.coverImageUrl ?? null)
const eventSlug = ref(props.initial?.eventSlug ?? '')
const publishedOn = ref(props.initial?.publishedOn ?? '')

const categoryOptions = Object.entries(CATEGORY_META).map(([value, meta]) => ({
  value,
  label: meta.label,
}))

function onSubmit() {
  emit('submit', {
    title: title.value.trim(),
    excerpt: excerpt.value.trim(),
    bodyMd: bodyMd.value,
    category: category.value,
    tags: tagsText.value
      .split(',')
      .map((t) => t.trim())
      .filter(Boolean),
    featured: featured.value,
    coverImageUrl: coverImageUrl.value?.trim() || null,
    eventSlug: eventSlug.value.trim() || null,
    publishedOn: publishedOn.value || null,
  })
}
</script>

<template>
  <form class="flex flex-col gap-6" @submit.prevent="onSubmit">
    <UiFormField v-slot="{ id, hasError }" label="Title" required>
      <UiInputField :id="id" v-model="title" :has-error="hasError" placeholder="Post title" />
    </UiFormField>

    <div class="grid gap-6 sm:grid-cols-2">
      <UiFormField v-slot="{ id }" label="Category" required>
        <UiSelectField :id="id" v-model="category" :options="categoryOptions" />
      </UiFormField>

      <UiFormField v-slot="{ id }" label="Published on" hint="Defaults to today if left blank">
        <UiInputField :id="id" v-model="publishedOn" type="date" />
      </UiFormField>
    </div>

    <UiFormField v-slot="{ id, hasError }" label="Excerpt" required>
      <UiTextareaField
        :id="id"
        v-model="excerpt"
        :has-error="hasError"
        :rows="2"
        placeholder="Short summary shown on cards"
      />
    </UiFormField>

    <UiFormField label="Cover image" hint="16:9 — crop after selecting">
      <AdminImageUpload v-model="coverImageUrl" :aspect-ratio="16 / 9" />
    </UiFormField>

    <div class="grid gap-6 sm:grid-cols-2">
      <UiFormField v-slot="{ id }" label="Tags" hint="Comma-separated">
        <UiInputField :id="id" v-model="tagsText" placeholder="SDR, RF, Workshop" />
      </UiFormField>

      <UiFormField
        v-slot="{ id }"
        label="Linked event slug"
        hint="For event recaps — links back to the event"
      >
        <UiInputField :id="id" v-model="eventSlug" placeholder="gnu-radio-workshop" />
      </UiFormField>
    </div>

    <UiCheckboxField v-model="featured">
      <span class="text-sm text-[var(--color-text-primary)]">Feature this post (hero slot)</span>
    </UiCheckboxField>

    <div>
      <p class="mb-1 block text-sm font-medium text-[var(--color-text-primary)]">Body</p>
      <AdminMarkdownEditor v-model="bodyMd" />
    </div>

    <p v-if="error" class="text-sm text-red-500" role="alert">{{ error }}</p>

    <div class="flex gap-3">
      <UiBaseButton type="submit" variant="primary" :loading="submitting">
        {{ initial ? 'Save changes' : 'Publish post' }}
      </UiBaseButton>
      <UiBaseButton href="/admin/news" variant="ghost">Cancel</UiBaseButton>
    </div>
  </form>
</template>
