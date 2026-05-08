<script setup lang="ts">
interface Props {
  label: string
  error?: string
  hint?: string
  required?: boolean
}

defineProps<Props>()

const id = useId()
</script>

<template>
  <div class="space-y-1">
    <label :for="id" class="block text-sm font-medium text-[var(--color-text-primary)]">
      {{ label }}
      <span v-if="required" class="text-red-500" aria-hidden="true">*</span>
    </label>
    <slot :id="id" :has-error="!!error" />
    <p v-if="hint && !error" class="text-xs text-[var(--color-text-tertiary)]">{{ hint }}</p>
    <p v-if="error" class="text-xs text-red-500" role="alert">{{ error }}</p>
  </div>
</template>
