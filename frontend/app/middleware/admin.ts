export default defineNuxtRouteMiddleware(async () => {
  const { isAuthenticated, isAdmin, ensureLoaded } = useAuth()
  await ensureLoaded()
  if (!isAuthenticated.value) {
    return navigateTo('/auth/login')
  }
  if (!isAdmin.value) {
    throw createError({ statusCode: 403, statusMessage: 'Admin access required' })
  }
})
