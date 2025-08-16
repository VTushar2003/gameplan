<template>
  <div
    class="border px-6 pt-6 pb-2.5 rounded-xl bg-surface-white hover:bg-surface-gray-1 transition-colors flex flex-col overflow-hidden w-full"
  >
    <div class="flex items-center gap-2">
      <LucideFileText class="size-5 text-ink-gray-6" />
      <div class="text-left text-lg font-semibold">{{ pod.title || 'Documents' }}</div>
    </div>
    <div class="flex-1 mt-3 grid grid-cols-3 gap-3" v-if="documents.length > 0">
      <div
        class="aspect-[37/50] bg-surface-white cursor-pointer overflow-hidden rounded dark:bg-gray-900 border border-gray-50 dark:border-outline-gray-1 p-3 shadow transition-shadow"
        v-for="document in documents"
        :key="`${document.type}-${document.name}`"
        @click="handleDocumentClick(document)"
      >
        <div class="overflow-hidden text-ellipsis whitespace-nowrap">
          <article
            class="prose prose-sm pointer-events-none w-[200%] origin-top-left scale-[.55] prose-p:my-1 md:w-[250%] md:scale-[.39]"
          >
            <h1 class="flex items-center">
              {{ document.title || 'Untitled' }}
              <LucideExternalLink
                v-if="document.type === 'external_url'"
                class="ml-2 size-4 text-ink-gray-6"
              />
            </h1>
            <div
              v-if="document.type === 'page' && document.content"
              v-html="trimContent(document.content)"
            ></div>
            <div v-else-if="document.type === 'external_url'" class="text-ink-gray-6">
              <p class="text-sm">{{ document.url }}</p>
              <div
                v-if="document.service"
                class="mt-1 inline-flex items-center px-1.5 py-0.5 rounded text-xs bg-surface-gray-2"
              >
                {{ document.service }}
              </div>
            </div>
          </article>
        </div>
      </div>
    </div>
    <div v-else class="flex-1 flex items-center justify-center text-ink-gray-6 text-p-sm">
      No documents yet
    </div>

    <ExternalLinkDialog
      v-model="showExternalLinkDialog"
      :url="selectedExternalUrl"
      :title="selectedExternalTitle"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useDocuments, type DocumentItem } from '@/data/documents'
import { GPPod } from '@/types/doctypes'
import ExternalLinkDialog from '@/components/ExternalLinkDialog.vue'

const props = defineProps<{
  spaceId: string
  pod: GPPod
}>()

const router = useRouter()
const showExternalLinkDialog = ref(false)
const selectedExternalUrl = ref('')
const selectedExternalTitle = ref('')

const { documents } = useDocuments({
  filters: { project: props.spaceId, pod: props.pod.name },
  orderBy: 'modified desc',
})

function handleDocumentClick(document: DocumentItem) {
  if (document.type === 'page') {
    router.push({
      name: document.project ? 'SpacePage' : 'Page',
      params: {
        pageId: document.name,
        slug: document.slug,
        spaceId: document.project,
      },
    })
  } else if (document.type === 'external_url') {
    selectedExternalUrl.value = document.url || ''
    selectedExternalTitle.value = document.title
    showExternalLinkDialog.value = true
  }
}

// content is html content, there is no root node, but a bunch of h1, p, etc.
// for trimming we can't just slice the string, we need to extract the first few html tags and trim at the end of the fifth tag
function trimContent(content?: string): string {
  if (!content) return ''

  // Create a temporary DOM element to parse the HTML
  const tempDiv = document.createElement('div')
  tempDiv.innerHTML = content

  // Get all child elements
  const elements = Array.from(tempDiv.children)

  // Take only the first 3 elements (reduced for smaller preview)
  const trimmedElements = elements.slice(0, 3)

  // Create a new container with the trimmed elements
  const result = document.createElement('div')
  trimmedElements.forEach((el) => result.appendChild(el.cloneNode(true)))

  return result.innerHTML
}
</script>
