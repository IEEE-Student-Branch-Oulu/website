<script setup lang="ts">
/**
 * Home page ( / )
 *
 * Assembles the three main home page sections:
 *   1. HeroSection      — full viewport intro with stats
 *   2. NextEventWidget  — live countdown to the next event
 *   3. LatestNewsRow    — 3 most recent blog posts
 *
 * Each section is a self-contained component.
 * Data fetching will move into each component's setup when the API is ready.
 */

definePageMeta({ layout: 'default' })

useSeoMeta({
  title: 'IEEE Oulu Student Branch',
  ogTitle: 'IEEE Oulu Student Branch',
  description:
    'The IEEE Student Branch at the University of Oulu. Workshops, tech talks, and an engineering community that ships.',
  ogDescription:
    'The IEEE Student Branch at the University of Oulu. Workshops, tech talks, and an engineering community that ships.',
})
</script>

<template>
  <div>
    <HomeHeroSection />
    <HomeNextEventWidget />
    <HomeLatestNewsRow />
  </div>
</template>
