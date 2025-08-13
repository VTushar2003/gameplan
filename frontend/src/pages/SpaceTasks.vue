<template>
  <div class="mt-5 mx-auto max-w-4xl px-2 sm:px-5">
    <div class="mb-4 px-3 flex items-center justify-between">
      <h1 class="text-xl font-semibold text-ink-gray-8">{{ pod.doc?.title }}</h1>
      <div class="flex items-stretch space-x-2">
        <Button variant="solid" @click="openNewTaskDialog">
          <template #prefix>
            <LucidePlus class="h-4 w-4" />
          </template>
          Add new
        </Button>
      </div>
    </div>
    <div class="px-3">
      <TaskList :listOptions="{ filters }" :groupByStatus="true" ref="taskList" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useTemplateRef } from 'vue'
import { useUser } from '@/data/users'
import TaskList from '@/components/TaskList.vue'
import { showNewTaskDialog } from '@/components/NewTaskDialog'
import { useDoc } from 'frappe-ui'
import { GPPod } from '@/types/doctypes'

const props = defineProps<{
  spaceId: string
  podId: string
}>()

const taskList = useTemplateRef<typeof TaskList>('taskList')

const filters = () => ({
  project: props.spaceId,
  pod: props.podId,
})

const pod = useDoc<GPPod>({
  doctype: 'GP Pod',
  name: () => props.podId,
})

function openNewTaskDialog() {
  showNewTaskDialog({
    defaults: {
      project: props.spaceId,
      pod: props.podId,
      assigned_to: useUser('sessionUser').name,
    },
    onSuccess: () => {
      taskList.value?.tasks.reload()
    },
  })
}
</script>
