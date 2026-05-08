<script setup lang="ts">
definePageMeta({ layout: 'default' })

useHead({ title: 'Register - IEEE SB Oulu' })

const { register } = useAuth()
const toast = useToast()

const step = ref(1)
const loading = ref(false)
const errors = ref<Record<string, string>>({})

const form = reactive({
  email: '',
  password: '',
  firstName: '',
  lastName: '',
  ieeeMembershipNumber: '',
  ieeeGrade: '',
  university: 'University of Oulu',
  studyLevel: '',
  studyProgram: '',
  expectedGraduationYear: '',
  privacyConsent: false,
  termsConsent: false,
  directoryOptIn: false,
})

const studyLevelOptions = [
  { label: "Bachelor's", value: 'bsc' },
  { label: "Master's", value: 'msc' },
  { label: 'PhD', value: 'phd' },
  { label: 'Postdoc', value: 'postdoc' },
  { label: 'Other', value: 'other' },
]

function validateStep1(): boolean {
  errors.value = {}
  if (!form.email) errors.value.email = 'Email is required'
  if (form.password.length < 12) errors.value.password = 'Password must be at least 12 characters'
  if (!form.firstName) errors.value.firstName = 'First name is required'
  if (!form.lastName) errors.value.lastName = 'Last name is required'
  return Object.keys(errors.value).length === 0
}

function validateStep2(): boolean {
  errors.value = {}
  if (!/^\d{8,10}$/.test(form.ieeeMembershipNumber)) {
    errors.value.ieeeMembershipNumber = 'IEEE membership number must be 8-10 digits'
  }
  return Object.keys(errors.value).length === 0
}

function validateStep3(): boolean {
  errors.value = {}
  if (!form.privacyConsent) errors.value.privacy = 'You must accept the privacy policy'
  if (!form.termsConsent) errors.value.terms = 'You must accept the terms of service'
  return Object.keys(errors.value).length === 0
}

function nextStep() {
  if (step.value === 1 && validateStep1()) step.value = 2
  else if (step.value === 2 && validateStep2()) step.value = 3
}

