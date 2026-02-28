<script setup lang="ts">
/**
 * BlogPostBody
 *
 * Renders the HTML body of a blog post with a full prose typography system.
 *
 * In production this receives pre-rendered HTML from markdown-it on the backend.
 * The styles defined here control all rendered content:
 *   - Headings with anchor links
 *   - Code blocks (terminal aesthetic — dark even in light mode)
 *   - Inline code
 *   - Blockquotes (styled as callouts)
 *   - Lists, tables, figures
 *
 * Props:
 *   html     - the rendered HTML string (from markdown-it or equivalent)
 *   category - used for heading accent color
 *
 * Usage:
 *   <BlogPostBody :html="post.bodyHtml" :category="post.category" />
 */
import { CATEGORY_META, type PostCategory } from '~/composables/useBlog'

interface Props {
  html: string
  category?: PostCategory
}

const props = withDefaults(defineProps<Props>(), { category: 'workshop-recap' })

const accentColor = computed(() => CATEGORY_META[props.category].color)
</script>

<template>
  <div class="post-body" :style="{ '--post-accent': accentColor }" v-html="html" />
</template>

<style>
/* ─── Post prose typography system ──────────────────────────────
   Scoped to .post-body so it never leaks outside the content area.
   Uses IBM Plex Sans + IBM Plex Mono (already loaded globally).
   --post-accent is set by the component via inline style.
*/

.post-body {
  color: var(--color-text-primary);
  font-size: 1.0625rem; /* 17px — slightly larger than base for readability */
  line-height: 1.75;
  max-width: 72ch;
}

/* ── Paragraphs ── */
.post-body p {
  margin-bottom: 1.5rem;
}

/* ── Headings ── */
.post-body h2,
.post-body h3,
.post-body h4 {
  font-weight: 700;
  color: var(--color-text-primary);
  scroll-margin-top: 6rem; /* Clears the fixed navbar on anchor jump */
}

.post-body h2 {
  font-size: 1.5rem;
  line-height: 1.25;
  margin-top: 2.75rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--color-border);
}

.post-body h3 {
  font-size: 1.125rem;
  line-height: 1.35;
  margin-top: 2rem;
  margin-bottom: 0.75rem;
  color: var(--post-accent);
}

.post-body h4 {
  font-size: 1rem;
  margin-top: 1.5rem;
  margin-bottom: 0.5rem;
}

/* ── Code — INLINE ── */
.post-body code:not(pre code) {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.85em;
  background-color: var(--color-surface-overlay);
  border: 1px solid var(--color-border);
  border-radius: 4px;
  padding: 0.1em 0.4em;
  white-space: nowrap;
  color: var(--post-accent);
}

/* ── Code — BLOCKS (terminal aesthetic, always dark) ── */
.post-body pre {
  position: relative;
  background-color: #0d1117; /* GitHub dark — dark in both modes */
  border: 1px solid #30363d;
  border-radius: 10px;
  padding: 1.25rem 1.5rem;
  overflow-x: auto;
  margin: 1.75rem 0;
  /* Top pill showing language */
}

.post-body pre code {
  font-family: 'IBM Plex Mono', 'Menlo', monospace;
  font-size: 0.875rem;
  line-height: 1.65;
  color: #e6edf3;
  background: none;
  border: none;
  padding: 0;
  white-space: pre;
}

/* Language label in top-right corner of code blocks */
.post-body pre[class*='language-']::before,
.post-body pre:has(code[class*='language-'])::before {
  content: attr(data-lang);
  position: absolute;
  top: 0.625rem;
  right: 0.875rem;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.625rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #6e7681;
}

/* Syntax hint coloring (basic, without a full highlighter) */
.post-body pre code .comment {
  color: #6e7681;
  font-style: italic;
}
.post-body pre code .string {
  color: #a5d6ff;
}
.post-body pre code .keyword {
  color: #ff7b72;
}
.post-body pre code .function {
  color: #d2a8ff;
}
.post-body pre code .number {
  color: #79c0ff;
}

/* ── Blockquotes ── */
.post-body blockquote {
  border-left: 3px solid var(--post-accent);
  margin: 1.75rem 0;
  padding: 1rem 1.25rem;
  background-color: color-mix(in srgb, var(--post-accent) 6%, var(--color-surface));
  border-radius: 0 8px 8px 0;
}

.post-body blockquote p {
  margin-bottom: 0;
  font-style: italic;
  color: var(--color-text-secondary);
}

.post-body blockquote p:last-child {
  margin-bottom: 0;
}

/* ── Lists ── */
.post-body ul,
.post-body ol {
  padding-left: 1.5rem;
  margin-bottom: 1.5rem;
}

.post-body ul {
  list-style: none;
  padding-left: 0;
}

.post-body ul li {
  position: relative;
  padding-left: 1.5rem;
  margin-bottom: 0.4rem;
}

.post-body ul li::before {
  content: '';
  position: absolute;
  left: 0.25rem;
  top: 0.65em;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: var(--post-accent);
  opacity: 0.7;
}

.post-body ol {
  list-style: decimal;
}

.post-body ol li {
  margin-bottom: 0.4rem;
  padding-left: 0.25rem;
}

.post-body ol li::marker {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.8em;
  font-weight: 700;
  color: var(--post-accent);
}

/* ── Strong and emphasis ── */
.post-body strong {
  font-weight: 600;
  color: var(--color-text-primary);
}

.post-body em {
  color: var(--color-text-secondary);
}

/* ── Links ── */
.post-body a {
  color: var(--post-accent);
  text-decoration: underline;
  text-underline-offset: 3px;
  text-decoration-thickness: 1px;
  transition: opacity 150ms ease;
}

.post-body a:hover {
  opacity: 0.8;
}

/* ── Tables ── */
.post-body table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.75rem 0;
  font-size: 0.9rem;
}

.post-body th {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  text-align: left;
  padding: 0.625rem 0.875rem;
  background-color: var(--color-surface-raised);
  border-bottom: 2px solid var(--post-accent);
  color: var(--color-text-secondary);
}

.post-body td {
  padding: 0.625rem 0.875rem;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text-secondary);
}

.post-body tr:hover td {
  background-color: var(--color-surface-raised);
}

/* ── Horizontal rule ── */
.post-body hr {
  border: none;
  border-top: 1px solid var(--color-border);
  margin: 2.5rem 0;
}

/* ── First paragraph lead treatment ── */
.post-body > p:first-of-type {
  font-size: 1.125rem;
  color: var(--color-text-secondary);
  line-height: 1.7;
}
</style>
