<template>
  <div>
    <EmptyStateBox class="col-span-4" v-if="documents.length === 0">
      <LucideCoffee class="h-7 w-7 text-ink-gray-4" />
      No documents
    </EmptyStateBox>
    <div class="relative" v-for="d in documents" :key="`${d.type}-${d.name}`">
      <div @click="handleDocumentClick(d)" class="cursor-pointer">
        <section class="group">
          <div
            class="aspect-[37/50] cursor-pointer overflow-hidden rounded-md dark:bg-gray-900 border border-gray-50 dark:border-outline-gray-1 p-3 shadow-lg transition-shadow hover:shadow-xl"
          >
            <div class="overflow-hidden text-ellipsis whitespace-nowrap">
              <div
                class="prose prose-sm pointer-events-none w-[200%] origin-top-left scale-[.55] prose-p:my-1 md:w-[250%] md:scale-[.39]"
              >
                <h1 class="text-3xl font-semibold text-ink-gray-8 flex items-center">
                  {{ d.title }}
                  <LucideExternalLink
                    v-if="d.type === 'external_url'"
                    class="ml-2 size-6 text-ink-gray-6"
                  />
                </h1>
                <div v-if="d.type === 'page' && d.content" v-html="d.content"></div>
                <div v-else-if="d.type === 'external_url'" class="text-ink-gray-6">
                  <p class="text-base">{{ d.url }}</p>
                  <div
                    v-if="d.service"
                    class="mt-2 inline-flex items-center px-2 py-1 rounded-full bg-surface-gray-2 text-xs"
                  >
                    {{ d.service }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
      <Dropdown :options="getDropdownOptions(d)" placement="bottom-end">
        <template #default>
          <Button
            class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity"
            variant="ghost"
            size="sm"
          >
            <LucideMoreVertical class="size-4" />
          </Button>
        </template>
      </Dropdown>
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
import { Dropdown } from 'frappe-ui'
import { useDocuments, type DocumentItem } from '@/data/documents'
import EmptyStateBox from '@/components/EmptyStateBox.vue'
import ExternalLinkDialog from '@/components/ExternalLinkDialog.vue'
import { createDialog } from '@/utils/dialogs'
import { UseListOptions } from 'frappe-ui/src/data-fetching/useList/types'
import type { GPPage } from '@/types/doctypes'

const props = defineProps<{
  listOptions: {
    filters: {
      project?: string
      pod?: string
    }
    orderBy?: 'title asc' | 'modified desc' | 'creation desc'
  }
}>()

const router = useRouter()
const showExternalLinkDialog = ref(false)
const selectedExternalUrl = ref('')
const selectedExternalTitle = ref('')

const { documents, pages, externalUrls } = useDocuments({
  filters: props.listOptions.filters,
  orderBy: props.listOptions.orderBy,
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

function getDropdownOptions(document: DocumentItem) {
  return [
    {
      label: 'Delete',
      icon: 'trash',
      onClick: () => {
        createDialog({
          title: `Delete ${document.type === 'page' ? 'Page' : 'External Link'}`,
          message: `Are you sure you want to delete this ${
            document.type === 'page' ? 'page' : 'external link'
          }?`,
          actions: [
            {
              label: 'Delete',
              onClick: ({ close }) => {
                close()
                if (document.type === 'page') {
                  return pages.delete.submit({ name: document.name })
                } else {
                  return externalUrls.delete.submit({ name: document.name })
                }
              },
              variant: 'solid',
              theme: 'red',
            },
          ],
        })
      },
    },
  ]
}
</script>
