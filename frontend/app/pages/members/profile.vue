<script setup lang="ts">
definePageMeta({ middleware: 'auth' })
useHead({ title: 'Edit Profile - IEEE SB Oulu' })

const { user, fetchMe } = useAuth()
const { api } = useApi()
const toast = useToast()

await callOnce(fetchMe)

const loading = ref(false)
const form = reactive({
  firstName: user.value?.firstName ?? '',
  lastName: user.value?.lastName ?? '',
  ieeeGrade: user.value?.ieeeGrade ?? '',
  university: user.value?.university ?? '',
  studyLevel: user.value?.studyLevel ?? '',
  studyProgram: user.value?.studyProgram ?? '',
  expectedGraduationYear: user.value?.expectedGraduationYear?.toString() ?? '',
  bio: user.value?.bio ?? '',
  profileVisibility: user.value?.profileVisibility ?? 'private',
})

const studyLevelOptions = [
  { label: "Bachelor's", value: 'bsc' },
  { label: "Master's", value: 'msc' },
  { label: 'PhD', value: 'phd' },
  { label: 'Postdoc', value: 'postdoc' },
  { label: 'Other', value: 'other' },
]

const visibilityOptions = [
  { label: 'Private (only you)', value: 'private' },
  { label: 'Members only', value: 'members' },
  { label: 'Public (directory)', value: 'public' },
]

async function submit() {
  loading.value = true
  try {
    await api('/members/me', {
      method: 'PATCH',
      body: {
        firstName: form.firstName,
        lastName: form.lastName,
        ieeeGrade: form.ieeeGrade || null,
        university: form.university,
        studyLevel: form.studyLevel || null,
        studyProgram: form.studyProgram || null,
        expectedGraduationYear: form.expectedGraduationYear
          ? parseInt(form.expectedGraduationYear)
          : null,
        bio: form.bio || null,
        profileVisibility: form.profileVisibility,
      },
    })
    await fetchMe()
    toast.success('Profile updated.')
  } catch (e: unknown) {
    const err = e as { detail?: string }
    toast.error(err?.detail ?? 'Update failed.')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="mx-auto max-w-lg px-4 py-16">
    <h1 class="mb-8 text-2xl font-bold text-[var(--color-text-primary)]">Edit Profile</h1>

    <form class="space-y-4" @submit.prevent="submit">
      <div class="grid grid-cols-2 gap-4">
        <UiFormField label="First name">
          <template #default="{ id }">
            <UiInputField :id="id" v-model="form.firstName" />
          </template>
        </UiFormField>
        <UiFormField label="Last name">
          <template #default="{ id }">
            <UiInputField :id="id" v-model="form.lastName" />
          </template>
        </UiFormField>
      </div>

      <UiFormField label="IEEE Grade">
        <template #default="{ id }">
          <UiInputField :id="id" v-model="form.ieeeGrade" />
        </template>
      </UiFormField>

      <UiFormField label="University">
        <template #default="{ id }">
          <UiInputField :id="id" v-model="form.university" />
        </template>
      </UiFormField>

      <UiFormField label="Study level">
        <template #default="{ id }">
          <UiSelectField
            :id="id"
            v-model="form.studyLevel"
            :options="studyLevelOptions"
            placeholder="Select..."
          />
        </template>
      </UiFormField>

      <UiFormField label="Study program">
        <template #default="{ id }">
          <UiInputField :id="id" v-model="form.studyProgram" />
        </template>
      </UiFormField>

      <UiFormField label="Expected graduation year">
        <template #default="{ id }">
          <UiInputField :id="id" v-model="form.expectedGraduationYear" type="number" />
        </template>
      </UiFormField>

      <UiFormField label="Bio">
        <template #default="{ id }">
          <UiTextareaField
            :id="id"
            v-model="form.bio"
            placeholder="Tell us about yourself..."
            :rows="3"
          />
        </template>
      </UiFormField>

      <UiFormField
        label="Profile visibility"
        hint="'Public' shows your profile in the member directory"
      >
        <template #default="{ id }">
          <UiSelectField :id="id" v-model="form.profileVisibility" :options="visibilityOptions" />
        </template>
      </UiFormField>

      <div class="flex gap-3 pt-4">
        <UiBaseButton href="/members" variant="ghost">Cancel</UiBaseButton>
        <UiBaseButton type="submit" variant="primary" class="flex-1" :loading="loading">
          Save Changes
        </UiBaseButton>
      </div>
    </form>
  </div>
</template>
