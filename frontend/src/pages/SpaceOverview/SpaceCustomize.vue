<template>
  <div class="max-w-5xl mt-10 mx-auto px-2 sm:px-5 pb-40">
    <div>
      <div class="mt-3 flex items-start justify-between gap-2">
        <div>
          <h1 class="text-xl font-semibold text-ink-gray-8">Customize this space</h1>
          <p class="text-ink-gray-6 text-p-base mt-2 max-w-[80ch]">
            Personalize your space by updating the cover image and customizing which pods are
            available. You can reorder pods by dragging, toggle their visibility, and add new ones
            to match your team's workflow.
          </p>
        </div>
        <div class="flex items-center gap-2">
          <Button @click="saveChanges" variant="solid" :loading="pods.setValue.loading">
            Save changes
          </Button>
        </div>
      </div>
    </div>

    <!-- Cover Image Section -->
    <div class="mt-5">
      <CoverImage
        class="rounded-xl"
        v-if="space"
        :imageUrl="space.cover_image"
        :imagePosition="space.cover_image_position"
        :height="200"
        :editable="true"
        @change="
          (data) => {
            spaces.setValue.submit({
              name: props.spaceId,
              cover_image: data.imageUrl || '',
              cover_image_position: data.imagePosition,
            })
          }
        "
      />
    </div>

    <div class="grid sm:grid-cols-2 gap-5 mt-5">
      <!-- Existing pods in edit mode -->
      <div
        v-for="(pod, index) in pods.data"
        :key="pod.name"
        draggable="true"
        @dragstart="handleDragStart(index, $event)"
        @dragover.prevent="handleDragOver(index, $event)"
        @drop="handleDrop(index, $event)"
        @dragend="handleDragEnd"
        class="h-80 border rounded-xl p-4 flex flex-col transition-colors cursor-move"
        :class="[
          modifiedPods.has(pod.name)
            ? 'border-blue-300 bg-blue-50'
            : 'border-outline-gray-2 hover:border-outline-gray-3',
          draggedIndex === index ? 'opacity-50' : '',
          dragOverIndex === index ? 'border-green-400 bg-green-50' : '',
        ]"
      >
        <!-- Pod Edit Card -->
        <div class="flex items-center justify-between mb-4 gap-2">
          <div class="flex items-center gap-2 flex-1">
            <!-- Drag Handle is now the entire card for better UX -->

            <input
              v-model="pod.title"
              @input="(event) => updatePodTitle(pod.name, (event.target as HTMLInputElement).value)"
              placeholder="Pod title"
              class="text-lg font-semibold bg-transparent border border-transparent text-ink-gray-8 p-0 focus:ring-0 hover:border-outline-gray-2 focus:border-outline-gray-2 rounded-sm px-0.5 py-1"
            />
          </div>

          <div class="flex items-center gap-2">
            <Switch
              :model-value="pod.enabled"
              @update:model-value="(value) => updatePodEnabled(pod.name, value)"
            />

            <Button variant="ghost" @click="deletePod(index)">
              <LucideTrash2 class="w-4 h-4 text-red-600 hover:text-red-700" />
            </Button>
          </div>
        </div>

        <!-- Pod Preview/Content -->
        <div class="flex-1 bg-surface-gray-1 rounded-lg p-3 flex items-center justify-center">
          <div class="text-center">
            <component :is="getPodIcon(pod.type)" class="size-5 text-ink-gray-5 mx-auto mb-2" />
            <p class="text-base font-medium text-ink-gray-8 mb-1">{{ pod.type }}</p>
            <p class="text-p-base text-ink-gray-5 max-w-[40ch] text-center">
              {{ getPodSummary(pod.type) }}
            </p>
          </div>
        </div>
      </div>

      <!-- Add New Pod Card -->
      <div
        @click="showAddPodDialog = true"
        class="h-80 border border-dashed border-outline-gray-3 rounded-xl flex flex-col items-center justify-center cursor-pointer hover:border-outline-gray-4 hover:bg-surface-gray-1 transition-colors group"
      >
        <!-- <LucidePlusCircle
          class="size-5 text-ink-gray-5 group-hover:text-ink-gray-6 transition-colors mb-2"
        /> -->
        <div class="flex gap-2 items-center mb-2">
          <LucideMessageSquare
            class="size-5 text-ink-gray-5 group-hover:text-ink-gray-6 transition-colors"
          />
          <LucideCheckSquare
            class="size-5 text-ink-gray-5 group-hover:text-ink-gray-6 transition-colors"
          />
          <LucideFileText
            class="size-5 text-ink-gray-5 group-hover:text-ink-gray-6 transition-colors"
          />
        </div>
        <p class="text-base font-medium text-ink-gray-8 mb-1">
          {{ pods.data?.length ? 'Add another pod' : 'Create your first pod' }}
        </p>
        <p class="text-p-base text-ink-gray-5 max-w-[40ch] text-center">
          Choose from discussions, tasks, or documents. You can have multiple pods of the same type.
        </p>
      </div>
    </div>

    <!-- Add Pod Dialog -->
    <Dialog v-model="showAddPodDialog" :options="{ title: 'Add New Pod' }">
      <template #body-content>
        <div class="space-y-4">
          <!-- Pod Type Selection -->
          <div>
            <FormLabel label="Choose Pod Type" id="pod-title" class="mb-1.5" />
            <div class="grid grid-cols-3 gap-2">
              <button
                v-for="option in podTypeOptions"
                :key="option.value"
                @click="newPod.type = option.value"
                :class="[
                  'flex gap-2 items-center p-2.5 border rounded-md cursor-pointer border-outline-gray-1 transition-all ',
                  newPod.type === option.value
                    ? 'bg-surface-gray-2 border-outline-gray-2'
                    : 'hover:border-outline-gray-2',
                ]"
              >
                <component
                  :is="getPodIcon(option.value)"
                  :class="[
                    'size-4',
                    newPod.type === option.value ? 'text-ink-gray-8' : 'text-ink-gray-5',
                  ]"
                />
                <span
                  :class="[
                    'text-base font-medium ',
                    newPod.type === option.value ? '' : 'text-ink-gray-7',
                  ]"
                >
                  {{ option.label }}
                </span>
              </button>
            </div>
          </div>

          <FormControl
            v-model="newPod.title"
            label="Pod Title"
            :placeholder="newPod.type"
            description="Choose a name that describes the functionality of your pod"
          />
        </div>
      </template>

      <template #actions>
        <div class="flex items-center justify-end">
          <Button
            variant="solid"
            @click="addNewPod"
            :disabled="!newPod.type"
            :loading="pods.insert.loading"
          >
            Add Pod to {{ space?.title }}
          </Button>
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Dialog, Switch, FormLabel, FormControl } from 'frappe-ui'
import CoverImage from '@/components/CoverImage.vue'
import { useSpace, spaces } from '@/data/spaces'
import { useSpacePods } from '@/data/spacePods'
import { GPProjectTool } from '@/types/doctypes'

