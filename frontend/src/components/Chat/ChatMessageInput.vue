<template>
  <div class="bg-surface-white">
    <div class="flex gap-1 items-start">
      <div class="flex-shrink-0 py-1">
        <Avatar
          :image="useSessionUser().user_image"
          :label="useSessionUser().full_name || useSessionUser().name"
          size="md"
        />
      </div>
      <div class="flex-1" @keydown="handleKeydown">
        <TextEditor
          ref="editorRef"
          :content="messageContent"
          @change="messageContent = $event"
          :placeholder="'Type a message...'"
          :editor-class="['prose-sm max-w-none', 'min-h-12 border rounded-lg p-2.5']"
          :starterkit-options="{ heading: false }"
          :editable="true"
        />
      </div>
      <Button variant="solid" :disabled="!canSend" @click="sendMessage" :loading="isLoading">
        Send
      </Button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, computed, watch } from 'vue'
import { Button, Avatar } from 'frappe-ui'
import { useList } from 'frappe-ui/src/data-fetching'
import { GPChatMessage } from '@/types/doctypes'

import LucideSend from '~icons/lucide/send'
import { useSessionUser } from '@/data/users'
import { useChatMessages } from '@/data/chatMessages'
import TextEditor from '../TextEditor.vue'

const props = defineProps<{
  spaceId: string
  podId: string
  pod?: any
  messages: ReturnType<typeof useChatMessages>
}>()

const emit = defineEmits<{
  messageSent: [message: GPChatMessage]
}>()

const messageContent = ref('')
const isLoading = ref(false)
const editorRef = ref()

const canSend = computed(() => {
  if (!messageContent.value || isLoading.value) {
    return false
  }

  // Ensure pod exists and belongs to the correct project
  if (!props.pod?.doc || props.pod.doc.project !== props.spaceId) {
    return false
  }

  // Remove HTML tags and check if there's actual content
  const textContent = messageContent.value.replace(/<[^>]*>/g, '').trim()
  return textContent.length > 0
})

async function sendMessage() {
  if (!canSend.value) return

  // Double-check validation before sending
  if (!props.pod?.doc) {
    console.error('Pod not found:', props.podId)
    return
  }

  if (props.pod.doc.project !== props.spaceId) {
    console.error('Pod does not belong to the correct project:', {
      podProject: props.pod.doc.project,
      expectedProject: props.spaceId,
    })
    return
  }

  isLoading.value = true

  try {
    props.messages.insert
      .submit({
        content: messageContent.value,
        project: props.spaceId,
        pod: props.podId,
        message_type: 'text',
      })
      .then(async () => {
        messageContent.value = ''
        await nextTick()
        if (editorRef.value?.editor) {
          editorRef.value.editor.commands.focus()
        }
      })
  } catch (error) {
    console.error('Failed to send message:', error)
  } finally {
    isLoading.value = false
  }
}

function handleKeydown(event: KeyboardEvent) {
  // Send message on Enter (without Shift)
  if (event.key === 'Enter' && !event.shiftKey && !event.ctrlKey && !event.metaKey) {
    event.preventDefault()
    sendMessage()
  }
}
</script>
