<script setup lang="ts">
interface Props {
  modelValue: boolean
  disabled?: boolean
  id?: string
}

defineProps<Props>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()
</script>

<template>
  <label :for="id" class="flex cursor-pointer items-start gap-3">
    <input
      :id="id"
      type="checkbox"
      :checked="modelValue"
      :disabled="disabled"
      class="mt-0.5 size-4 rounded border-[var(--color-border)] text-[var(--color-ieee-blue)] focus:ring-[var(--color-ieee-blue)]"
      @change="emit('update:modelValue', ($event.target as HTMLInputElement).checked)"
    />
    <span class="text-sm text-[var(--color-text-secondary)]">
      <slot />
    </span>
  </label>
</template>
