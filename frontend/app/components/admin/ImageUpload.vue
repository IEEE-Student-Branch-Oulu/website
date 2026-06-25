<script setup lang="ts">
/**
 * ImageUpload
 *
 * Cover-image picker with cropping + forced aspect ratio (vue-advanced-cropper).
 * Flow: pick file → crop to the required aspect ratio → upload the cropped
 * result to S3 via /admin/uploads → v-model receives the public URL.
 */
import { Cropper } from 'vue-advanced-cropper'
import 'vue-advanced-cropper/dist/style.css'

const model = defineModel<string | null>({ default: null })

withDefaults(
  defineProps<{
    /** Forced crop aspect ratio (width / height). */
    aspectRatio?: number
  }>(),
  { aspectRatio: 16 / 9 }
)

const { api } = useApi()

const fileInput = ref<HTMLInputElement | null>(null)
const cropperRef = ref<InstanceType<typeof Cropper> | null>(null)
const rawImage = ref<string | null>(null) // data URL of the file being cropped
const uploading = ref(false)
const error = ref<string | null>(null)

interface UploadResponse {
  url: string
}

function pick() {
  error.value = null
  fileInput.value?.click()
}

function onFileChange(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = () => {
    rawImage.value = reader.result as string
  }
  reader.readAsDataURL(file)
  // Allow re-picking the same file later.
  input.value = ''
}

function cancelCrop() {
  rawImage.value = null
}

function canvasToBlob(canvas: HTMLCanvasElement): Promise<Blob> {
  return new Promise((resolve, reject) => {
    canvas.toBlob(
      (blob) => (blob ? resolve(blob) : reject(new Error('Could not render image.'))),
      'image/jpeg',
      0.9
    )
  })
}

async function cropAndUpload() {
  if (!cropperRef.value) return
  const result = cropperRef.value.getResult()
  const canvas = result?.canvas
  if (!canvas) return

  uploading.value = true
  error.value = null
  try {
    const blob = await canvasToBlob(canvas)
    const form = new FormData()
    form.append('file', blob, 'cover.jpg')
    const res = await api<UploadResponse>('/admin/uploads', { method: 'POST', body: form })
    model.value = res.url
    rawImage.value = null
  } catch (e) {
    error.value = (e as { detail?: string })?.detail ?? 'Upload failed.'
  } finally {
    uploading.value = false
  }
}

function remove() {
  model.value = null
}
</script>

<template>
  <div class="flex flex-col gap-3">
    <input ref="fileInput" type="file" accept="image/*" class="hidden" @change="onFileChange" />

    <!-- Cropping stage -->
    <ClientOnly>
      <div v-if="rawImage" class="overflow-hidden rounded-lg border border-[var(--color-border)]">
        <Cropper
          ref="cropperRef"
          class="max-h-80 bg-[var(--color-surface-overlay)]"
          :src="rawImage"
          :stencil-props="{ aspectRatio }"
        />
        <div class="flex gap-2 border-t border-[var(--color-border)] p-3">
          <UiBaseButton
            type="button"
            variant="primary"
            size="sm"
            :loading="uploading"
            @click="cropAndUpload"
          >
            Crop & upload
          </UiBaseButton>
          <UiBaseButton type="button" variant="ghost" size="sm" @click="cancelCrop">
            Cancel
          </UiBaseButton>
        </div>
      </div>
    </ClientOnly>

    <!-- Current image preview -->
    <div
      v-if="model && !rawImage"
      class="overflow-hidden rounded-lg border border-[var(--color-border)]"
    >
      <img :src="model" alt="Cover preview" class="block w-full object-cover" />
      <div class="flex gap-2 border-t border-[var(--color-border)] p-3">
        <UiBaseButton type="button" variant="secondary" size="sm" @click="pick">
          Replace
        </UiBaseButton>
        <UiBaseButton type="button" variant="ghost" size="sm" @click="remove">
          Remove
        </UiBaseButton>
      </div>
    </div>

    <!-- Empty state -->
    <button
      v-if="!model && !rawImage"
      type="button"
      class="flex h-32 flex-col items-center justify-center gap-1 rounded-lg border border-dashed border-[var(--color-border)] text-sm text-[var(--color-text-muted)] transition-colors hover:border-[var(--color-ieee-blue)] hover:text-[var(--color-text-secondary)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-ieee-blue)]"
      @click="pick"
    >
      <svg
        class="size-6"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="1.5"
        aria-hidden="true"
      >
        <rect x="3" y="3" width="18" height="18" rx="2" />
        <circle cx="9" cy="9" r="2" />
        <path d="M21 15l-5-5L5 21" />
      </svg>
      Click to upload an image
    </button>

    <p v-if="error" class="text-xs text-red-500" role="alert">{{ error }}</p>
  </div>
</template>
