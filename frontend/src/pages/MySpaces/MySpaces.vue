<template>
  <div>
    <!-- Header -->
    <header
      class="sticky top-0 z-10 flex items-center justify-between border-b bg-white/40 backdrop-blur-lg dark:bg-black/50 px-3 sm:px-5 py-2.5"
    >
      <Breadcrumbs class="h-7" :items="[{ label: 'Home', route: { name: 'MySpaces' } }]" />
    </header>

    <div class="mx-auto max-w-4xl px-3 sm:px-5 pb-20">
      <!-- My Spaces Section -->
      <div class="mt-6">
        <div class="flex items-start justify-between mb-4">
          <div>
            <h2 class="text-xl font-semibold">
              {{ customizeMode ? 'Customize Your Spaces' : 'My Spaces' }}
            </h2>
            <p v-if="customizeMode" class="mt-0.5 text-p-base text-ink-gray-6">
              Drag and drop space cards to reorder them
            </p>
          </div>
          <div class="flex items-center gap-2">
            <Button v-if="!customizeMode" variant="ghost" :route="{ name: 'Spaces' }">
              Browse all spaces
            </Button>

            <DropdownMoreOptions
              v-if="!customizeMode"
              :options="[{ label: 'Customize', onClick: onCustomizeClick }]"
              placement="right"
            />

            <Button
              v-if="customizeMode"
              @click="
                () => {
                  customizeMode = false
                  updatedPinnedSpaces = []
                }
              "
              >Cancel</Button
            >
            <Button
              v-if="customizeMode"
              variant="solid"
              @click="onCustomizeClick"
              :class="{ 'bg-surface-gray-1': customizeMode }"
              :loading="isReordering"
              :disabled="updatedPinnedSpaces.length === 0"
            >
              <template #prefix>
                <LucideBlocks v-if="!customizeMode && !isReordering" class="h-4 w-4" />
                <LucideSave v-if="customizeMode && !isReordering" class="h-4 w-4" />
              </template>
              {{
                isReordering ? 'Saving changes...' : customizeMode ? 'Save changes' : 'Customize'
              }}
            </Button>
          </div>
        </div>

        <!-- Loading State -->
        <div
          v-if="pinnedSpaces.loading"
          class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
        >
          <div v-for="i in 3" :key="i" class="animate-pulse">
            <div
              class="p-4 relative overflow-hidden rounded-xl shadow h-[9.5rem] bg-white/80 dark:bg-black/60"
            >
              <div class="flex flex-col h-full">
                <div class="flex items-start justify-between mb-3">
                  <div>
                    <!-- Icon placeholder -->
                    <div class="size-6 bg-surface-gray-2 rounded-lg mb-2"></div>
                    <!-- Title placeholder -->
                    <div class="h-5 bg-surface-gray-2 rounded w-24 mb-2"></div>
                    <!-- Description placeholder -->
                    <div class="space-y-0.5">
                      <div class="h-4 bg-surface-gray-2 rounded w-32"></div>
                      <div class="h-4 bg-surface-gray-2 rounded w-20"></div>
                    </div>
                  </div>
                </div>

                <!-- Member avatars placeholder at bottom -->
                <div class="flex items-center gap-2 mt-auto">
                  <div class="flex -space-x-1">
                    <div class="size-4 bg-surface-gray-2 rounded-full"></div>
                    <div class="size-4 bg-surface-gray-2 rounded-full"></div>
                    <div class="size-4 bg-surface-gray-2 rounded-full"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div
          v-else-if="pinnedSpaces.data?.length == 0 && !pinnedSpaces.loading"
          class="text-center py-12 bg-surface-gray-1 rounded-xl"
        >
          <div class="text-ink-gray-5 mb-4">
            <LucidePin class="size-6 mx-auto" />
          </div>
          <h3 class="text-base font-medium text-ink-black mb-2">No pinned spaces</h3>
          <p class="text-ink-gray-6 mb-4 max-w-md text-p-base mx-auto">
            Pin your favorite spaces to have quick access to them from your homepage.
          </p>
          <router-link :to="{ name: 'Spaces' }">
            <Button variant="solid">Browse all spaces</Button>
          </router-link>
        </div>

        <!-- Pinned Spaces Grid -->
        <div v-else-if="customizeMode">
          <DraggableGrid :items="orderedPinnedSpaces" @update:items="onSpacesReorder" />
        </div>
        <div v-else>
          <div class="grid grid-cols-2 lg:grid-cols-3 gap-4 items-stretch">
            <div
              v-for="pinnedSpace in orderedPinnedSpaces"
              :key="pinnedSpace.name"
              class="transition-transform h-full"
            >
              <SpaceCard :spaceId="pinnedSpace.project" />
            </div>
          </div>
        </div>
      </div>

      <!-- My Tasks Section -->
      <div class="pt-8">
        <MyTasksSection />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { usePageMeta, Breadcrumbs, Button } from 'frappe-ui'
import { usePinnedSpaces } from '@/data/pinnedSpaces'
import SpaceCard from './SpaceCard.vue'
import MyTasksSection from './MyTasksSection.vue'

import LucidePin from '~icons/lucide/pin'
import DraggableGrid from './DraggableGrid.vue'
import { GPPinnedProject } from '@/types/doctypes'
import DropdownMoreOptions from '@/components/DropdownMoreOptions.vue'

const { pinnedSpaces, reorderSpaces } = usePinnedSpaces()
const customizeMode = ref(false)
const isReordering = ref(false)

const orderedPinnedSpaces = computed(() => {
  return (pinnedSpaces.data || []).sort((a, b) => (a.order ?? 0) - (b.order ?? 0))
})

const updatedPinnedSpaces = ref<GPPinnedProject[]>([])

function onCustomizeClick() {
  if (isReordering.value) return
  customizeMode.value = !customizeMode.value

  if (customizeMode.value) {
    // Entering customize mode
  } else {
    // Exiting customize mode
    if (updatedPinnedSpaces.value.length > 0) {
      // If there are changes, reorder spaces
      isReordering.value = true
      reorderSpaces(
        updatedPinnedSpaces.value.map((d, i) => ({
          name: d.name,
          order: i + 1,
        })),
      ).then(() => {
        isReordering.value = false
      })
      updatedPinnedSpaces.value = []
    }
  }
}

function onSpacesReorder(reorderedPinnedSpaces: GPPinnedProject[]) {
  updatedPinnedSpaces.value = reorderedPinnedSpaces
}

usePageMeta(() => {
  return {
    title: 'Home',
  }
})
</script>
