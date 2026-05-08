/**
 * API client composable — wraps $fetch with credentials and CSRF handling.
 *
 * During SSR, forwards the browser's cookies to the backend so that
 * server-rendered pages see the authenticated state (no auth flash).
 */

export interface ApiError {
  type: string
  title: string
  status: number
  detail: string
  errors?: Array<{ loc: string[]; msg: string; type: string }>
}

function getCsrfToken(): string | null {
  if (import.meta.server) return null
  const match = document.cookie.match(/(?:^|;\s*)ieee_csrf=([^;]+)/)
  return match ? decodeURIComponent(match[1]!) : null
}

export function useApi() {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase as string

  const ssrHeaders = import.meta.server ? useRequestHeaders(['cookie']) : {}

  async function api<T>(
    path: string,
    options: {
      method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE' | 'HEAD' | 'OPTIONS'
      body?: unknown
      query?: Record<string, string | number | boolean | undefined>
    } = {}
  ): Promise<T> {
    const headers: Record<string, string> = {}

    if (import.meta.server && ssrHeaders.cookie) {
      headers.cookie = ssrHeaders.cookie
    }

    if (options.method && !['GET', 'HEAD', 'OPTIONS'].includes(options.method)) {
      const csrf = getCsrfToken()
      if (csrf) headers['X-CSRF-Token'] = csrf
    }

    try {
      return await $fetch<T>(path, {
        baseURL,
        credentials: 'include',
        method: options.method,
        body: options.body as Record<string, unknown> | undefined,
        query: options.query,
        headers,
      })
    } catch (error: unknown) {
      if (error && typeof error === 'object' && 'data' in error) {
        const fetchError = error as { data: ApiError; statusCode: number }
        throw fetchError.data
      }
      throw error
    }
  }

  return { api }
}
