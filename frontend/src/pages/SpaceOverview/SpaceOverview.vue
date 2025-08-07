<template>
  <div class="max-w-5xl mt-5 mx-auto px-2 pb-40 sm:px-5">
    <!-- Cover Image Section or Gray Background -->
    <div class="relative rounded-xl overflow-hidden mb-5">
      <div class="h-[200px] relative">
        <!-- Cover image or gray background -->
        <div v-if="space?.cover_image" class="h-full w-full">
          <img
            :src="space.cover_image"
            :style="{ objectPosition: `center ${space.cover_image_position || 50}%` }"
            class="h-full w-full object-cover"
            alt="Space cover"
          />
          <!-- Gradient overlay for text contrast -->
          <div
            class="absolute inset-0 bg-gradient-to-t from-black/75 via-black/45 to-transparent"
          ></div>
        </div>
        <div v-else class="h-full w-full border rounded-xl bg-surface-gray-1"></div>

        <!-- Space title and icon overlay -->
        <div class="absolute bottom-0 left-0 p-6 w-full">
          <div class="flex items-end gap-3 w-full">
            <div class="flex-1">
              <div class="text-[28px] font-[emoji]">{{ space?.icon }}</div>
              <div class="flex items-center mt-1 gap-3">
                <h1
                  class="text-2xl font-bold"
                  :class="space?.cover_image ? 'text-white' : 'text-ink-gray-9'"
                >
                  {{ space?.title }}
                </h1>
              </div>
              <p
                v-if="space?.description"
                class="text-p-base mt-2 max-w-[60ch]"
                :class="space?.cover_image ? 'text-white/90' : 'text-ink-gray-7'"
              >
                {{ space.description }}
              </p>
              <div class="flex mt-3 items-center gap-2">
                <UserAvatarGroup :members="space?.members || []" :maxVisible="9" size="md" />
              </div>
            </div>
            <div class="flex items-center gap-2">
              <div :data-theme="space?.cover_image ? 'dark' : 'light'">
                <SpaceOptions :spaceId="spaceId" placement="right" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="grid sm:grid-cols-2 gap-5 mt-5">
      <template v-for="pod in enabledPods" :key="pod.name">
        <!-- Discussion Pods -->
        <router-link
          v-if="pod.type === 'Discussions'"
          class="flex h-[18.5rem]"
          :to="{ name: 'SpaceDiscussions', params: { spaceId: spaceId, podId: pod.name } }"
        >
          <PodDiscussions :spaceId="spaceId" :pod />
        </router-link>

        <!-- Task Pods -->
        <router-link
          v-else-if="pod.type === 'Tasks'"
          class="flex h-[18.5rem]"
          :to="{ name: 'SpaceTasks', params: { spaceId: spaceId, podId: pod.name } }"
        >
          <PodTasks :spaceId="spaceId" :pod />
        </router-link>

        <!-- Document Pods -->
        <router-link
          v-else-if="pod.type === 'Documents'"
          class="flex h-[18.5rem]"
          :to="{ name: 'SpacePages', params: { spaceId: spaceId, podId: pod.name } }"
        >
          <PodDocuments :spaceId="spaceId" :pod />
        </router-link>
      </template>

      <!-- Fallback message when no pods are enabled -->
      <div
        v-if="!enabledPods.length"
        class="col-span-2 text-center py-8 text-ink-gray-6 border rounded-xl"
      >
        <LucideLayoutPanelTop class="size-6 mx-auto text-ink-gray-6" />
        <p class="text-p-base text-ink-gray-7 max-w-[50ch] mx-auto mt-2.5">
          No pods are enabled for this space yet. Create some discussions, tasks, or documents to
          get started.
        </p>

        <Button class="mt-3" :route="{ name: 'SpaceCustomize' }">Add pods</Button>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import UserAvatarGroup from '@/components/UserAvatarGroup.vue'
import { useSpace } from '@/data/spaces'
import { useSpacePods } from '@/data/spacePods'
import PodDiscussions from './PodDiscussions.vue'
import PodTasks from './PodTasks.vue'
import PodDocuments from './PodDocuments.vue'
import SpaceOptions from '@/components/SpaceOptions.vue'

const props = defineProps<{
  spaceId: string
}>()

const space = useSpace(() => props.spaceId)
const { enabledPods } = useSpacePods(() => props.spaceId)
</script>