async function submit() {
  if (!validateStep3()) return

  loading.value = true
  try {
    await register({
      email: form.email,
      password: form.password,
      firstName: form.firstName,
      lastName: form.lastName,
      ieeeMembershipNumber: form.ieeeMembershipNumber,
      ieeeGrade: form.ieeeGrade || undefined,
      university: form.university,
      studyLevel: form.studyLevel || undefined,
      studyProgram: form.studyProgram || undefined,
      expectedGraduationYear: form.expectedGraduationYear
        ? parseInt(form.expectedGraduationYear)
        : undefined,
      profileVisibility: form.directoryOptIn ? 'public' : 'private',
      consents: {
        privacy: { version: '1.0', accepted_at: new Date().toISOString() },
        terms: { version: '1.0', accepted_at: new Date().toISOString() },
      },
    })
    await navigateTo('/auth/check-your-email')
  } catch (e: unknown) {
    const err = e as { detail?: string; title?: string }
    toast.error(err?.detail ?? err?.title ?? 'Registration failed. Please try again.')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="mx-auto max-w-lg px-4 py-16">
    <h1 class="mb-2 text-2xl font-bold text-[var(--color-text-primary)]">
      Join IEEE Student Branch Oulu
    </h1>
    <p class="mb-8 text-sm text-[var(--color-text-secondary)]">Step {{ step }} of 3</p>

    <div class="mb-8 flex gap-1">
      <div
        v-for="i in 3"
        :key="i"
        class="h-1 flex-1 rounded-full transition-colors"
        :class="i <= step ? 'bg-[var(--color-ieee-blue)]' : 'bg-[var(--color-border)]'"
      />
    </div>

    <!-- Step 1: Account -->
    <form v-if="step === 1" class="space-y-4" @submit.prevent="nextStep">
      <UiFormField label="Email" :error="errors.email" required>
        <template #default="{ id, hasError }">
          <UiInputField
            :id="id"
            v-model="form.email"
            type="email"
            placeholder="you@example.com"
            :has-error="hasError"
          />
        </template>
      </UiFormField>

      <UiFormField label="Password" :error="errors.password" hint="At least 12 characters" required>
        <template #default="{ id, hasError }">
          <UiPasswordInput
            :id="id"
            v-model="form.password"
            placeholder="Choose a strong password"
            :has-error="hasError"
            show-strength
          />
        </template>
      </UiFormField>

      <div class="grid grid-cols-2 gap-4">
        <UiFormField label="First name" :error="errors.firstName" required>
          <template #default="{ id, hasError }">
            <UiInputField :id="id" v-model="form.firstName" :has-error="hasError" />
          </template>
        </UiFormField>
        <UiFormField label="Last name" :error="errors.lastName" required>
          <template #default="{ id, hasError }">
            <UiInputField :id="id" v-model="form.lastName" :has-error="hasError" />
          </template>
        </UiFormField>
      </div>

      <UiBaseButton type="submit" variant="primary" class="w-full">Continue</UiBaseButton>
    </form>

    <!-- Step 2: IEEE & Academic -->
    <form v-else-if="step === 2" class="space-y-4" @submit.prevent="nextStep">
      <div
        class="rounded-lg border border-blue-200 bg-blue-50 p-4 text-sm text-blue-800 dark:border-blue-800 dark:bg-blue-950 dark:text-blue-200"
      >
        <strong>IEEE membership required.</strong> You must be an IEEE member to join the student
        branch.
        <a
          href="https://www.ieee.org/membership/students/"
          target="_blank"
          rel="noopener noreferrer"
          class="underline hover:no-underline"
        >
          Become an IEEE member
        </a>
      </div>

      <UiFormField label="IEEE Membership Number" :error="errors.ieeeMembershipNumber" required>
        <template #default="{ id, hasError }">
          <UiInputField
            :id="id"
            v-model="form.ieeeMembershipNumber"
            placeholder="12345678"
            :has-error="hasError"
          />
        </template>
      </UiFormField>

      <UiFormField label="IEEE Grade" hint="e.g. Student Member, Graduate Student Member">
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
          <UiInputField :id="id" v-model="form.studyProgram" placeholder="e.g. Computer Science" />
        </template>
      </UiFormField>

      <UiFormField label="Expected graduation year">
        <template #default="{ id }">
          <UiInputField
            :id="id"
            v-model="form.expectedGraduationYear"
            type="number"
            placeholder="2027"
          />
        </template>
      </UiFormField>

      <div class="flex gap-3">
        <UiBaseButton variant="ghost" @click="step = 1">Back</UiBaseButton>
        <UiBaseButton type="submit" variant="primary" class="flex-1">Continue</UiBaseButton>
      </div>
    </form>

    <!-- Step 3: Consent -->
    <form v-else class="space-y-4" @submit.prevent="submit">
      <AuthConsentCheckbox v-model="form.privacyConsent" required>
        I have read and accept the
        <NuxtLink to="/legal/privacy" class="underline">Privacy Policy</NuxtLink> (v1.0)
      </AuthConsentCheckbox>
      <p v-if="errors.privacy" class="text-xs text-red-500">{{ errors.privacy }}</p>

      <AuthConsentCheckbox v-model="form.termsConsent" required>
        I have read and accept the
        <NuxtLink to="/legal/terms" class="underline">Terms of Service</NuxtLink> (v1.0)
      </AuthConsentCheckbox>
      <p v-if="errors.terms" class="text-xs text-red-500">{{ errors.terms }}</p>

      <div
        class="mt-4 rounded-lg border border-[var(--color-border)] bg-[var(--color-surface-overlay)] p-4"
      >
        <UiCheckboxField v-model="form.directoryOptIn">
          <span class="text-sm text-[var(--color-text-secondary)]">
            Show my profile in the <strong>member directory</strong> so other members can find me.
            You can change this anytime in your profile settings.
          </span>
        </UiCheckboxField>
      </div>

      <div class="flex gap-3">
        <UiBaseButton variant="ghost" @click="step = 2">Back</UiBaseButton>
        <UiBaseButton type="submit" variant="primary" class="flex-1" :loading="loading">
          Create Account
        </UiBaseButton>
      </div>
    </form>

    <p class="mt-6 text-center text-sm text-[var(--color-text-secondary)]">
      Already have an account?
      <NuxtLink to="/auth/login" class="text-[var(--color-ieee-blue)] hover:underline"
        >Log in</NuxtLink
      >
    </p>
  </div>
</template>
