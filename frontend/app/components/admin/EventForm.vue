<script setup lang="ts">
/**
 * EventForm
 *
 * Shared create/edit form for events. Datetime-local inputs are read in
 * the browser's local timezone and submitted as full ISO strings (with
 * offset) so the backend stores correct UTC.
 */
import {
  EVENT_TYPE_META,
  type EventEdit,
  type EventInput,
  type EventType,
} from '~/composables/useEvents'

const props = defineProps<{
  initial?: EventEdit | null
  submitting?: boolean
  error?: string | null
}>()

const emit = defineEmits<{ submit: [value: EventInput] }>()

function toLocalInput(iso?: string | null): string {
  if (!iso) return ''
  const d = new Date(iso)
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`
}

const title = ref(props.initial?.title ?? '')
const description = ref(props.initial?.description ?? '')
const type = ref<EventType>(props.initial?.type ?? 'workshop')
const startsAt = ref(toLocalInput(props.initial?.startsAt))
const endsAt = ref(toLocalInput(props.initial?.endsAt))
const location = ref(props.initial?.location ?? '')
const locationUrl = ref(props.initial?.locationUrl ?? '')
const rsvpLink = ref(props.initial?.rsvpLink ?? '')
const speakerName = ref(props.initial?.speakerName ?? '')
const speakerTitle = ref(props.initial?.speakerTitle ?? '')
const coverImageUrl = ref<string | null>(props.initial?.coverImageUrl ?? null)
const tagsText = ref((props.initial?.tags ?? []).join(', '))
const isHighlighted = ref(props.initial?.isHighlighted ?? false)

const typeOptions = Object.entries(EVENT_TYPE_META).map(([value, meta]) => ({
  value,
  label: meta.label,
}))

const formError = ref<string | null>(null)

function onSubmit() {
  if (!startsAt.value) {
    formError.value = 'Start date & time is required.'
    return
  }
  formError.value = null
  emit('submit', {
    title: title.value.trim(),
    description: description.value.trim(),
    type: type.value,
    startsAt: new Date(startsAt.value).toISOString(),
    endsAt: endsAt.value ? new Date(endsAt.value).toISOString() : null,
    location: location.value.trim(),
    locationUrl: locationUrl.value.trim() || null,
    rsvpLink: rsvpLink.value.trim() || null,
    speakerName: speakerName.value.trim() || null,
    speakerTitle: speakerTitle.value.trim() || null,
    coverImageUrl: coverImageUrl.value?.trim() || null,
    tags: tagsText.value
      .split(',')
      .map((t) => t.trim())
      .filter(Boolean),
    isHighlighted: isHighlighted.value,
  })
}
</script>

<template>
  <form class="flex flex-col gap-6" @submit.prevent="onSubmit">
    <UiFormField v-slot="{ id, hasError }" label="Title" required>
      <UiInputField :id="id" v-model="title" :has-error="hasError" placeholder="Event title" />
    </UiFormField>

    <UiFormField v-slot="{ id }" label="Type" required>
      <UiSelectField :id="id" v-model="type" :options="typeOptions" />
    </UiFormField>

    <div class="grid gap-6 sm:grid-cols-2">
      <UiFormField v-slot="{ id }" label="Starts at" required>
        <UiInputField :id="id" v-model="startsAt" type="datetime-local" />
      </UiFormField>

      <UiFormField v-slot="{ id }" label="Ends at" hint="Optional">
        <UiInputField :id="id" v-model="endsAt" type="datetime-local" />
      </UiFormField>
    </div>

    <div class="grid gap-6 sm:grid-cols-2">
      <UiFormField v-slot="{ id, hasError }" label="Location" required>
        <UiInputField
          :id="id"
          v-model="location"
          :has-error="hasError"
          placeholder="Linnanmaa Campus, TS101"
        />
      </UiFormField>

      <UiFormField v-slot="{ id }" label="Location URL" hint="Maps / Mazemap link">
        <UiInputField :id="id" v-model="locationUrl" placeholder="https://maps.google.com/…" />
      </UiFormField>
    </div>

    <UiFormField v-slot="{ id, hasError }" label="Description" required>
      <UiTextareaField
        :id="id"
        v-model="description"
        :has-error="hasError"
        :rows="4"
        placeholder="What the event is about"
      />
    </UiFormField>

    <div class="grid gap-6 sm:grid-cols-2">
      <UiFormField v-slot="{ id }" label="RSVP link" hint="Optional">
        <UiInputField :id="id" v-model="rsvpLink" placeholder="https://forms.gle/…" />
      </UiFormField>

      <UiFormField label="Cover image" hint="16:9 — crop after selecting">
        <AdminImageUpload v-model="coverImageUrl" :aspect-ratio="16 / 9" />
      </UiFormField>
    </div>

    <div class="grid gap-6 sm:grid-cols-2">
      <UiFormField v-slot="{ id }" label="Speaker name" hint="Talks only">
        <UiInputField :id="id" v-model="speakerName" placeholder="Dr. Aino Mäkinen" />
      </UiFormField>

      <UiFormField v-slot="{ id }" label="Speaker title" hint="Talks only">
        <UiInputField :id="id" v-model="speakerTitle" placeholder="Senior Researcher, Nokia" />
      </UiFormField>
    </div>

    <UiFormField v-slot="{ id }" label="Tags" hint="Comma-separated">
      <UiInputField :id="id" v-model="tagsText" placeholder="Python, ML, Workshop" />
    </UiFormField>

    <UiCheckboxField v-model="isHighlighted">
      <span class="text-sm text-[var(--color-text-primary)]">Highlight this event (featured)</span>
    </UiCheckboxField>

    <p v-if="formError || error" class="text-sm text-red-500" role="alert">
      {{ formError || error }}
    </p>

    <div class="flex gap-3">
      <UiBaseButton type="submit" variant="primary" :loading="submitting">
        {{ initial ? 'Save changes' : 'Create event' }}
      </UiBaseButton>
      <UiBaseButton href="/admin/events" variant="ghost">Cancel</UiBaseButton>
    </div>
  </form>
</template>
