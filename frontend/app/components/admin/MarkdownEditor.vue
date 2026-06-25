<script setup lang="ts">
/**
 * MarkdownEditor
 *
 * Thin wrapper around md-editor-v3 used by the admin authoring forms.
 * Stores markdown (the backend renders it to HTML on read). The image
 * toolbar button uploads via POST /admin/uploads and inserts the URL.
 *
 * Render client-only — the editor touches browser APIs. Wrap usages in
 * <ClientOnly> or rely on this component's own guard.
 */
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'

const model = defineModel<string>({ required: true })

const { isDark } = useColorMode()
const { api } = useApi()

const theme = computed(() => (isDark.value ? 'dark' : 'light'))

interface UploadResponse {
  url: string
}

async function onUploadImg(files: File[], callback: (urls: string[]) => void): Promise<void> {
  const urls = await Promise.all(
    files.map(async (file) => {
      const form = new FormData()
      form.append('file', file)
      const res = await api<UploadResponse>('/admin/uploads', {
        method: 'POST',
        body: form,
      })
      return res.url
    })
  )
  callback(urls)
}
</script>

<template>
  <ClientOnly>
    <MdEditor
      v-model="model"
      :theme="theme"
      language="en-US"
      :preview="false"
      :toolbars-exclude="['save', 'github', 'catalog']"
      @on-upload-img="onUploadImg"
    />
    <template #fallback>
      <div
        class="flex h-64 items-center justify-center rounded-lg border border-[var(--color-border)] text-sm text-[var(--color-text-muted)]"
      >
        Loading editor…
      </div>
    </template>
  </ClientOnly>
</template>
