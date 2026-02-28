/**
 * useCountdown
 *
 * Reactive countdown timer to a target date.
 * Updates every second on the client. SSR-safe.
 *
 * Usage:
 *   const { formatted, time } = useCountdown('2026-03-15T13:00:00')
 *   // formatted.days → '14', formatted.hours → '06', etc.
 */

export interface CountdownTime {
  days: number
  hours: number
  minutes: number
  seconds: number
  total: number
  isExpired: boolean
}

export function useCountdown(targetDate: string | Date) {
  const target = new Date(targetDate).getTime()

  function calculate(): CountdownTime {
    const total = target - Date.now()
    if (total <= 0) {
      return { days: 0, hours: 0, minutes: 0, seconds: 0, total: 0, isExpired: true }
    }
    return {
      days: Math.floor(total / 864e5),
      hours: Math.floor((total % 864e5) / 36e5),
      minutes: Math.floor((total % 36e5) / 6e4),
      seconds: Math.floor((total % 6e4) / 1000),
      total,
      isExpired: false,
    }
  }

  const time = ref<CountdownTime>(calculate())

  const formatted = computed(() => ({
    days: String(time.value.days).padStart(2, '0'),
    hours: String(time.value.hours).padStart(2, '0'),
    minutes: String(time.value.minutes).padStart(2, '0'),
    seconds: String(time.value.seconds).padStart(2, '0'),
  }))

  let interval: ReturnType<typeof setInterval>

  onMounted(() => {
    time.value = calculate()
    interval = setInterval(() => {
      time.value = calculate()
      if (time.value.isExpired) clearInterval(interval)
    }, 1000)
  })

  onUnmounted(() => clearInterval(interval))

  return { time, formatted }
}
