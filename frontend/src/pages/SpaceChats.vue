<template>
  <div class="max-w-4xl mt-5 mx-auto px-2 sm:px-5">
    <div class="flex flex-col h-full">
      <!-- Chat header -->
      <h1 class="text-xl font-semibold text-ink-gray-8">{{ pod.doc?.title || 'Chats' }}</h1>

      <!-- Chat messages area -->
      <div class="flex-1 mt-4 min-h-0">
        <ChatMessageList :spaceId="spaceId" :podId="podId" :pod="pod" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useDoc } from 'frappe-ui'
import { GPPod } from '@/types/doctypes'
import ChatMessageList from '@/components/Chat/ChatMessageList.vue'

const props = defineProps<{
  spaceId: string
  podId: string
}>()

const pod = useDoc<GPPod>({
  doctype: 'GP Pod',
  name: () => props.podId,
})
</script>
