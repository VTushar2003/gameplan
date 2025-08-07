<template>
  <Breadcrumbs :items="breadcrumbs">
    <template #prefix="{ item }">
      <component :is="item.prefix" v-if="item.prefix" class="mr-1.5 size-4 text-ink-gray-6" />
    </template>
    <template #suffix="{ item }">
      <component :is="item.suffix" v-if="item.suffix" class="ml-1.5 size-3.5 text-ink-gray-6" />
    </template>
  </Breadcrumbs>
</template>

<script setup lang="ts">
import { type Component, computed, h } from 'vue'
import { Breadcrumbs, BreadcrumbsProps } from 'frappe-ui'
import { useSpace } from '@/data/spaces'
import LucideLock from '~icons/lucide/lock'
import { useTeam } from '@/data/teams'
import { useRoute } from 'vue-router'

const props = defineProps<{
  spaceId: string
  items?: BreadcrumbsProps['items'] & {
    suffix?: Component
    prefix?: Component
  }
}>()

const route = useRoute()
const space = useSpace(() => props.spaceId)

const breadcrumbs = computed(() => {
  let items: BreadcrumbsProps['items'] = [
    {
      label: 'Home',
      route: { name: 'Home' },
    },
  ]

  if (space.value) {
    items.push({
      label: space.value.title || space.value.name || '',
      prefix: h(
        'span',
        { class: 'grid place-items-center font-[emoji] text-lg' },
        space.value.icon,
      ),
      suffix: space.value.is_private ? LucideLock : null,
      route: { name: 'Space', params: { spaceId: props.spaceId } },
    })

    if (route.name === 'SpaceCustomize') {
      items.push({
        label: 'Customize',
        route: { name: 'SpaceCustomize', params: { spaceId: props.spaceId } },
      })
    }
  }

  if (props.items) {
    items.push(...props.items)
  }

  return items
})
</script>

<style>
button:has(span.font-\[emoji\]) {
  align-items: baseline;
}
</style>
