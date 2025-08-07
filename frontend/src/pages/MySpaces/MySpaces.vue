<template>
  <div>
    <!-- Header -->
    <header
      class="sticky top-0 z-10 flex items-center justify-between border-b bg-surface-white px-3 sm:px-5 py-2.5"
    >
      <Breadcrumbs class="h-7" :items="[{ label: 'My Spaces', route: { name: 'MySpaces' } }]" />
      <Button
        variant="outline"
        @click="customizeMode = !customizeMode"
        :class="{ 'bg-surface-gray-1': customizeMode }"
      >
        <template #prefix>
          <LucideSettings class="h-4 w-4" />
        </template>
        {{ customizeMode ? 'Done' : 'Customize' }}
      </Button>
    </header>

    <div class="mx-auto max-w-7xl px-3 sm:px-5 pb-20">
      <!-- My Spaces Section -->
      <div class="mt-6 mb-8">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold text-ink-black">My Spaces</h2>
          <router-link
            :to="{ name: 'Spaces' }"
            class="text-sm text-ink-gray-6 hover:text-ink-gray-8 transition-colors"
          >
            Browse all spaces
          </router-link>
        </div>

        <!-- Loading State -->
        <div
          v-if="pinnedSpaces.loading"
          class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
        >
          <div v-for="i in 6" :key="i" class="animate-pulse">
            <div class="border border-outline-gray-2 rounded-lg">
              <div class="h-20 bg-surface-gray-2 rounded-t-lg"></div>
              <div class="p-4 space-y-3">
                <div class="flex items-center gap-3">
                  <div class="size-10 bg-surface-gray-2 rounded-lg"></div>
                  <div class="flex-1 space-y-2">
                    <div class="h-4 bg-surface-gray-2 rounded w-3/4"></div>
                    <div class="h-3 bg-surface-gray-2 rounded w-1/2"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="!pinnedSpaceIds?.length" class="text-center py-12">
          <div class="text-ink-gray-4 mb-4">
            <LucidePin class="size-16 mx-auto" />
          </div>
          <h3 class="text-lg font-medium text-ink-black mb-2">No pinned spaces</h3>
          <p class="text-ink-gray-6 mb-4 max-w-md mx-auto">
            Pin your favorite spaces to have quick access to them from your homepage.
          </p>
          <router-link :to="{ name: 'Spaces' }">
            <Button variant="solid">Browse all spaces</Button>
          </router-link>
        </div>

        <!-- Pinned Spaces Grid -->
        <div v-else>
          <div
            class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
            :class="{ 'opacity-75': customizeMode }"
          >
            <div
              v-for="(spaceId, index) in pinnedSpaceIds"
              :key="spaceId"
              :draggable="customizeMode"
              @dragstart="onDragStart($event, index)"
              @dragover.prevent
              @drop="onDrop($event, index)"
              class="transition-transform"
              :class="{ 'cursor-move': customizeMode }"
            >
              <SpaceCard :spaceId="spaceId" :showDragHandle="customizeMode" />
            </div>
          </div>

          <!-- Customize Mode Info -->
          <div v-if="customizeMode" class="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <div class="flex items-start gap-3">
              <LucideInfo class="size-5 text-blue-600 mt-0.5" />
              <div>
                <p class="text-sm font-medium text-blue-800">Customize Mode</p>
                <p class="text-sm text-blue-600 mt-1">
                  Drag and drop space cards to reorder them, or use the options menu to pin/unpin
                  spaces.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- My Tasks Section -->
      <div class="border-t pt-8">
        <MyTasksSection />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { usePageMeta, Breadcrumbs, Button } from 'frappe-ui'
import { usePinnedSpaces } from '@/data/pinnedSpaces'
import SpaceCard from './SpaceCard.vue'
import MyTasksSection from './MyTasksSection.vue'

import LucideSettings from '~icons/lucide/settings'
import LucidePin from '~icons/lucide/pin'
import LucideInfo from '~icons/lucide/info'

const { pinnedSpaces, pinnedSpaceIds, reorderSpaces } = usePinnedSpaces()
const customizeMode = ref(false)
const draggedIndex = ref<number | null>(null)

const onDragStart = (event: DragEvent, index: number) => {
  draggedIndex.value = index
  if (event.dataTransfer) {
    event.dataTransfer.effectAllowed = 'move'
  }
}

const onDrop = async (event: DragEvent, dropIndex: number) => {
  event.preventDefault()

  if (draggedIndex.value === null || draggedIndex.value === dropIndex) {
    return
  }

  const newOrder = [...(pinnedSpaceIds.value || [])]
  const draggedItem = newOrder[draggedIndex.value]

  // Remove dragged item and insert at new position
  newOrder.splice(draggedIndex.value, 1)
  newOrder.splice(dropIndex, 0, draggedItem)

  // Save the new order
  try {
    await reorderSpaces(newOrder)
  } catch (error) {
    console.error('Failed to reorder spaces:', error)
  }

  draggedIndex.value = null
}

usePageMeta(() => {
  return {
    title: 'My Spaces',
  }
})
</script>
