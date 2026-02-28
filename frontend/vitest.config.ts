import { defineVitestConfig } from '@nuxt/test-utils/config'

export default defineVitestConfig({
  test: {
    environment: 'nuxt',
    environmentOptions: {
      nuxt: {
        domEnvironment: 'happy-dom',
      },
    },
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/**',
        '.nuxt/**',
        '.output/**',
        'coverage/**',
        'tests/e2e/**',
        '**/*.config.*',
        '**/*.d.ts',
      ],
      thresholds: {
        lines: 70,
        functions: 70,
      },
    },
  },
})
