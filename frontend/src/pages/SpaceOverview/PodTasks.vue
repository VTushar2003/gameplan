<template>
  <div
    class="border px-6 pt-6 pb-2.5 rounded-xl bg-surface-white transition-colors hover:bg-surface-gray-1 flex flex-col w-full overflow-hidden"
  >
    <div class="flex items-center gap-2">
      <LucideClipboardList class="size-5 text-ink-gray-6" />
      <div class="text-left text-lg font-semibold">{{ pod.title || 'Tasks' }}</div>
    </div>
    <div class="divide-y flex-1 mt-1.5" v-if="tasks.data && tasks.data.length > 0">
      <div class="py-1.5" v-for="task in tasks.data" :key="task.name">
        <div class="flex items-start gap-2">
          <div class="flex-shrink-0 grid place-items-center h-5 w-5">
            <TaskStatusIcon :status="task.status" />
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-ink-gray-8 leading-5 text-p-sm font-medium truncate">
              {{ task.title }}
            </p>
            <div class="flex items-center gap-2 mt-0.5">
              <div class="text-ink-gray-7 text-p-sm flex items-center">
                <div v-if="task.assigned_to" class="flex items-center gap-1">
                  <UserAvatar :user="task.assigned_to" size="xs" />
                  <span>
                    {{ useUser(task.assigned_to).full_name }}
                  </span>
                </div>
                <div class="mx-1" v-if="task.assigned_to && task.due_date">&middot;</div>
                <div v-if="task.due_date" class="flex items-center gap-1">
                  <LucideCalendar class="text-ink-gray-5 size-3.5" />
                  {{ dayjsLocal(task.due_date).format('MMM D') }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="flex-1 flex items-center justify-center text-ink-gray-6 text-p-sm">
      No active tasks
    </div>
  </div>
</template>

<script setup lang="ts">
import TaskStatusIcon from '@/components/NewTaskDialog/TaskStatusIcon.vue'
import { useList, dayjsLocal } from 'frappe-ui'
import { GPPod, GPTask } from '@/types/doctypes'
import { activeUsers, useUser } from '@/data/users'
import UserAvatar from '@/components/UserAvatar.vue'

const props = defineProps<{
  spaceId: string
  pod: GPPod
}>()

const tasks = useList<GPTask>({
  doctype: 'GP Task',
  fields: ['name', 'title', 'status', 'assigned_to', 'due_date'],
  filters: {
    project: () => props.spaceId,
    pod: () => props.pod.name,
    status: ['in', ['Backlog', 'Todo', 'In Progress']],
  },
  limit: 7,
  cacheKey: `SpaceOverviewTasks-${props.spaceId}`,
  immediate: true,
  orderBy: 'modified desc',
})

function getAssignedUserName(userId: string) {
  const user = activeUsers.value.find((u: any) => u.name === userId)
  return user?.full_name || user?.name || userId
}

function getStatusText(status: GPTask['status']) {
  const statusMap = {
    Backlog: 'Backlog',
    Todo: 'Todo',
    'In Progress': 'In Progress',
    Done: 'Done',
    Canceled: 'Canceled',
  }
  return statusMap[status] || status
}
</script>
