<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <h2 class="text-lg font-semibold text-ink-black">My Tasks</h2>
      <router-link
        :to="{ name: 'MyTasks' }"
        class="text-sm text-ink-gray-6 hover:text-ink-gray-8 transition-colors"
      >
        View all tasks
      </router-link>
    </div>

    <div v-if="tasks.loading" class="space-y-3">
      <div
        v-for="i in 3"
        :key="i"
        class="animate-pulse border border-outline-gray-2 rounded-lg p-4"
      >
        <div class="flex items-center justify-between">
          <div class="space-y-2 flex-1">
            <div class="h-4 bg-surface-gray-2 rounded w-3/4"></div>
            <div class="h-3 bg-surface-gray-2 rounded w-1/2"></div>
          </div>
          <div class="h-6 w-16 bg-surface-gray-2 rounded-full"></div>
        </div>
      </div>
    </div>

    <div v-else-if="tasks.data?.length === 0" class="text-center py-8">
      <div class="text-ink-gray-4 mb-2">
        <LucideCheckSquare class="size-12 mx-auto" />
      </div>
      <p class="text-ink-gray-6">No tasks assigned to you</p>
    </div>

    <div v-else class="space-y-2">
      <div
        v-for="task in tasks.data?.slice(0, 5)"
        :key="task.name"
        class="group border border-outline-gray-2 rounded-lg p-4 hover:border-outline-gray-3 transition-colors cursor-pointer"
        @click="navigateToTask(task)"
      >
        <div class="flex items-start justify-between gap-3">
          <div class="flex-1 min-w-0">
            <h3 class="text-sm font-medium text-ink-black truncate group-hover:text-ink-gray-8">
              {{ task.title }}
            </h3>
            <div class="flex items-center gap-2 mt-1">
              <span
                class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
                :class="getStatusColor(task.status)"
              >
                {{ task.status }}
              </span>
              <span v-if="task.project_title" class="text-xs text-ink-gray-5">
                in {{ task.project_title }}
              </span>
              <span
                v-if="task.due_date"
                class="text-xs text-ink-gray-5"
                :class="getDueDateClass(task.due_date)"
              >
                Due {{ formatDueDate(task.due_date) }}
              </span>
            </div>
          </div>
          <div v-if="task.assigned_to" class="flex-shrink-0">
            <UserAvatar :user="task.assigned_to" size="xs" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useList } from 'frappe-ui/src/data-fetching'
import { useUser } from '@/data/users'
import UserAvatar from '@/components/UserAvatar.vue'
import { GPTask } from '@/types/doctypes'

import LucideCheckSquare from '~icons/lucide/check-square'

const router = useRouter()
const sessionUser = useUser('sessionUser')

interface TaskWithProject extends GPTask {
  project_title?: string
}

const tasks = useList<TaskWithProject>({
  doctype: 'GP Task',
  fields: [
    'name',
    'title',
    'status',
    'due_date',
    'assigned_to',
    'project',
    'project.title as project_title',
  ],
  filters: () => ({ assigned_to: sessionUser.name }),
  orderBy: 'modified desc',
  limit: 5,
  cacheKey: 'myRecentTasks',
  immediate: true,
})

const navigateToTask = (task: TaskWithProject) => {
  if (task.project) {
    router.push({
      name: 'SpaceOverview',
      params: { spaceId: task.project },
      query: { task: task.name },
    })
  }
}

const getStatusColor = (status: string) => {
  const colors = {
    Backlog: 'bg-surface-gray-2 text-ink-gray-6',
    Todo: 'bg-blue-100 text-blue-800',
    'In Progress': 'bg-yellow-100 text-yellow-800',
    Done: 'bg-green-100 text-green-800',
    Canceled: 'bg-red-100 text-red-800',
  }
  return colors[status as keyof typeof colors] || colors.Todo
}

const formatDueDate = (dateStr: string) => {
  const date = new Date(dateStr)
  const now = new Date()
  const diffTime = date.getTime() - now.getTime()
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays === 0) return 'today'
  if (diffDays === 1) return 'tomorrow'
  if (diffDays === -1) return 'yesterday'
  if (diffDays > 1) return `in ${diffDays} days`
  if (diffDays < -1) return `${Math.abs(diffDays)} days ago`
  return date.toLocaleDateString()
}

const getDueDateClass = (dateStr: string) => {
  const date = new Date(dateStr)
  const now = new Date()
  const diffTime = date.getTime() - now.getTime()
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays < 0) return 'text-red-600'
  if (diffDays === 0) return 'text-orange-600'
  return 'text-ink-gray-5'
}
</script>
