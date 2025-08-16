<template>
  <div
    class="px-5 pt-5 border flex flex-col rounded-xl bg-surface-white hover:bg-surface-gray-1 group overflow-hidden transition-colors cursor-pointer w-full"
  >
    <div class="flex items-center justify-between mb-3">
      <div class="flex items-center gap-2">
        <LucideMessagesSquare class="size-5 text-ink-gray-6" />
        <h3 class="text-lg font-medium text-ink-gray-8">{{ pod?.title }}</h3>
      </div>
    </div>

    <!-- Recent messages preview -->
    <div class="flex-1 min-h-0 relative overflow-hidden">
      <div v-if="recentMessages.loading" class="text-sm text-ink-gray-5">Loading messages...</div>
      <div v-else-if="recentMessages.data?.length" class="space-y-3 absolute bottom-2">
        <div class="gap-2 flex flex-col justify-end max-h-64 overflow-hidden">
          <div
            v-for="message in [...(recentMessages.data || [])].reverse()"
            :key="message.name"
            class="flex items-start gap-2 flex-shrink-0"
          >
            <div class="py-1">
              <Avatar
                :image="message.user_image"
                :label="message.user_full_name || message.owner"
                size="sm"
              />
            </div>
            <div class="min-w-0 bg-surface-gray-1 p-2 rounded-lg group-hover:bg-surface-white">
              <div class="flex items-center gap-2 text-xs">
                <span class="font-medium text-ink-gray-7 truncate">
                  {{ message.user_full_name || message.owner }}
                </span>
                <span class="text-xs text-ink-gray-4">
                  {{ shortTimestamp(message.creation) }}
                </span>
              </div>
              <div
                class="text-ink-gray-6 line-clamp-1 text-p-sm"
                v-html="stripHtml(message.content)"
              ></div>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="h-full grid place-content-center text-ink-gray-5">
        <LucideMessageCircle class="size-6 mx-auto text-ink-gray-4 mb-2" />
        <p class="text-sm">No messages yet</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Avatar, dayjsLocal } from 'frappe-ui'
import { GPPod } from '@/types/doctypes'
import { useChatMessages } from '@/data/chatMessages'

import LucideMessageCircle from '~icons/lucide/message-circle'
import { shortTimestamp } from '@/utils'

const props = defineProps<{
  spaceId: string
  pod: GPPod
}>()

const recentMessages = useChatMessages({
  filters: () => ({
    project: props.spaceId,
    pod: props.pod.name,
  }),
  limit: 5,
  orderBy: 'creation desc',
  cacheKey: `chat-preview-${props.spaceId}-${props.pod.name}`,
})

function stripHtml(html: string) {
  return html.replace(/<[^>]*>/g, '')
}
</script>
