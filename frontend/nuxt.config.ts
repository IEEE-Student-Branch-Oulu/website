// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  srcDir: 'app',
  devtools: { enabled: true },

  typescript: {
    typeCheck: true,
  },

  modules: ['@nuxtjs/tailwindcss', '@nuxt/eslint'],

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE ?? 'http://localhost:8000/api/v1',
    },
  },

  tailwindcss: {
    exposeConfig: true,
    viewer: true,
  },

  eslint: {
    config: {
      stylistic: false,
    },
  },

  css: ['~/assets/css/main.css', '~/assets/css/transitions.css'],
})
