<template>
  <div class="min-h-[3rem] overflow-hidden bg-surface-gray-2">
    <div
      ref="groupContainer"
      class="group relative w-full"
      :style="{ height: `${height}px` }"
      v-if="validatedImageUrl"
    >
      <img
        class="w-full object-cover"
        :style="{ height: `${height}px`, objectPosition }"
        :class="{ 'animate-pulse': loading }"
        :src="validatedImageUrl"
        @load="loading = false"
      />
      <div
        class="absolute inset-0 flex cursor-grab select-none items-center justify-center"
        v-if="reposition"
        @mousedown="startReposition"
      >
        <div class="text-center">
          <div class="rounded-md bg-black/50 px-3 py-2 text-base text-ink-white backdrop-blur-sm">
            Drag up/down to reposition image
          </div>
          <Button class="mt-2" @click="savePosition"> Save position </Button>
          <Button class="ml-2 mt-2" @click="cancelReposition">Cancel</Button>
        </div>
      </div>
      <div
        class="absolute bottom-0 left-1/2 mb-4 flex -translate-x-1/2 space-x-2 opacity-0 transition-opacity focus-within:opacity-100 group-hover:opacity-100"
        v-if="!reposition"
      >
        <UnsplashImageBrowser v-if="editable" @select="handleImageSelect">
          <template v-slot="{ togglePopover }">
            <Button variant="outline" @click="togglePopover()"> Change Image </Button>
          </template>
        </UnsplashImageBrowser>
        <Button v-if="editable" variant="outline" @click="startRepositionMode"> Reposition </Button>
      </div>
    </div>
    <div
      v-else
      class="flex w-full items-center justify-center bg-surface-menu-bar text-sm text-ink-gray-4"
      :style="{ height: `${height}px` }"
    >
      <UnsplashImageBrowser v-if="editable" @select="handleImageSelect">
        <template v-slot="{ togglePopover }">
          <Button variant="outline" @click="togglePopover()"> Click to set cover image </Button>
        </template>
      </UnsplashImageBrowser>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted, useTemplateRef } from 'vue'
// @ts-ignore
import UnsplashImageBrowser from '@/components/UnsplashImageBrowser.vue'
import { getImgDimensions } from '@/utils'

interface Props {
  imageUrl?: string | null
  imagePosition?: number
  editable?: boolean
  height?: number
}

const props = withDefaults(defineProps<Props>(), {
  imageUrl: null,
  imagePosition: 0,
  editable: false,
  height: 130,
})

const emit = defineEmits<{
  change: [{ imageUrl: string | null; imagePosition: number }]
  'update:imageUrl': [string | null]
  'update:imagePosition': [number]
}>()

const groupContainer = useTemplateRef('groupContainer')

// Reactive state
const reposition = ref(false)
const tempImagePosition = ref<number | null>(null)
const loading = ref(true)
const initialY = ref<number | null>(null)
const changeY = ref<number>(0)
const imageDimensions = ref<any>(null)

// Computed properties
// Add responsive parameters to Unsplash images for better performance
const validatedImageUrl = computed(() => {
  if (!props.imageUrl) return null
  if (props.imageUrl.startsWith('https://images.unsplash.com')) {
    let width = window.innerWidth || 768
    return props.imageUrl + `&w=${width}&fit=crop&crop=entropy,faces,focalpoint`
  }
  return props.imageUrl
})

const objectPosition = computed(() => {
  const position = reposition.value ? tempImagePosition.value : props.imagePosition
  return `center ${(position ?? 0) + changeY.value}%`
})

// Mouse event handlers
let onMouseMove: (e: MouseEvent) => void
let onMouseUp: () => void

onMounted(() => {
  onMouseMove = (e: MouseEvent) => {
    if (!reposition.value) return
    if (initialY.value && imageDimensions.value) {
      let ratio = imageDimensions.value.ratio
      let containerWidth = groupContainer.value?.clientWidth || window.innerWidth
      let imageHeight = containerWidth / ratio
      let diff = initialY.value - e.clientY
      changeY.value = (diff * 100) / imageHeight

      // Clamp position to 0-100%
      let finalPosition = (tempImagePosition.value ?? 0) + changeY.value
      if (finalPosition > 100) {
        changeY.value = 100 - (tempImagePosition.value ?? 0)
      }
      if (finalPosition < 0) {
        changeY.value = -(tempImagePosition.value ?? 0)
      }
    }
  }

  onMouseUp = () => {
    if (!reposition.value) return
    const position = tempImagePosition.value
    if (position === null) return

    initialY.value = null
    tempImagePosition.value = position + changeY.value
    changeY.value = 0
  }

  window.addEventListener('mousemove', onMouseMove)
  window.addEventListener('mouseup', onMouseUp)
})

onUnmounted(() => {
  window.removeEventListener('mousemove', onMouseMove)
  window.removeEventListener('mouseup', onMouseUp)
})

// Watch for image URL changes and fetch dimensions
watch(
  () => validatedImageUrl.value,
  async (newVal, oldVal) => {
    if (newVal !== oldVal && newVal) {
      imageDimensions.value = await getImgDimensions(newVal)
    }
  },
  { immediate: true },
)

// Methods
const startReposition = (event: MouseEvent) => {
  initialY.value = event.clientY
}

const savePosition = () => {
  const position = tempImagePosition.value
  if (position === null) return

  emit('update:imagePosition', position)
  emit('change', { imageUrl: props.imageUrl, imagePosition: position })
  reposition.value = false
  tempImagePosition.value = null
}

const cancelReposition = () => {
  reposition.value = false
}

const startRepositionMode = () => {
  reposition.value = true
  tempImagePosition.value = props.imagePosition
}

const handleImageSelect = (imageUrl: string) => {
  loading.value = true
  imageDimensions.value = null
  emit('update:imageUrl', imageUrl)
  emit('change', { imageUrl, imagePosition: props.imagePosition })
}
</script>
