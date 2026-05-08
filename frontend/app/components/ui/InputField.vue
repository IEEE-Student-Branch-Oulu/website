<script setup lang="ts">
interface Props {
  modelValue: string
  type?: string
  placeholder?: string
  hasError?: boolean
  disabled?: boolean
  id?: string
}

withDefaults(defineProps<Props>(), {
  type: 'text',
  hasError: false,
  disabled: false,
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()
</script>

<template>
  <input
    :id="id"
    :type="type"
    :value="modelValue"
    :placeholder="placeholder"
    :disabled="disabled"
    :class="[
      'w-full rounded-lg border px-3 py-2 text-sm transition-colors',
      'bg-[var(--color-surface)] text-[var(--color-text-primary)]',
      'placeholder:text-[var(--color-text-tertiary)]',
      'focus:outline-none focus:ring-2 focus:ring-[var(--color-ieee-blue)]',
      'disabled:cursor-not-allowed disabled:opacity-50',
      hasError ? 'border-red-500 focus:ring-red-500' : 'border-[var(--color-border)]',
    ]"
    @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
  />
</template>
