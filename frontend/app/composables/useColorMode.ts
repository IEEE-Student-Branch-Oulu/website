/**
 * useColorMode
 *
 * Manages light/dark mode with:
 * - System preference detection
 * - Manual toggle persisted to localStorage
 * - SSR-safe (no hydration mismatch)
 *
 * Usage:
 *   const { isDark, toggle, mode } = useColorMode()
 */
export type ColorMode = 'light' | 'dark' | 'system'

const STORAGE_KEY = 'ieee-oulu-color-mode'

export function useColorMode() {
  const mode = useState<ColorMode>('color-mode', () => 'system')
  const isDark = useState<boolean>('is-dark', () => false)

  function getSystemPreference(): boolean {
    if (import.meta.server) return false
    return window.matchMedia('(prefers-color-scheme: dark)').matches
  }

  function applyMode(value: ColorMode) {
    const dark = value === 'dark' || (value === 'system' && getSystemPreference())
    isDark.value = dark
    if (import.meta.client) {
      document.documentElement.classList.toggle('dark', dark)
      localStorage.setItem(STORAGE_KEY, value)
    }
  }

  function toggle() {
    const next = isDark.value ? 'light' : 'dark'
    mode.value = next
    applyMode(next)
  }

  function setMode(value: ColorMode) {
    mode.value = value
    applyMode(value)
  }

  function init() {
    if (import.meta.server) return

    const stored = localStorage.getItem(STORAGE_KEY) as ColorMode | null
    const initial: ColorMode = stored ?? 'system'
    mode.value = initial
    applyMode(initial)

    // Listen for system preference changes (only affects 'system' mode)
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
      if (mode.value === 'system') applyMode('system')
    })
  }

  return { isDark, mode, toggle, setMode, init }
}
