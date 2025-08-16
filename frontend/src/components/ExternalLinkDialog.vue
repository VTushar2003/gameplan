<template>
  <Dialog v-model="open" :options="{ size: '7xl' }" :disable-outside-click-to-close="true">
    <template #body>
      <div class="flex flex-col h-full">
        <div class="flex items-center justify-between p-4 border-b border-outline-gray-2">
          <div class="flex items-center space-x-3">
            <LucideExternalLink class="size-5 text-ink-gray-6" />
            <div>
              <h2 class="text-lg font-semibold text-ink-gray-8">{{ title }}</h2>
              <p class="text-sm text-ink-gray-6 truncate max-w-md">{{ url }}</p>
            </div>
          </div>
          <div class="flex items-center space-x-2">
            <Button @click="openInNewTab" variant="outline">
              <template #prefix>
                <LucideExternalLink class="size-4" />
              </template>
              Open in new tab
            </Button>
            <Button @click="close" variant="ghost">
              <LucideX class="size-4" />
            </Button>
          </div>
        </div>

        <div class="flex-1 bg-surface-gray-1 relative">
          <!-- Always render iframe for events to work -->
          <iframe
            ref="iframeRef"
            :src="url"
            class="w-full h-full border-0 min-h-[calc(80vh)]"
            @load="onIframeLoad"
            @error="onIframeError"
            sandbox="allow-same-origin allow-scripts allow-popups allow-forms allow-top-navigation"
          />

          <!-- Loading overlay -->
          <div
            v-if="loading"
            class="absolute inset-0 flex items-center justify-center bg-surface-gray-1"
          >
            <div class="flex items-center">
              <LoadingIndicator class="w-6 h-6" />
              <span class="ml-2 text-ink-gray-6">Loading...</span>
            </div>
          </div>

          <!-- Error overlay -->
          <div
            v-if="error"
            class="absolute inset-0 flex items-center justify-center bg-surface-gray-1 text-center p-8"
          >
            <div>
              <LucideAlertTriangle class="size-8 text-red-500 mx-auto mb-4" />
              <h3 class="text-lg font-medium text-ink-gray-8 mb-2">Unable to load content</h3>
              <p class="text-ink-gray-6 mb-4">This URL cannot be displayed in a frame.</p>
              <Button @click="openInNewTab" variant="solid">
                <template #prefix>
                  <LucideExternalLink class="size-4" />
                </template>
                Open in new tab instead
              </Button>
            </div>
          </div>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup lang="ts">
import { ref, watch, onUnmounted } from 'vue'
import { Dialog, Button, LoadingIndicator } from 'frappe-ui'

interface Props {
  modelValue: boolean
  url: string
  title: string
}

interface Emits {
  (e: 'update:modelValue', value: boolean): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const open = ref(props.modelValue)
const loading = ref(true)
const error = ref(false)
const iframeRef = ref<HTMLIFrameElement>()
let loadingTimeout: number | null = null

watch(
  () => props.modelValue,
  (value) => {
    open.value = value
    if (value) {
      loading.value = true
      error.value = false

      // Set a timeout to handle cases where iframe never loads
      loadingTimeout = setTimeout(() => {
        if (loading.value) {
          loading.value = false
          error.value = true
        }
      }, 10000) // 10 second timeout
    }
  },
)

watch(open, (value) => {
  emit('update:modelValue', value)
  if (!value && loadingTimeout) {
    clearTimeout(loadingTimeout)
    loadingTimeout = null
  }
})

onUnmounted(() => {
  if (loadingTimeout) {
    clearTimeout(loadingTimeout)
  }
})

function close() {
  open.value = false
}

function openInNewTab() {
  window.open(props.url, '_blank', 'noopener,noreferrer')
  close()
}

function onIframeLoad() {
  loading.value = false
  error.value = false

  if (loadingTimeout) {
    clearTimeout(loadingTimeout)
    loadingTimeout = null
  }

  // Additional check to see if the iframe actually loaded content
  setTimeout(() => {
    try {
      const iframe = iframeRef.value
      if (iframe) {
        // Try to access the iframe's content
        const doc = iframe.contentDocument || iframe.contentWindow?.document
        if (!doc || doc.location.href === 'about:blank') {
          error.value = true
        }
      }
    } catch (e) {
      // CORS error means the page loaded but we can't access it, which is fine
      // Leave error as false in this case
    }
  }, 1000)
}

function onIframeError() {
  loading.value = false
  error.value = true

  if (loadingTimeout) {
    clearTimeout(loadingTimeout)
    loadingTimeout = null
  }
}
</script>
