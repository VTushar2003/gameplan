<template>
  <div class="flex group py-1 transition-colors">
    <!-- User Avatar -->
    <div class="flex-shrink-0 mr-1 py-1">
      <Avatar
        :image="message.user_image"
        :label="message.user_full_name || message.owner"
        size="md"
      />
    </div>

    <!-- Message Content -->
    <div class="p-2.5 rounded-lg min-w-0 bg-surface-gray-1">
      <!-- Header with user name and timestamp -->
      <div class="flex items-baseline gap-2 mb-1">
        <span class="text-sm font-medium text-ink-gray-8">
          {{ message.user_full_name || message.owner }}
        </span>
        <span class="text-xs text-ink-gray-5">
          {{ shortTimestamp(message.creation) }}
        </span>
        <span v-if="message.edited_at" class="text-xs text-ink-gray-4">(edited)</span>
      </div>

      <!-- Message content -->
      <div class="text-sm text-ink-gray-7 prose prose-sm max-w-none">
        <div v-html="message.content"></div>
      </div>

      <!-- Reactions (placeholder) -->
      <div v-if="message.reactions?.length" class="mt-2 flex gap-1">
        <span
          v-for="reaction in message.reactions"
          :key="reaction.name"
          class="inline-flex items-center px-2 py-1 rounded-full bg-surface-gray-2 text-xs"
        >
          {{ reaction.emoji }} {{ reaction.count }}
        </span>
      </div>
    </div>

    <!-- Message actions (on hover) -->
    <div class="opacity-0 group-hover:opacity-100 transition-opacity ml-1">
      <DropdownMoreOptions placement="bottom-end" :options="messageActions" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Avatar } from 'frappe-ui'
import { ChatMessage } from '@/data/chatMessages'
import DropdownMoreOptions from '../DropdownMoreOptions.vue'
import { shortTimestamp } from '@/utils'

const props = defineProps<{
  message: ChatMessage
}>()

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
    condition: () => true, // TODO: Check if user owns the message
  },
  {
    label: 'Delete',
    icon: 'trash-2',
    onClick: () => {
      // TODO: Implement delete
      console.log('Delete message', props.message.name)
    },
    condition: () => true, // TODO: Check if user owns the message
  },
])
</script>
