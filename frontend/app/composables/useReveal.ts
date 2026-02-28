/**
 * useReveal
 *
 * Scroll-triggered visibility composable.
 * Bind `el` to the element you want to animate, then use `isVisible`
 * to toggle animation classes. Triggers once and stops observing.
 *
 * Uses the native IntersectionObserver API — no external dependencies.
 *
 * Usage:
 *   const { el, isVisible } = useReveal()
 *   <div ref="el" :class="isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'">
 */

export function useReveal(threshold = 0.15) {
  const el = ref<HTMLElement | null>(null)
  const isVisible = ref(false)
  let observer: IntersectionObserver | null = null

  const cleanup = () => {
    if (observer) {
      observer.disconnect()
      observer = null
    }
  }

  onMounted(() => {
    if (!el.value) return

    observer = new IntersectionObserver(
      (entries: IntersectionObserverEntry[]) => {
        const entry = entries[0]
        if (entry?.isIntersecting) {
          isVisible.value = true
          cleanup()
        }
      },
      { threshold }
    )

    observer.observe(el.value)
  })

  onUnmounted(cleanup)

  return { el, isVisible }
}
