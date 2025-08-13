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
        <Button variant="solid" @click="createNewPage">
          <template #prefix><LucidePlus class="w-4" /></template>
          <span class="whitespace-nowrap"> Add new </span>
        </Button>
      </div>
    </div>
    <PageGrid
      class="grid grid-cols-2 gap-x-5 gap-y-8 md:grid-cols-3 lg:grid-cols-4 px-3"
      :listOptions="{
        filters: { project: spaceId, pod: podId ? podId : undefined },
        orderBy: () => orderBy,
      }"
    />
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Dropdown } from 'frappe-ui'
import { useDoc, useNewDoc } from 'frappe-ui/src/data-fetching'
import PageGrid from './PageGrid.vue'
import ArrowDownUp from '~icons/lucide/arrow-up-down'
import { GPPage, GPPod } from '@/types/doctypes'
import { UseListOptions } from 'frappe-ui/src/data-fetching/useList/types'

const props = defineProps<{
  spaceId: string
  podId: string
}>()

const router = useRouter()
const orderBy: UseListOptions<GPPage>['orderBy'] = ref('modified desc')

const newPage = useNewDoc<GPPage>('GP Page', {
  project: props.spaceId,
  pod: props.podId,
  title: 'Untitled',
  content: '',
})

const pod = useDoc<GPPod>({
  doctype: 'GP Pod',
  name: () => props.podId,
})

function createNewPage() {
  newPage.submit().then((doc) => {
    router.push({
      name: 'Page',
      params: { pageId: doc.name },
    })
  })
}
</script>
<style scoped>
.sort-button:deep(.feather-minimize-2) {
  transform: rotate(15deg);
}
</style>
