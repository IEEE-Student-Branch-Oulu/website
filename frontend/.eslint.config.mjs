import withNuxt from './.nuxt/eslint.config.mjs'
import configPrettier from 'eslint-config-prettier'

export default withNuxt(configPrettier, {
  rules: {
    // Vue
    'vue/component-api-style': ['error', ['script-setup']], // enforce <script setup>
    'vue/block-order': ['error', { order: ['script', 'template', 'style'] }],
    'vue/no-unused-vars': 'error',

    // General
    'no-console': ['warn', { allow: ['warn', 'error'] }],
    'no-debugger': 'error',
  },
})
