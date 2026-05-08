<script setup lang="ts">
interface Props {
  modelValue: string
  placeholder?: string
  hasError?: boolean
  disabled?: boolean
  rows?: number
  id?: string
}

withDefaults(defineProps<Props>(), {
  hasError: false,
  disabled: false,
  rows: 4,
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()
</script>

<template>
  <textarea
    :id="id"
    :value="modelValue"
    :placeholder="placeholder"
    :disabled="disabled"
    :rows="rows"
    :class="[
      'w-full resize-y rounded-lg border px-3 py-2 text-sm transition-colors',
      'bg-[var(--color-surface)] text-[var(--color-text-primary)]',
      'placeholder:text-[var(--color-text-tertiary)]',
      'focus:outline-none focus:ring-2 focus:ring-[var(--color-ieee-blue)]',
      'disabled:cursor-not-allowed disabled:opacity-50',
      hasError ? 'border-red-500 focus:ring-red-500' : 'border-[var(--color-border)]',
    ]"
    @input="emit('update:modelValue', ($event.target as HTMLTextAreaElement).value)"
  />
</template>
