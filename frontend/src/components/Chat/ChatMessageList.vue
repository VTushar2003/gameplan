<template>
  <div class="flex flex-col h-full">
    <!-- Messages container -->
    <div ref="messagesContainer" class="flex-1 overflow-y-auto">
      <!-- Loading state -->
      <div v-if="messages.loading" class="flex items-center justify-center py-8">
        <div class="text-ink-gray-6">Loading messages...</div>
      </div>

      <!-- Messages -->
      <div v-else-if="messages.data?.length" class="space-y-0">
        <ChatMessage v-for="message in reversedMessages" :key="message.name" :message="message" />
      </div>

      <!-- Empty state -->
      <div v-else class="flex flex-col items-center justify-center py-12 text-center">
        <LucideMessageCircle class="h-12 w-12 text-ink-gray-4 mb-3" />
        <h3 class="text-lg font-medium text-ink-gray-6 mb-2">No messages yet</h3>
        <p class="text-ink-gray-5 max-w-sm">
          Start the conversation by sending the first message to your team.
        </p>
      </div>

      <!-- Load more button -->
      <div v-if="hasMoreMessages" class="px-4 py-3 border-b">
        <Button
          variant="ghost"
          class="w-full"
          @click="loadMoreMessages"
          :loading="messages.loading"
        >
          Load more messages
        </Button>
      </div>
    </div>

    <!-- Message input -->
    <div class="fixed bottom-0 right-1 sm:left-[15rem]">
      <div class="max-w-4xl mx-auto px-2 sm:px-5">
        <div class="h-8 bg-gradient-to-t from-white via-white/50 to-transparent"></div>
        <ChatMessageInput
          class="pb-5 pt-1"
          :spaceId="spaceId"
          :podId="podId"
          :pod="pod"
          :messages="messages"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, computed } from 'vue'
import { Button } from 'frappe-ui'
import { useChatMessages, ChatMessage as ChatMessageType } from '@/data/chatMessages'
import ChatMessage from './ChatMessage.vue'
import ChatMessageInput from './ChatMessageInput.vue'
import { GPPod } from '@/types/doctypes'

import LucideMessageCircle from '~icons/lucide/message-circle'

const props = defineProps<{
  spaceId: string
  podId: string
  pod?: any
}>()

const messagesContainer = ref<HTMLElement>()
const hasMoreMessages = ref(false) // TODO: Implement pagination logic

const messages = useChatMessages({
  filters: () => ({
    project: props.spaceId,
    pod: props.podId,
  }),
  limit: 50,
  orderBy: 'creation desc', // Latest first, then reverse for display
  cacheKey: `chat-${props.spaceId}-${props.podId}`,
})

// Reverse messages to show oldest first (chat style)
const reversedMessages = computed(() => {
  return messages.data ? [...messages.data].reverse() : []
})

onMounted(() => {
  scrollToBottom()
})

function scrollToBottom() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

function handleMessageSent() {
  // Reload messages and scroll to bottom
  messages.reload()
  scrollToBottom()
}

function loadMoreMessages() {
  // TODO: Implement load more functionality
  console.log('Load more messages')
}
</script>
