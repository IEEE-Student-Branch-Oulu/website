<script setup lang="ts">
/**
 * BlogCategoryBadge
 *
 * Renders a styled category pill using the CATEGORY_META color system.
 * Wraps UiBaseBadge for consistent badge structure (font, spacing, border-radius),
 * applying category-specific colors via CATEGORY_META.badgeClass.
 *
 * Uses:
 *   - UiBaseBadge for the base pill styling (mono font, uppercase tracking, sizing)
 *
 * Props:
 *   category - PostCategory key
 *   size     - 'sm' | 'md'
 *
 * Usage:
 *   <BlogCategoryBadge category="tutorial" />
 */
import { CATEGORY_META, type PostCategory } from '~/composables/useBlog'

interface Props {
  category: PostCategory
  size?: 'sm' | 'md'
}

withDefaults(defineProps<Props>(), { size: 'sm' })
</script>

<template>
  <UiBaseBadge :size="size" :class="CATEGORY_META[category].badgeClass">
    {{ CATEGORY_META[category].label }}
  </UiBaseBadge>
</template>
