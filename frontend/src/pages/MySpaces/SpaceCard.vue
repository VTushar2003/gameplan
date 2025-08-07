<template>
  <div
    class="group relative overflow-hidden rounded-lg border border-outline-gray-2 bg-surface-white hover:border-outline-gray-3 transition-colors cursor-pointer"
    @click="navigateToSpace"
  >
    <!-- Cover Image -->
    <div
      v-if="space?.cover_image"
      class="h-20 bg-cover bg-center"
      :style="{
        backgroundImage: `url(${space.cover_image})`,
        backgroundPosition: space.cover_image_position || 'center',
      }"
    >
      <div class="h-full bg-ink-black bg-opacity-20"></div>
    </div>
    <div v-else class="h-20 bg-surface-gray-2"></div>

    <!-- Space Icon and Info -->
    <div class="p-4">
      <div class="flex items-start justify-between mb-3">
        <div class="flex items-center gap-3 flex-1 min-w-0">
          <!-- Space Icon -->
          <div class="flex-shrink-0">
            <div
              v-if="space?.icon"
              class="size-10 rounded-lg flex items-center justify-center text-lg"
              :style="{ backgroundColor: getSpaceIconColor(space.name) }"
            >
              {{ space.icon }}
            </div>
            <div
              v-else
              class="size-10 rounded-lg bg-surface-gray-3 flex items-center justify-center"
            >
              <LucideHash class="size-4 text-ink-gray-6" />
            </div>
          </div>

          <!-- Space Title and Description -->
          <div class="flex-1 min-w-0">
            <h3 class="text-base font-medium text-ink-black truncate">
              {{ space?.title }}
            </h3>
            <p v-if="space?.description" class="text-sm text-ink-gray-6 line-clamp-2 mt-1">
              {{ space.description }}
            </p>
          </div>
        </div>

        <!-- Unread Count Badge -->
        <div
          v-if="unreadCount > 0"
          class="flex-shrink-0 ml-2 bg-red-500 text-white text-xs px-2 py-1 rounded-full font-medium"
        >
          {{ unreadCount > 99 ? '99+' : unreadCount }}
        </div>
      </div>

      <!-- Member Avatars -->
      <div v-if="space?.members?.length" class="flex items-center gap-2">
        <div class="flex -space-x-1">
          <UserAvatar
            v-for="(member, index) in space.members.slice(0, 5)"
            :key="member.user"
            :user="member.user || ''"
            size="xs"
            class="ring-2 ring-surface-white"
          />
          <div
            v-if="space.members.length > 5"
            class="size-4 rounded-full bg-surface-gray-3 border-2 border-surface-white flex items-center justify-center"
          >
            <span class="text-xs font-medium text-ink-gray-6">
              +{{ space.members.length - 5 }}
            </span>
          </div>
        </div>
        <span class="text-xs text-ink-gray-5">
          {{ space.members.length === 1 ? '1 member' : `${space.members.length} members` }}
        </span>
      </div>

      <!-- Drag Handle (in customize mode) -->
      <div
        v-if="showDragHandle"
        class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity cursor-grab active:cursor-grabbing"
        @mousedown.stop
      >
        <LucideGripVertical class="size-4 text-ink-gray-4" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import UserAvatar from '@/components/UserAvatar.vue'
import { useSpace, getSpaceUnreadCount } from '@/data/spaces'
import type { Space } from '@/data/spaces'

import LucideHash from '~icons/lucide/hash'
import LucideGripVertical from '~icons/lucide/grip-vertical'

const props = defineProps<{
  spaceId: string
  showDragHandle?: boolean
}>()

const router = useRouter()
const space = useSpace(() => props.spaceId)
const unreadCount = computed(() => getSpaceUnreadCount(props.spaceId))

const navigateToSpace = () => {
  router.push({
    name: 'SpaceOverview',
    params: { spaceId: props.spaceId },
  })
}

const getSpaceIconColor = (spaceId: string) => {
  const colors = [
    '#3B82F6',
    '#EF4444',
    '#10B981',
    '#F59E0B',
    '#8B5CF6',
    '#EC4899',
    '#14B8A6',
    '#F97316',
    '#6366F1',
    '#84CC16',
  ]
  const hash = spaceId.split('').reduce((a, b) => {
    a = (a << 5) - a + b.charCodeAt(0)
    return a & a
  }, 0)
  return colors[Math.abs(hash) % colors.length]
}
</script>
