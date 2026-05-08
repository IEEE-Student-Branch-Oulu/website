export default defineNuxtRouteMiddleware(async (to) => {
  const { isAuthenticated, ensureLoaded } = useAuth()
  await ensureLoaded()
  if (!isAuthenticated.value) {
    return navigateTo(`/auth/login?next=${encodeURIComponent(to.fullPath)}`)
  }
})
