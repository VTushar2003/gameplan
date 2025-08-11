<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <h2 class="text-xl font-semibold">My Tasks</h2>
      <Button variant="ghost" :route="{ name: 'MyTasks' }"> View all tasks </Button>
    </div>

    <TaskList :listOptions="{ filters, pageLength: 999 }" :groupByStatus="true" />
  </div>
</template>

<script setup lang="ts">
import { useUser } from '@/data/users'
import TaskList from '@/components/TaskList.vue'

const sessionUser = useUser('sessionUser')

const filters = () => ({
  assigned_or_owner: sessionUser.name,
  status: ['in', ['Todo', 'In Progress', 'Backlog']],
})
</script>
