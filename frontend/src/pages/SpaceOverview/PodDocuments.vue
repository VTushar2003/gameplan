<template>
  <div
    class="border px-6 pt-6 pb-2.5 rounded-xl bg-surface-white hover:bg-surface-gray-1 transition-colors flex flex-col overflow-hidden w-full"
  >
    <div class="text-left text-lg font-semibold">{{ pod.title || 'Documents' }}</div>
    <div class="flex-1 mt-3 grid grid-cols-3 gap-3" v-if="pages.data && pages.data.length > 0">
      <div
        class="aspect-[37/50] bg-surface-white cursor-pointer overflow-hidden rounded dark:bg-gray-900 border border-gray-50 dark:border-outline-gray-1 p-3 shadow transition-shadow"
        v-for="page in pages.data"
        :key="page.name"
      >
        <div class="overflow-hidden text-ellipsis whitespace-nowrap">
          <article
            class="prose prose-sm pointer-events-none w-[200%] origin-top-left scale-[.55] prose-p:my-1 md:w-[250%] md:scale-[.39]"
          >
            <h1>{{ page.title || 'Untitled' }}</h1>
            <div v-html="trimContent(page.content)"></div>
          </article>
        </div>
      </div>
    </div>
    <div v-else class="flex-1 flex items-center justify-center text-ink-gray-6 text-p-sm">
      No documents yet
    </div>
  </div>
</template>

<script setup lang="ts">
import { useList, dayjsLocal } from 'frappe-ui'
import { GPPage, GPProjectTool } from '@/types/doctypes'
import { useUser } from '@/data/users'
import UserAvatar from '@/components/UserAvatar.vue'

const props = defineProps<{
  spaceId: string
  pod: GPProjectTool
}>()

const pages = useList<GPPage>({
  doctype: 'GP Page',
  filters: () => ({ project: props.spaceId, project_tool: props.pod.name }),
  fields: ['name', 'title', 'content', 'modified', 'owner'],
  limit: 5,
  cacheKey: `SpaceOverviewPages-${props.spaceId}`,
  immediate: true,
  orderBy: 'modified desc',
})

// content is html content, there is no root node, but a bunch of h1, p, etc.
// for trimming we can't just slice the string, we need to extract the first few html tags and trim at the end of the fifth tag
function trimContent(content?: string): string {
  if (!content) return ''

  // Create a temporary DOM element to parse the HTML
  const tempDiv = document.createElement('div')
  tempDiv.innerHTML = content

  // Get all child elements
  const elements = Array.from(tempDiv.children)

  // Take only the first 5 elements
  const trimmedElements = elements.slice(0, 5)

  // Create a new container with the trimmed elements
  const result = document.createElement('div')
  trimmedElements.forEach((el) => result.appendChild(el.cloneNode(true)))

  return result.innerHTML
}
</script>
