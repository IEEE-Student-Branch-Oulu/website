<script setup lang="ts">
interface Props {
  modelValue: string
  options: Array<{ label: string; value: string }>
  placeholder?: string
  hasError?: boolean
  disabled?: boolean
  id?: string
}

withDefaults(defineProps<Props>(), {
  hasError: false,
  disabled: false,
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()
</script>

<template>
  <select
    :id="id"
    :value="modelValue"
    :disabled="disabled"
    :class="[
      'w-full appearance-none rounded-lg border px-3 py-2 text-sm transition-colors',
      'bg-[var(--color-surface)] text-[var(--color-text-primary)]',
      'focus:outline-none focus:ring-2 focus:ring-[var(--color-ieee-blue)]',
      'disabled:cursor-not-allowed disabled:opacity-50',
      hasError ? 'border-red-500 focus:ring-red-500' : 'border-[var(--color-border)]',
    ]"
    @change="emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
  >
    <option v-if="placeholder" value="" disabled>{{ placeholder }}</option>
    <option v-for="opt in options" :key="opt.value" :value="opt.value">
      {{ opt.label }}
    </option>
  </select>
</template>
