<template>
  <Dialog
    :options="{
      title: 'Merge with another space',
    }"
    @after-leave="
      () => {
        selectedSpace = null
        mergePreview = null
        showConfirmation = false
      }
    "
    v-model="show"
  >
    <template #body-content>
      <!-- Step 1: Space Selection -->
      <div v-if="!showConfirmation">
        <p class="text-p-base text-ink-gray-7 mb-4">
          This will move all pods, discussions, tasks, and pages from the
          <span class="whitespace-nowrap font-semibold">{{ space?.title }}</span> space to the
          selected space. This change is irreversible!
        </p>
        <Combobox :options="spaceOptions" v-model="selectedSpace" placeholder="Select a space">
          <template #item-prefix="{ option }">
            <span class="mr-2">{{ option.icon }}</span>
          </template>
        </Combobox>
        <ErrorMessage class="mt-2" :message="spaces.runDocMethod.error" />
      </div>

      <!-- Step 2: Merge Preview & Confirmation -->
      <div v-else-if="mergePreview">
        <h3 class="text-base font-semibold text-ink-gray-8">What will happen:</h3>
        <!-- Pods Being Added with Content Counts -->
        <div class="mt-4.5">
          <h4 class="font-medium text-base text-ink-gray-8 flex items-center gap-2">
            Pods being added to "{{ mergePreview.target_project.title }}"
          </h4>
          <div class="bg-surface-gray-1 dark:bg-surface-gray-2 rounded-lg p-4 mt-2.5">
            <div class="space-y-4">
              <div
                v-for="pod in mergePreview.pods_to_add"
                :key="`${pod.type}-${pod.new_title}`"
                class="text-p-sm"
              >
                <div class="flex items-center gap-3">
                  <component :is="getPodIcon(pod.type)" class="size-4 text-ink-gray-5" />
                  <span class="text-ink-gray-9">{{ pod.new_title }}</span>
                </div>
                <div class="ml-7 mt-0.5 text-ink-gray-6">
                  {{ getContentCountForPodType(pod.type) }}
                </div>
              </div>
              <div v-if="mergePreview.pods_to_add.length === 0" class="text-ink-gray-6 text-p-sm">
                No pods to add
              </div>
            </div>
          </div>
        </div>

        <!-- Members Being Added -->
        <div class="mt-4.5">
          <h4 class="font-medium text-base text-ink-gray-8 flex items-center gap-3">
            Members being added to "{{ mergePreview.target_project.title }}"
          </h4>
          <div
            v-if="mergePreview.members_to_add.length > 0"
            class="bg-surface-gray-1 dark:bg-surface-gray-2 rounded-lg p-4 mt-2.5"
          >
            <div class="space-y-2">
              <div
                v-for="member in mergePreview.members_to_add"
                :key="member"
                class="text-p-sm text-ink-gray-7 flex items-center"
              >
                <UserAvatar :user="member" class="inline-block mr-3" size="xs" />
                <span> {{ useUser(member).full_name }} ({{ member }}) </span>
              </div>
            </div>
          </div>
        </div>
        <!-- Warning Header -->
        <div
          class="mt-7 flex items-start gap-3 p-3 bg-surface-red-1 border border-outline-red-1 rounded-lg"
        >
          <LucideAlertTriangle class="size-4 text-ink-red-4 flex-shrink-0" />
          <div>
            <h3 class="font-semibold text-sm text-ink-red-4">This action cannot be undone!</h3>
            <p class="text-p-sm text-ink-red-3 mt-1">
              Space "{{ mergePreview.source_project.title }}" will be permanently deleted after
              merging.
            </p>
          </div>
        </div>
      </div>
    </template>
    <template #actions>
      <div v-if="!showConfirmation" class="flex justify-end gap-2">
        <Button variant="outline" @click="show = false"> Cancel </Button>
        <Button
          variant="solid"
          :loading="spaces.runDocMethod.isLoading(spaceId, 'get_merge_preview')"
          :disabled="!selectedSpace"
          @click="loadMergePreview"
        >
          Preview Merge
        </Button>
      </div>

      <div v-else class="flex justify-end gap-2">
        <Button variant="outline" @click="showConfirmation = false"> Back </Button>
        <Button
          variant="solid"
          theme="red"
          :loading="spaces.runDocMethod.isLoading(spaceId, 'merge_with_project')"
          @click="confirmMerge"
        >
          Confirm Merge
        </Button>
      </div>
    </template>
  </Dialog>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Combobox } from 'frappe-ui'
