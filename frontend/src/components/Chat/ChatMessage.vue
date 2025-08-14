<template>
  <div class="flex group py-1 transition-colors" :class="{ 'flex-row-reverse': isOwnMessage }">
    <!-- User Avatar -->
    <div class="flex-shrink-0 py-1" :class="isOwnMessage ? 'ml-1' : 'mr-1'">
      <Avatar
        :image="message.user_image"
        :label="message.user_full_name || message.owner"
        size="md"
      />
    </div>

    <!-- Message Content -->
    <div
      class="p-2.5 rounded-lg min-w-0"
      :class="isOwnMessage ? 'bg-surface-gray-2' : 'bg-surface-gray-1'"
    >
      <!-- Header with user name and timestamp -->
      <div class="flex items-baseline gap-2 mb-1" v-if="!isOwnMessage">
        <span class="text-sm font-medium text-ink-gray-8">
          {{ message.user_full_name || message.owner }}
        </span>
        <span class="text-xs text-ink-gray-5">
          {{ shortTimestamp(message.creation) }}
        </span>
        <span v-if="message.edited_at" class="text-xs text-ink-gray-4">(edited)</span>
      </div>

      <!-- Message content -->
      <div
        class="text-sm text-ink-gray-7 prose prose-sm max-w-none"
        :class="{ 'text-right': isOwnMessage }"
      >
        <div v-html="message.content"></div>
      </div>

      <!-- Reactions (placeholder) -->
      <div
        v-if="groupedReactions.length"
        class="mt-2 flex gap-1"
        :class="{ 'justify-end': isOwnMessage }"
      >
        <span
          v-for="reaction in groupedReactions"
          :key="reaction.emoji"
          class="inline-flex items-center px-2 py-1 rounded-full bg-surface-gray-2 text-xs"
        >
          {{ reaction.emoji }} {{ reaction.count }}
        </span>
      </div>
    </div>

    <!-- Message actions (on hover) -->
    <div
      class="opacity-0 group-hover:opacity-100 transition-opacity"
      :class="isOwnMessage ? 'mr-1' : 'ml-1'"
    >
      <DropdownMoreOptions
        :placement="isOwnMessage ? 'bottom-start' : 'bottom-end'"
        :options="messageActions"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Avatar } from 'frappe-ui'
import { ChatMessage } from '@/data/chatMessages'
import DropdownMoreOptions from '../DropdownMoreOptions.vue'
import { shortTimestamp } from '@/utils'
import { session } from '@/data/session'

const props = defineProps<{
  message: ChatMessage
}>()

// Check if the message is from the current user
const isOwnMessage = computed(() => {
  return session.user === props.message.owner
})

// Group reactions by emoji and count them
const groupedReactions = computed(() => {
  if (!props.message.reactions?.length) return []

  const reactionMap = new Map<string, number>()
  props.message.reactions.forEach((reaction) => {
    const count = reactionMap.get(reaction.emoji) || 0
    reactionMap.set(reaction.emoji, count + 1)
  })

  return Array.from(reactionMap.entries()).map(([emoji, count]) => ({ emoji, count }))
})

function formatMessageTime(timestamp: string) {
  const date = new Date(timestamp)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const messageActions = computed(() => [
  {
    label: 'Reply',
    icon: 'reply',
    onClick: () => {
      // TODO: Implement reply
      console.log('Reply to message', props.message.name)
    },
  },
  {
    label: 'Edit',
    icon: 'edit',
    onClick: () => {
      // TODO: Implement edit
      console.log('Edit message', props.message.name)
    },
    condition: () => isOwnMessage.value,
  },
  {
    label: 'Delete',
    icon: 'trash-2',
    onClick: () => {
      // TODO: Implement delete
      console.log('Delete message', props.message.name)
    },
    condition: () => isOwnMessage.value,
  },
])
</script>
