/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class', // controlled by our useColorMode composable

  theme: {
    extend: {
      // ── Brand colors ──────────────────────────────────────────
      colors: {
        ieee: {
          blue: '#00629B',
          'blue-light': '#0077BB',
          'blue-dark': '#004F7C',
          accent: '#00A3E0',
        },
      },

      // ── Typography ────────────────────────────────────────────
      fontFamily: {
        sans: ['IBM Plex Sans', 'system-ui', 'sans-serif'],
        mono: ['IBM Plex Mono', 'Menlo', 'monospace'],
      },

      // ── Spacing ───────────────────────────────────────────────
      spacing: {
        nav: 'var(--nav-height)',
      },

      // ── Page transition ───────────────────────────────────────
      keyframes: {
        'fade-in': {
          from: { opacity: '0', transform: 'translateY(6px)' },
          to: { opacity: '1', transform: 'translateY(0)' },
        },
      },
      animation: {
        'fade-in': 'fade-in 0.3s ease-out both',
      },
    },
  },

  plugins: [],
}