import { useDoctype } from 'frappe-ui/src/data-fetching'
import { GPProject } from '@/types/doctypes'
import UserAvatar from './UserAvatar.vue'
import { useSpace, useSpaceOptions } from '@/data/spaces'
import { useUser } from '@/data/users'

import LucideMessageSquare from '~icons/lucide/message-square'
import LucideAlertTriangle from '~icons/lucide/alert-triangle'
import LucideCheckSquare from '~icons/lucide/check-square'
import LucideFileText from '~icons/lucide/file-text'
import LucideMessageCircle from '~icons/lucide/message-circle'

interface MergePreview {
  source_project: {
    name: string
    title: string
  }
  target_project: {
    name: string
    title: string
  }
  pods_to_add: Array<{
    type: string
    original_title: string
    new_title: string
    enabled: boolean
  }>
  existing_target_pods: Array<{
    type: string
    title: string
  }>
  members_to_add: string[]
  content_counts: {
    discussions: number
    tasks: number
    pages: number
    chat_messages: number
    total: number
  }
}

const props = defineProps<{
  spaceId: string
}>()

const router = useRouter()
const spaces = useDoctype<GPProject>('GP Project')
const space = useSpace(() => props.spaceId)

const selectedSpace = ref<string | null>(null)
const showConfirmation = ref(false)
const mergePreview = ref<MergePreview | null>(null)
const show = defineModel<boolean>()

const spaceOptions = useSpaceOptions({
  filterFn: (s) => s.name.toString() !== props.spaceId.toString(),
})

// Pod icon mapping
const getPodIcon = (type: string) => {
  const iconMap = {
    Discussions: LucideMessageSquare,
    Tasks: LucideCheckSquare,
    Documents: LucideFileText,
    Chats: LucideMessageCircle,
  }
  return iconMap[type as keyof typeof iconMap] || 'LucideFileText'
}

// Get content count text for a pod type
const getContentCountForPodType = (podType: string) => {
  if (!mergePreview.value) return '0 items'

  const counts = mergePreview.value.content_counts

  switch (podType) {
    case 'Discussions':
      return counts.discussions === 1 ? '1 discussion' : `${counts.discussions} discussions`
    case 'Tasks':
      return counts.tasks === 1 ? '1 task' : `${counts.tasks} tasks`
    case 'Documents':
      return counts.pages === 1 ? '1 document' : `${counts.pages} documents`
    case 'Chats':
      return counts.chat_messages === 1 ? '1 chat message' : `${counts.chat_messages} chat messages`
    default:
      return '0 items'
  }
}

function loadMergePreview() {
  if (!selectedSpace.value) return

  spaces.runDocMethod
    .submit({
      method: 'get_merge_preview',
      name: props.spaceId,
      params: {
        project: selectedSpace.value,
      },
    })
    .then((data: MergePreview) => {
      mergePreview.value = data
      showConfirmation.value = true
    })
}

function confirmMerge() {
  if (!selectedSpace.value) return

  spaces.runDocMethod
    .submit({
      method: 'merge_with_project',
      name: props.spaceId,
      params: {
        project: selectedSpace.value,
      },
      validate() {
        if (!selectedSpace.value) {
          return 'Please select a project to merge'
        }
      },
    })
    .then(() => {
      if (selectedSpace.value) {
        show.value = false
        return router.replace({
          name: 'Space',
          params: { spaceId: selectedSpace.value },
        })
      }
    })
}
</script>
