<template>
  <Dialog v-model="open" :options="{ size: 'lg', title: 'Add External Link' }">
    <template #body-content>
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <FormControl
            label="URL"
            v-model="newExternalUrl.doc.url"
            type="url"
            placeholder="https://example.com"
            required
            @blur="extractTitleFromUrl"
          />
        </div>

        <div>
          <FormControl
            label="Title"
            id="title"
            v-model="newExternalUrl.doc.title"
            type="text"
            placeholder="Enter a title for this link"
          />
        </div>

        <div>
          <FormControl
            label="Service (Optional)"
            v-model="newExternalUrl.doc.service"
            type="select"
            :options="[
              { value: '', label: 'Auto-detect' },
              { value: 'Figma', label: 'Figma' },
              { value: 'Google Sheets', label: 'Google Sheets' },
            ]"
          />
        </div>

        <div v-if="error" class="text-red-600 text-sm">
          {{ error }}
        </div>
      </form>
    </template>
    <template #actions>
      <div class="flex justify-end">
        <Button
          @click="handleSubmit"
          variant="solid"
          :loading="isSubmitting"
          :disabled="!newExternalUrl.doc.url || !newExternalUrl.doc.title"
        >
          Add Link
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { Dialog, Button, TextInput, FormControl } from 'frappe-ui'
import { useNewDoc } from 'frappe-ui/src/data-fetching'

// Temporary interface until types are auto-generated
interface GPExternalURL {
  name?: string
  url: string
  title: string
  service?: 'Figma' | 'Google Sheets' | ''
  project: string
  pod: string
  creation?: string
  modified?: string
}

interface Props {
  modelValue: boolean
  spaceId: string
  podId: string
}

interface Emits {
  (e: 'update:modelValue', value: boolean): void
  (e: 'success'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const open = ref(props.modelValue)
const isSubmitting = ref(false)
const error = ref('')

// Create new document handler
const newExternalUrl = useNewDoc<GPExternalURL>('GP External URL', {
  url: '',
  title: '',
  service: '',
  project: props.spaceId,
  pod: props.podId,
})

// Initialize the document with required fields
// newExternalUrl.doc = {
//   url: '',
//   title: '',
//   service: '',
//   project: props.spaceId,
//   pod: props.podId,
// }

watch(
  () => props.modelValue,
  (value) => {
    open.value = value
    if (value) {
      // Reset form when opened
      newExternalUrl.doc.url = ''
      newExternalUrl.doc.title = ''
      newExternalUrl.doc.service = ''
      newExternalUrl.doc.project = props.spaceId
      newExternalUrl.doc.pod = props.podId
      error.value = ''
    }
  },
)

watch(open, (value) => {
  emit('update:modelValue', value)
})

function close() {
  open.value = false
}

function detectServiceFromUrl(url: string): 'Figma' | 'Google Sheets' | '' {
  try {
    const urlObj = new URL(url)
    const hostname = urlObj.hostname.toLowerCase()

    if (hostname.includes('figma.com')) {
      return 'Figma'
    } else if (hostname.includes('docs.google.com') && urlObj.pathname.includes('/spreadsheets/')) {
      return 'Google Sheets'
    }

    return ''
  } catch {
    return ''
  }
}

async function extractTitleFromUrl() {
  if (!newExternalUrl.doc.url || newExternalUrl.doc.title) return

  try {
    // Auto-detect service
    if (!newExternalUrl.doc.service) {
      newExternalUrl.doc.service = detectServiceFromUrl(newExternalUrl.doc.url)
    }

    // Try to extract title from URL
    const url = new URL(newExternalUrl.doc.url)
    let title = ''

    // For common services, extract meaningful titles
    if (url.hostname.includes('figma.com')) {
      const pathParts = url.pathname.split('/')
      const fileIndex = pathParts.findIndex((part) => part === 'file')
      if (fileIndex !== -1 && pathParts[fileIndex + 2]) {
        title = pathParts[fileIndex + 2].replace(/-/g, ' ')
      }
    } else if (url.hostname.includes('docs.google.com')) {
      // Extract from URL parameter or path
      const pathParts = url.pathname.split('/')
      if (pathParts.length > 3) {
        title = 'Google Document'
      }
    }

    if (!title) {
      // Fallback to hostname
      title = url.hostname.replace('www.', '')
    }

    newExternalUrl.doc.title = title.charAt(0).toUpperCase() + title.slice(1)
  } catch {
    // Invalid URL, do nothing
  }
}

async function handleSubmit() {
  if (!newExternalUrl.doc.url || !newExternalUrl.doc.title) return

  isSubmitting.value = true
  error.value = ''

  try {
    // Auto-detect service if not set
    const service = newExternalUrl.doc.service || detectServiceFromUrl(newExternalUrl.doc.url)

    // Update service if auto-detected
    if (service) {
      newExternalUrl.doc.service = service
    }

    await newExternalUrl.submit()

    emit('success')
    close()
  } catch (err: any) {
    error.value = err.message || 'Failed to add external link'
  } finally {
    isSubmitting.value = false
  }
}
</script>
