<script setup lang="ts">
interface Props {
  modelValue: string
  placeholder?: string
  hasError?: boolean
  disabled?: boolean
  showStrength?: boolean
  id?: string
}

const props = withDefaults(defineProps<Props>(), {
  hasError: false,
  disabled: false,
  showStrength: false,
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const visible = ref(false)

const strengthScore = computed(() => {
  const pw = props.modelValue
  if (!pw) return 0
  let score = 0
  if (pw.length >= 12) score++
  if (pw.length >= 16) score++
  if (/[A-Z]/.test(pw) && /[a-z]/.test(pw)) score++
  if (/\d/.test(pw)) score++
  if (/[^A-Za-z0-9]/.test(pw)) score++
  return Math.min(score, 4)
})

const strengthLabel = computed(
  () => ['', 'Weak', 'Fair', 'Good', 'Strong'][strengthScore.value] ?? ''
)

const strengthColor = computed(
  () =>
    ['bg-gray-200', 'bg-red-500', 'bg-yellow-500', 'bg-blue-500', 'bg-green-500'][
      strengthScore.value
    ] ?? 'bg-gray-200'
)
</script>

<template>
  <div>
    <div class="relative">
      <input
        :id="id"
        :type="visible ? 'text' : 'password'"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :class="[
          'w-full rounded-lg border px-3 py-2 pr-10 text-sm transition-colors',
          'bg-[var(--color-surface)] text-[var(--color-text-primary)]',
          'placeholder:text-[var(--color-text-tertiary)]',
          'focus:outline-none focus:ring-2 focus:ring-[var(--color-ieee-blue)]',
          'disabled:cursor-not-allowed disabled:opacity-50',
          hasError ? 'border-red-500 focus:ring-red-500' : 'border-[var(--color-border)]',
        ]"
        @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      />
      <button
        type="button"
        class="absolute right-2 top-1/2 -translate-y-1/2 rounded p-1 text-[var(--color-text-tertiary)] hover:text-[var(--color-text-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-ieee-blue)]"
        :aria-label="visible ? 'Hide password' : 'Show password'"
        @click="visible = !visible"
      >
        <svg
          v-if="!visible"
          class="size-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
          />
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
          />
        </svg>
        <svg
          v-else
          class="size-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
          />
        </svg>
      </button>
    </div>
    <div v-if="showStrength && modelValue" class="mt-2 space-y-1">
      <div class="flex gap-1">
        <div
          v-for="i in 4"
          :key="i"
          class="h-1 flex-1 rounded-full transition-colors"
          :class="i <= strengthScore ? strengthColor : 'bg-[var(--color-border)]'"
        />
      </div>
      <p class="text-xs text-[var(--color-text-tertiary)]">{{ strengthLabel }}</p>
    </div>
  </div>
</template>
