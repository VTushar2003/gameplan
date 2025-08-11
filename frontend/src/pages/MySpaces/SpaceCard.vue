<template>
  <component
    :is="customizeMode ? 'div' : 'router-link'"
    class="group block p-4 relative overflow-hidden rounded-xl shadow transition-colors h-[9.5rem] bg-white/80 dark:bg-black/60 bg-blend-lighten dark:bg-blend-darken"
    :class="[customizeMode ? 'cursor-grab' : '']"
    :to="{ name: 'SpaceOverview', params: { spaceId: space?.name } }"
    :style="{
      backgroundImage: space ? `url(${space.cover_image})` : 'none',
      backgroundSize: 'cover',
      backgroundPosition: `center ${space?.cover_image_position || 'center'}`,
    }"
  >
    <div
      v-if="space?.cover_image"
      class="absolute inset-0 bg-gradient-to-t dark:from-black/95 dark:via-black/65 dark:to-black/10 from-white/95 via-white/65 to-transparent"
    ></div>

    <!-- Space Icon and Info -->
    <div class="relative flex flex-col h-full">
      <div class="flex items-start justify-between mb-3">
        <div>
          <div class="text-2xl font-[emoji]">{{ space?.icon }}</div>
          <h3 class="text-lg pt-2 font-semibold truncate text-ink-gray-8">
            {{ space?.title }}
          </h3>
          <p v-if="space?.description" class="text-p-sm line-clamp-2 mt-1 text-ink-gray-8">
            {{ space.description }}
          </p>
        </div>

        <!-- Unread Count Badge -->
        <div
          v-if="unreadCount > 0 && !customizeMode"
          class="flex-shrink-0 ml-2 bg-orange-500 text-white text-xs size-5 grid place-content-center rounded-full font-medium"
        >
          {{ unreadCount > 99 ? '99+' : unreadCount }}
        </div>
        <!-- Drag Handle (in customize mode) -->
        <div
          v-else-if="customizeMode"
          class="absolute top-2 right-2 cursor-grab active:cursor-grabbing"
        >
          <LucideGripVertical class="size-4 text-ink-gray-6" />
        </div>
      </div>

      <!-- Member Avatars -->
      <div v-if="space?.members?.length" class="flex items-center gap-2 mt-auto">
        <div class="flex -space-x-1">
          <UserAvatarGroup :members="space.members" size="xs" :max-visible="9" />
        </div>
      </div>
    </div>
  </component>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useSpace, getSpaceUnreadCount } from '@/data/spaces'
import UserAvatarGroup from '@/components/UserAvatarGroup.vue'
import LucideGripVertical from '~icons/lucide/grip-vertical'

const props = defineProps<{
  spaceId: string
  customizeMode?: boolean
}>()

const space = useSpace(() => props.spaceId)
const unreadCount = computed(() => getSpaceUnreadCount(props.spaceId))
</script>
