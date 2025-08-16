<template>
  <div class="mt-5 mx-auto max-w-4xl px-2 sm:px-5">
    <div class="flex px-3 mb-4 items-center justify-between">
      <h1 class="text-xl font-semibold text-ink-gray-8">{{ pod.doc?.title }}</h1>
      <div class="flex items-center space-x-2">
        <Dropdown
          :options="[
            {
              label: 'Alphabetical',
              onClick: () => (orderBy = 'title asc'),
            },
            {
              label: 'Last updated',
              onClick: () => (orderBy = 'modified desc'),
            },
            {
              label: 'Created',
              onClick: () => (orderBy = 'creation desc'),
            },
          ]"
          placement="right"
        >
          <template #default>
            <Button>
              <template #prefix>
                <ArrowDownUp class="mr-1.5 h-4 w-4 leading-none" :stroke-width="1.5" />
              </template>
              {{
                orderBy === 'title asc'
                  ? 'Alphabetical'
                  : orderBy === 'modified desc'
                    ? 'Last updated'
                    : 'Created'
              }}
            </Button>
          </template>
        </Dropdown>
        <Dropdown
          :options="[
            {
              label: 'Add Page',
              icon: 'file-text',
              onClick: createNewPage,
            },
            {
              label: 'Add External Link',
              icon: 'external-link',
              onClick: () => (showAddExternalLinkModal = true),
            },
          ]"
          placement="bottom-end"
        >
          <template #default>
            <Button variant="solid">
              <template #prefix><LucidePlus class="w-4" /></template>
              <span class="whitespace-nowrap"> Add new </span>
              <template #suffix><LucideChevronDown class="w-4 ml-1" /></template>
            </Button>
          </template>
        </Dropdown>
      </div>
    </div>
    <PageGrid
      class="grid grid-cols-2 gap-x-5 gap-y-8 md:grid-cols-3 lg:grid-cols-4 px-3"
      :listOptions="{
        filters: { project: spaceId, pod: podId ? podId : undefined },
        orderBy: orderBy,
      }"
    />

    <AddExternalLinkModal
      v-model="showAddExternalLinkModal"
      :spaceId="spaceId"
      :podId="podId"
      @success="onExternalLinkAdded"
    />
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Dropdown } from 'frappe-ui'
import { useDoc, useNewDoc } from 'frappe-ui/src/data-fetching'
import PageGrid from './PageGrid.vue'
import AddExternalLinkModal from '@/components/AddExternalLinkModal.vue'
import ArrowDownUp from '~icons/lucide/arrow-up-down'
import { GPPage, GPPod } from '@/types/doctypes'

const props = defineProps<{
  spaceId: string
  podId: string
}>()

const router = useRouter()
const orderBy = ref<'title asc' | 'modified desc' | 'creation desc'>('modified desc')
const showAddExternalLinkModal = ref(false)

const newPage = useNewDoc<GPPage>('GP Page')

const pod = useDoc<GPPod>({
  doctype: 'GP Pod',
  name: () => props.podId,
})

function createNewPage() {
  newPage.doc = {
    project: props.spaceId,
    pod: props.podId,
    title: 'Untitled',
    content: '',
  }

  newPage.submit().then((doc) => {
    router.push({
      name: 'Page',
      params: { pageId: doc.name },
    })
  })
}

function onExternalLinkAdded() {
  // The PageGrid will automatically refresh its data
  // since it uses the documents composable which handles caching
}
</script>
<style scoped>
.sort-button:deep(.feather-minimize-2) {
  transform: rotate(15deg);
}
</style>
