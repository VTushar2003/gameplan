<template>
  <router-link
    class="group flex items-center px-3 -mx-3 py-2 h-15 relative overflow-hidden rounded-lg bg-surface-white hover:bg-surface-gray-1 transition-colors"
    :to="{ name: 'SpaceOverview', params: { spaceId: space?.name } }"
  >
    <div class="flex items-center gap-4 w-full">
      <!-- Space Icon -->
      <div class="flex-shrink-0 flex items-center justify-center">
        <div v-if="space?.archived_at" class="text-ink-gray-6">
          <LucideFolderArchive class="size-6" />
        </div>
        <div v-else class="text-2xl font-[emoji]">{{ space?.icon }}</div>
      </div>

      <!-- Space Info -->
      <div class="flex-grow min-w-0">
        <div class="flex items-center gap-2 mb-1">
          <h3 class="text-base font-semibold truncate text-ink-gray-8">
            {{ space?.title }}
          </h3>
          <LucideLock v-if="space?.is_private" class="size-4 text-ink-gray-6 flex-shrink-0" />
          <!-- Unread Count Badge -->
          <div
            v-if="unreadCount > 0"
            class="flex-shrink-0 bg-orange-500 text-white text-xs px-1.5 py-0.5 rounded-full font-medium"
          >
            {{ unreadCount > 99 ? '99+' : unreadCount }}
          </div>
        </div>
        <p v-if="space?.description" class="mt-1.5 text-base text-ink-gray-5 line-clamp-1">
          {{ space.description }}
        </p>
      </div>

      <!-- Member Avatars and Options -->
      <div class="flex items-center gap-3 flex-shrink-0">
        <span class="text-sm text-ink-gray-5"
          >{{ space?.members?.length }}
          {{ space?.members?.length === 1 ? 'member' : 'members' }}</span
        >
        <SpaceOptions :spaceId="spaceId" placement="right" />
      </div>
    </div>
  </router-link>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useSpace, getSpaceUnreadCount } from '@/data/spaces'
import UserAvatarGroup from '@/components/UserAvatarGroup.vue'
import SpaceOptions from '@/components/SpaceOptions.vue'

const props = defineProps<{
  spaceId: string
}>()

const space = useSpace(() => props.spaceId)
const unreadCount = computed(() => getSpaceUnreadCount(props.spaceId))
</script>
