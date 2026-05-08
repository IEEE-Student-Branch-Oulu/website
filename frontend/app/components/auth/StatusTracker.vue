<script setup lang="ts">
interface Props {
  status: string
}

const props = defineProps<Props>()

const steps = [
  { key: 'pending_email', label: 'Verify Email' },
  { key: 'pending_approval', label: 'Board Review' },
  { key: 'active', label: 'Active Member' },
]

const statusIndex = computed(() => {
  const idx = steps.findIndex((s) => s.key === props.status)
  return idx >= 0 ? idx : -1
})

const statusMessage = computed(() => {
  const messages: Record<string, string> = {
    pending_email: 'Please check your email and click the verification link.',
    pending_approval:
      'Your application is awaiting board review. This usually happens at the next board meeting.',
    active: 'Your membership is active. Welcome!',
    rejected: 'Your application was not approved. Please contact us for more information.',
    suspended: 'Your account has been suspended. Please contact an admin.',
  }
  return messages[props.status] ?? ''
})

const statusColor = computed(() => {
  if (props.status === 'rejected' || props.status === 'suspended') return 'text-red-500'
  if (props.status === 'active') return 'text-green-500'
  return 'text-yellow-500'
})
</script>

<template>
  <div class="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] p-6">
    <h3 class="mb-4 text-lg font-semibold text-[var(--color-text-primary)]">Membership Status</h3>

    <div
      v-if="status !== 'rejected' && status !== 'suspended'"
      class="mb-6 flex items-center gap-2"
    >
      <template v-for="(step, i) in steps" :key="step.key">
        <div class="flex items-center gap-2">
          <div
            :class="[
              'flex size-8 items-center justify-center rounded-full text-xs font-bold transition-colors',
              i <= statusIndex
                ? 'bg-[var(--color-ieee-blue)] text-white'
                : 'border-2 border-[var(--color-border)] text-[var(--color-text-tertiary)]',
            ]"
          >
            <svg
              v-if="i < statusIndex"
              class="size-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              aria-hidden="true"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="3"
                d="M5 13l4 4L19 7"
              />
            </svg>
            <span v-else>{{ i + 1 }}</span>
          </div>
          <span
            class="text-sm"
            :class="
              i <= statusIndex
                ? 'font-medium text-[var(--color-text-primary)]'
                : 'text-[var(--color-text-tertiary)]'
            "
          >
            {{ step.label }}
          </span>
        </div>
        <div
          v-if="i < steps.length - 1"
          class="mx-1 h-0.5 flex-1 rounded"
          :class="i < statusIndex ? 'bg-[var(--color-ieee-blue)]' : 'bg-[var(--color-border)]'"
        />
      </template>
    </div>

    <p :class="['text-sm', statusColor]">{{ statusMessage }}</p>
  </div>
</template>
