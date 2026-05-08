<script setup lang="ts">
const { toasts, dismiss } = useToast()

const typeClasses: Record<string, string> = {
  success: 'bg-green-600 text-white',
  error: 'bg-red-600 text-white',
  info: 'bg-[var(--color-ieee-blue)] text-white',
}
</script>

<template>
  <Teleport to="body">
    <div class="fixed right-4 top-4 z-[100] flex flex-col gap-2" aria-live="polite">
      <TransitionGroup
        enter-active-class="transition-all duration-300 ease-out"
        enter-from-class="translate-x-full opacity-0"
        enter-to-class="translate-x-0 opacity-100"
        leave-active-class="transition-all duration-200 ease-in"
        leave-from-class="translate-x-0 opacity-100"
        leave-to-class="translate-x-full opacity-0"
      >
        <div
          v-for="toast in toasts"
          :key="toast.id"
          :class="[
            typeClasses[toast.type],
            'flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium shadow-lg',
          ]"
          role="alert"
        >
          <span class="flex-1">{{ toast.message }}</span>
          <button
            class="rounded p-0.5 opacity-80 hover:opacity-100"
            aria-label="Dismiss"
            @click="dismiss(toast.id)"
          >
            <svg
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
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>
