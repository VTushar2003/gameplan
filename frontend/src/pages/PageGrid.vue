<template>
  <div>
    <EmptyStateBox class="col-span-4" v-if="pages.data?.length === 0">
      <LucideCoffee class="h-7 w-7 text-ink-gray-4" />
      No pages
    </EmptyStateBox>
    <div class="relative" v-for="d in pages.data" :key="d.name">
      <router-link
        :to="{
          name: d.project ? 'SpacePage' : 'Page',
          params: {
            pageId: d.name,
            slug: d.slug,
            spaceId: d.project,
          },
        }"
      >
        <section class="group">
          <div
            class="aspect-[37/50] cursor-pointer overflow-hidden rounded-md dark:bg-gray-900 border border-gray-50 dark:border-outline-gray-1 p-3 shadow-lg transition-shadow hover:shadow-xl"
          >
            <div class="overflow-hidden text-ellipsis whitespace-nowrap">
              <div
                class="prose prose-sm pointer-events-none w-[200%] origin-top-left scale-[.55] prose-p:my-1 md:w-[250%] md:scale-[.39]"
              >
                <h1 class="text-3xl font-semibold text-ink-gray-8">{{ d.title }}</h1>
                <div v-html="d.content"></div>
              </div>
            </div>
          </div>
        </section>
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Dropdown } from 'frappe-ui'
import { useList } from 'frappe-ui/src/data-fetching'
import EmptyStateBox from '@/components/EmptyStateBox.vue'
import { createDialog } from '@/utils/dialogs'
import { UseListOptions } from 'frappe-ui/src/data-fetching/useList/types'
import { GPPage } from '@/types/doctypes'
import { useSpace } from '@/data/spaces'

const props = defineProps<{
  listOptions: {
    filters: UseListOptions<GPPage>['filters']
    orderBy?: UseListOptions<GPPage>['orderBy']
  }
}>()

interface Page
  extends Pick<
    GPPage,
    'name' | 'creation' | 'title' | 'content' | 'slug' | 'project' | 'team' | 'modified'
  > {}

const pages = useList<Page>({
  doctype: 'GP Page',
  fields: ['name', 'creation', 'title', 'content', 'slug', 'project', 'team', 'modified'],
  filters: props.listOptions.filters,
  orderBy: props.listOptions.orderBy,
  cacheKey: ['Pages', props.listOptions],
})

function getSpace(page: Page) {
  return useSpace(() => page.project).value
}

const getDropdownOptions = (page: Page) => [
  {
    label: 'Delete',
    icon: 'trash',
    onClick: () => {
      createDialog({
        title: 'Delete Page',
        message: 'Are you sure you want to delete this page?',
        actions: [
          {
            label: 'Delete',
            onClick: ({ close }) => {
              close()
              return pages.delete.submit({ name: page.name })
            },
            variant: 'solid',
            theme: 'red',
          },
        ],
      })
    },
  },
]
</script>
