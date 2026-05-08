export default defineNuxtRouteMiddleware(async () => {
  const { isAuthenticated, isActive, ensureLoaded } = useAuth()
  await ensureLoaded()
  if (!isAuthenticated.value) {
    return navigateTo('/auth/login')
  }
  if (!isActive.value) {
    return navigateTo('/members')
  }
})
