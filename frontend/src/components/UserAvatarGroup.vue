<template>
  <div class="flex pl-1 isolate">
    <!-- Display visible avatars -->
    <UserAvatar
      class="-ml-1"
      v-for="member in visibleMembers"
      :key="member.user"
      :user="member.user || ''"
      :size="size"
    />

    <!-- Show overflow indicator if there are more members -->
    <div
      v-if="overflowCount > 0"
      class="-ml-1 flex items-center justify-center rounded-full border-2 bg-surface-gray-3 font-medium text-ink-gray-7 z-[1]"
      :class="avatarSizeClasses"
    >
      +{{ overflowCount }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import UserAvatar from '@/components/UserAvatar.vue'
import { AvatarProps } from 'frappe-ui'

interface Member {
  user?: string
}

interface Props {
  members: Member[]
  maxVisible?: number
  size?: AvatarProps['size']
}

const props = withDefaults(defineProps<Props>(), {
  maxVisible: 9,
  size: 'md',
})

const visibleMembers = computed(() => {
  return props.members.slice(0, props.maxVisible)
})

const overflowCount = computed(() => {
  return Math.max(0, props.members.length - props.maxVisible)
})

const avatarSizeClasses = computed(() => {
  const sizeMap = {
    xs: 'h-4 w-4 text-2xs',
    sm: 'h-5 w-5 text-2xs',
    md: 'h-6 w-6 text-2xs',
    lg: 'h-7 w-7 text-sm',
    xl: 'h-8 w-8 text-base',
    '2xl': 'h-10 w-10 text-lg',
    '3xl': 'h-11.5 w-11.5 text-xl',
  }
  return sizeMap[props.size] || sizeMap.md
})
</script>
