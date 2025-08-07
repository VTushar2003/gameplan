<template>
  <div class="max-w-4xl mt-5 mx-auto px-2 sm:px-5">
    <div class="flex px-3 mb-4 items-center justify-between">
      <h1 class="text-xl font-semibold text-ink-gray-8">{{ pod.doc?.title }}</h1>
      <Button
        variant="solid"
        :route="{ name: 'NewDiscussion', query: { spaceId: spaceId, podId: podId } }"
      >
        <template #prefix><LucidePlus class="h-4 w-4" /></template>
        Add new
      </Button>
    </div>
    <DiscussionList
      :filters="() => ({ project: spaceId, project_tool: podId ? podId : undefined })"
      :cacheKey="`SpaceDiscussions-${spaceId}-${podId}`"
    />
  </div>
</template>
<script setup lang="ts">
import DiscussionList from '@/components/DiscussionList.vue'
import { GPProjectTool } from '@/types/doctypes'
import { useDoc } from 'frappe-ui'

const props = defineProps<{
  spaceId: string
  podId: string
}>()

const pod = useDoc<GPProjectTool>({
  doctype: 'GP Project Tool',
  name: () => props.podId,
})
</script>
