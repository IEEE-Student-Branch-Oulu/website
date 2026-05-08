/**
 * Auth state composable — manages user session, login, logout, register.
 */

export type UserStatus = 'pending_email' | 'pending_approval' | 'active' | 'rejected' | 'suspended'
export type UserRole = 'member' | 'admin'
export type MembershipStatus = 'pending' | 'approved' | 'rejected' | 'lapsed'

export interface MembershipPeriod {
  id: number
  periodYear: number
  status: MembershipStatus
  ieeeMembershipNumber: string
  appliedAt: string
  reviewedAt: string | null
}

export interface AuthUser {
  id: number
  email: string
  firstName: string
  lastName: string
  role: UserRole
  status: UserStatus
  emailVerifiedAt: string | null
  ieeeMembershipNumber: string
  ieeeGrade: string | null
  university: string
  studyLevel: string | null
  studyProgram: string | null
  expectedGraduationYear: number | null
  bio: string | null
  profileVisibility: string
  consents: Record<string, unknown>
  createdAt: string
  membershipPeriods: MembershipPeriod[]
}

type AuthStatus = 'idle' | 'loading' | 'authenticated' | 'unauthenticated'

export function useAuth() {
  const user = useState<AuthUser | null>('auth-user', () => null)
  const status = useState<AuthStatus>('auth-status', () => 'idle')

  const isAuthenticated = computed(() => status.value === 'authenticated')
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isActive = computed(() => user.value?.status === 'active')

  const { api } = useApi()

  async function fetchMe() {
    try {
      status.value = 'loading'
      user.value = await api<AuthUser>('/auth/me')
      status.value = 'authenticated'
    } catch {
      user.value = null
      status.value = 'unauthenticated'
    }
  }

  async function login(email: string, password: string) {
    user.value = await api<AuthUser>('/auth/login', {
      method: 'POST',
      body: { email, password },
    })
    status.value = 'authenticated'
  }

  async function logout() {
    try {
      await api('/auth/logout', { method: 'POST' })
    } finally {
      user.value = null
      status.value = 'unauthenticated'
    }
  }

  async function register(data: Record<string, unknown>) {
    return await api<{ message: string }>('/auth/register', {
      method: 'POST',
      body: data,
    })
  }

  async function ensureLoaded() {
    if (status.value === 'idle') {
      await fetchMe()
    }
  }

  return {
    user,
    status,
    isAuthenticated,
    isAdmin,
    isActive,
    fetchMe,
    ensureLoaded,
    login,
    logout,
    register,
  }
}
