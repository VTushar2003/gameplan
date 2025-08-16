<template>
  <component
    :is="customizeMode ? 'div' : 'router-link'"
    class="group block p-4 relative overflow-hidden rounded-xl shadow transition-colors h-[9.5rem]"
    :class="[
      customizeMode ? 'cursor-grab' : '',
      space?.cover_image
        ? 'bg-white/80 dark:bg-black/60 bg-blend-lighten dark:bg-blend-darken'
        : 'bg-surface-white',
    ]"
    :to="{ name: 'SpaceOverview', params: { spaceId: space?.name } }"
    :style="
      space?.cover_image
        ? {
            backgroundImage: `url(${space.cover_image})`,
            backgroundSize: 'cover',
            backgroundPosition: `center ${space?.cover_image_position || 'center'}`,
          }
        : {}
    "
  >
    <div
      v-if="space?.cover_image"
      class="absolute inset-0 bg-gradient-to-t dark:from-black/95 dark:via-black/65 dark:to-black/10 from-white/95 via-white/65 to-transparent"
    ></div>

    <div class="flex flex-col h-full isolate">
      <!-- Space Icon, Unread Count, Archived Badge -->
      <div class="flex items-center justify-between">
        <div class="text-2xl font-[emoji]">{{ space?.icon }}</div>
        <!-- Unread Count Badge -->
        <div class="mix-blend-multiply" v-if="space?.archived_at">
          <Badge>Archived</Badge>
        </div>
        <div
          v-else-if="unreadCount > 0 && !customizeMode"
          class="flex-shrink-0 ml-2 bg-orange-500 text-white text-xs h-5 px-1.5 min-w-5 grid place-content-center rounded-full font-medium"
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
      <!-- Space Title and Lock Icon -->
      <div>
        <h3 class="text-lg pt-2 font-semibold truncate text-ink-gray-8 line-clamp-1">
          {{ space?.title }}
          <LucideLock
            v-if="space?.is_private"
            class="size-3.5 text-ink-gray-6 inline ml-1 mb-0.5"
          />
        </h3>
      </div>
      <!-- Space Description -->
      <p v-if="space?.description" class="text-p-sm line-clamp-2 mt-1 text-ink-gray-5">
        {{ space.description }}
      </p>
      <!-- Member Avatars -->
      <div v-if="space?.members?.length" class="flex items-end justify-between gap-2 mt-auto">
        <HoverCard>
          <span class="text-sm text-ink-gray-5">
            {{ space?.members?.length }}
            {{ space?.members?.length === 1 ? 'member' : 'members' }}
          </span>

          <template #content>
            <div class="flex flex-wrap gap-1 max-w-[276px]">
              <div class="flex" v-for="member in space.members" :key="member.user">
                <Tooltip :text="useUser(member.user).full_name">
                  <UserAvatar :user="member.user" />
                </Tooltip>
              </div>
            </div>
          </template>
        </HoverCard>

        <div class="-mr-1 -mb-1">
          <SpaceOptions v-if="!customizeMode" :spaceId="spaceId" placement="right" />
        </div>
      </div>
    </div>
  </component>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useSpace, getSpaceUnreadCount } from '@/data/spaces'
import LucideGripVertical from '~icons/lucide/grip-vertical'
import SpaceOptions from '@/components/SpaceOptions.vue'
import { Badge, Tooltip } from 'frappe-ui'
import HoverCard from '@/components/HoverCard.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import { useUser } from '@/data/users'

const props = defineProps<{
  spaceId: string
  customizeMode?: boolean
}>()

const space = useSpace(() => props.spaceId)
const unreadCount = computed(() => getSpaceUnreadCount(props.spaceId))
</script>
