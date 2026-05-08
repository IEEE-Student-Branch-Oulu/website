<script setup lang="ts">
interface Props {
  modelValue: boolean
  required?: boolean
}

defineProps<Props>()
const emit = defineEmits<{ 'update:modelValue': [value: boolean] }>()
</script>

<template>
  <UiCheckboxField
    :model-value="modelValue"
    @update:model-value="emit('update:modelValue', $event)"
  >
    <slot />
    <span v-if="required" class="ml-0.5 text-red-500" aria-hidden="true">*</span>
  </UiCheckboxField>
</template>