import LucideMessageSquare from '~icons/lucide/message-square'
import LucideCheckSquare from '~icons/lucide/check-square'
import LucideFileText from '~icons/lucide/file-text'
import LucideTrash2 from '~icons/lucide/trash-2'

const props = defineProps<{
  spaceId: string
}>()

const router = useRouter()
const space = useSpace(() => props.spaceId)
const { pods } = useSpacePods(() => props.spaceId)

// Edit state
const showAddPodDialog = ref(false)
const modifiedPods = ref<Set<string>>(new Set()) // Track modified pod names
const originalPods = ref<Map<string, GPProjectTool>>(new Map()) // Store original pod data

// Drag and drop state
const draggedIndex = ref<number | null>(null)
const dragOverIndex = ref<number | null>(null)

const newPod = ref<{
  type: GPProjectTool['type']
  title: GPProjectTool['title']
}>({
  type: 'Discussions',
  title: '',
})

// Pod type options for Select component
const podTypeOptions: Array<{ label: string; value: GPProjectTool['type'] }> = [
  { label: 'Discussions', value: 'Discussions' },
  { label: 'Tasks', value: 'Tasks' },
  { label: 'Documents', value: 'Documents' },
  { label: 'Chats', value: 'Chats' },
]

// Pod icon mapping
const getPodIcon = (type: string) => {
  const iconMap = {
    Discussions: LucideMessageSquare,
    Tasks: LucideCheckSquare,
    Documents: LucideFileText,
    Chats: LucideMessageCircle,
  }
  return iconMap[type as keyof typeof iconMap] || 'file-text'
}

// Pod summary mapping
const getPodSummary = (type: string) => {
  const summaryMap = {
    Discussions: 'Share ideas, ask questions, and collaborate with your team',
    Tasks: 'Create, assign, and track progress on tasks and projects',
    Documents: 'Store, organize, and collaborate on documents and files',
    Chats: 'Real-time messaging and instant communication with your team',
  }
  return summaryMap[type as keyof typeof summaryMap] || 'Enhance your workspace with this pod'
}

// Initialize pods data and setup change tracking
onMounted(() => {
  if (pods.data) {
    // Store original pod data for comparison
    pods.data.forEach((pod) => {
      originalPods.value.set(pod.name, { ...pod })
    })
  }
})

