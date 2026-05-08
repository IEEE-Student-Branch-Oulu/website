/**
 * Simple toast notification composable.
 */

export interface Toast {
  id: number
  message: string
  type: 'success' | 'error' | 'info'
}

export function useToast() {
  const nextId = useState<number>('toast-next-id', () => 0)
  const toasts = useState<Toast[]>('toasts', () => [])

  function show(message: string, type: Toast['type'] = 'info', duration = 4000) {
    const id = nextId.value++
    toasts.value.push({ id, message, type })
    if (duration > 0) {
      setTimeout(() => dismiss(id), duration)
    }
  }

  function dismiss(id: number) {
    toasts.value = toasts.value.filter((t) => t.id !== id)
  }

  function success(message: string) {
    show(message, 'success')
  }
  function error(message: string) {
    show(message, 'error', 6000)
  }

  return { toasts, show, dismiss, success, error }
}