// Watch for pods.data to become available and initialize original data
watch(
  () => pods.data,
  (newData) => {
    if (newData && originalPods.value.size === 0) {
      // Store original pod data for comparison
      newData.forEach((pod) => {
        originalPods.value.set(pod.name, { ...pod })
      })
    }
  },
  { immediate: true },
)

// Helper function to check if a pod has been modified
const isPodModified = (pod: GPProjectTool): boolean => {
  const original = originalPods.value.get(pod.name)
  if (!original) return false

  return (
    pod.title !== original.title || pod.enabled !== original.enabled || pod.idx !== original.idx
  )
}

// Helper function to mark a pod as modified
const markPodAsModified = (podName: string) => {
  modifiedPods.value.add(podName)
}

// Update pod title and track changes
const updatePodTitle = (podName: string, newTitle: string) => {
  const pod = pods.data?.find((p) => p.name === podName)
  if (pod) {
    pod.title = newTitle
    if (isPodModified(pod)) {
      markPodAsModified(podName)
    } else {
      modifiedPods.value.delete(podName)
    }
  }
}

// Update pod enabled state and track changes
const updatePodEnabled = (podName: string, newEnabled: boolean) => {
  const pod = pods.data?.find((p) => p.name === podName)
  if (pod) {
    pod.enabled = newEnabled ? 1 : 0
    if (isPodModified(pod)) {
      markPodAsModified(podName)
    } else {
      modifiedPods.value.delete(podName)
    }
  }
}

// Drag and drop handlers
const handleDragStart = (index: number, event: DragEvent) => {
  draggedIndex.value = index
  if (event.dataTransfer) {
    event.dataTransfer.effectAllowed = 'move'
    event.dataTransfer.setData('text/plain', index.toString())
  }
}

const handleDragOver = (index: number, event: DragEvent) => {
  event.preventDefault()
  if (event.dataTransfer) {
    event.dataTransfer.dropEffect = 'move'
  }
  dragOverIndex.value = index
}

const handleDrop = (dropIndex: number, event: DragEvent) => {
  event.preventDefault()
  const dragIndex = draggedIndex.value

  if (dragIndex !== null && dragIndex !== dropIndex && pods.data) {
    // Create a new array with reordered items
    const reorderedPods = [...pods.data]
    const draggedPod = reorderedPods[dragIndex]

    // Remove the dragged item
    reorderedPods.splice(dragIndex, 1)

    // Insert it at the new position
    reorderedPods.splice(dropIndex, 0, draggedPod)

    // Update the idx property for all pods based on new order
    reorderedPods.forEach((pod, index) => {
      const originalPod = pods.data?.find((p) => p.name === pod.name)
      if (originalPod && originalPod.idx !== index + 1) {
        originalPod.idx = index + 1
        markPodAsModified(pod.name)
      }
    })

    // Update the pods data with new order
    pods.data.splice(0, pods.data.length, ...reorderedPods)
  }

  // Reset drag state
  draggedIndex.value = null
  dragOverIndex.value = null
}

const handleDragEnd = () => {
  draggedIndex.value = null
  dragOverIndex.value = null
}

// Actions
const saveChanges = async () => {
  if (!pods.data) return

  // Get only the pods that have been modified
  const modifiedPodsList = pods.data.filter((pod) => modifiedPods.value.has(pod.name))

  if (modifiedPodsList.length === 0) {
    // No changes to save, just navigate back
    router.push({ name: 'SpaceOverview', params: { spaceId: props.spaceId } })
    return
  }

  try {
    // Save each modified pod sequentially to avoid conflicts
    for (const pod of modifiedPodsList) {
      await pods.setValue.submit({
        name: pod.name,
        title: pod.title,
        enabled: pod.enabled,
        idx: pod.idx,
      })
    }

    // Clear the modified pods set
    modifiedPods.value.clear()

    // Navigate back to space overview
    router.push({ name: 'SpaceOverview', params: { spaceId: props.spaceId } })
  } catch (error) {
    console.error('Error saving pods:', error)
  }
}

const deletePod = async (index: number) => {
  if (!pods.data?.[index]) return

  const pod = pods.data[index]

  try {
    await pods.delete.submit({ name: pod.name })
  } catch (error) {
    console.error('Error deleting pod:', error)
  }
}

const addNewPod = () => {
  if (!newPod.value.type) return

  if (!newPod.value.title) {
    newPod.value.title = newPod.value.type
  }

  return pods.insert
    .submit({
      project: props.spaceId,
      type: newPod.value.type,
      title: newPod.value.title,
    })
    .then(() => {
      newPod.value = { type: 'Discussions', title: '' }
      showAddPodDialog.value = false
    })
}
</script>
