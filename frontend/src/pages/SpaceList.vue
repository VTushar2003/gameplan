<template>
  <PageHeader>
    <Breadcrumbs
      class="h-7"
      :items="[
        { label: 'Home', route: { name: 'Home' } },
        { label: 'All Spaces', route: { name: 'Spaces' } },
      ]"
    />
    <Button variant="solid" @click="newSpaceDialog = true">
      <template #prefix><LucidePlus class="h-4 w-4" /></template>
      Add new
    </Button>
  </PageHeader>
  <NewSpaceDialog v-model="newSpaceDialog" />
  <div class="mx-auto max-w-4xl px-2 sm:px-5 pb-20 sm:pb-80">
    <div class="mt-6 px-2.5">
      <h1 class="text-xl font-semibold">Spaces</h1>
      <p class="text-p-base text-ink-gray-6 mt-1 max-w-[60ch]">
        Spaces keep discussions, tasks, and files in one place. Use them for a team, project or any
        topic. Spaces you join will show up on your sidebar.
      </p>
    </div>
    <div class="mt-3 mb-3 flex px-2.5 items-center justify-between gap-2.5">
      <TextInput
        ref="searchInput"
        v-model="query"
        :placeholder="`Search ${$platform == 'mac' ? '⌘F' : 'Ctrl+F'}`"
        class="w-full"
        @blur="handleSearchBlur"
        v-focus
      >
        <template #prefix>
          <LucideSearch class="size-4 text-ink-gray-5" />
        </template>
      </TextInput>
      <div class="shrink-0">
        <Tooltip text="Filter by space visibility">
          <Select v-model="currentTab" :options="['Public', 'Private', 'Archived']" />
        </Tooltip>
      </div>
      <TabButtons :buttons="[{ label: 'Grid' }, { label: 'List' }]" v-model="currentView" />
    </div>
    <div class="p-3" v-if="filteredSpaces.length === 0">
      <EmptyStateBox>
        <div class="text-ink-gray-5 text-base">No spaces</div>
      </EmptyStateBox>
    </div>
    <div class="px-3">
      <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-3" v-if="currentView === 'Grid'">
        <SpaceCard v-for="space in filteredSpaces" :key="space.name" :spaceId="space.name" />
      </div>
      <div class="flex flex-col divide-y" v-else-if="currentView === 'List'">
        <div v-for="space in filteredSpaces" :key="space.name" class="">
          <SpaceListItem :spaceId="space.name" />
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { Breadcrumbs, TabButtons, Button, Tooltip, Select, TextInput } from 'frappe-ui'
import { useDoctype } from 'frappe-ui/src/data-fetching'
import { spaces as allSpaces, joinedSpaces, Space } from '@/data/spaces'
import NewSpaceDialog from '@/components/NewSpaceDialog.vue'
import PageHeader from '@/components/PageHeader.vue'
import { GPProject } from '@/types/doctypes'
import EmptyStateBox from '@/components/EmptyStateBox.vue'
import { vFocus } from '@/directives'
import SpaceCard from './MySpaces/SpaceCard.vue'
import SpaceListItem from './MySpaces/SpaceListItem.vue'

const currentTab = ref('Public')
const currentView = ref('Grid')
const query = ref('')
const newSpaceDialog = ref(false)
const searchInput = ref()
const searchWasFocused = ref(false)

let spaces = useDoctype<GPProject>('GP Project')

// Handle Cmd+F / Ctrl+F keyboard shortcut
const handleKeydown = (event: KeyboardEvent) => {
  if ((event.metaKey || event.ctrlKey) && event.key === 'f') {
    // Check if search input is currently focused
    const isSearchFocused = document.activeElement === searchInput.value?.el

    if (!isSearchFocused || !searchWasFocused.value) {
      // First time or search not focused - prevent default and focus search
      event.preventDefault()
      event.stopPropagation()
      searchInput.value?.el?.focus()
      searchWasFocused.value = true
    } else {
      // Search was already focused - allow browser default search
      searchWasFocused.value = false
    }
  }
}

// Reset the flag when search input loses focus
const handleSearchBlur = () => {
  searchWasFocused.value = false
}

onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})

// Filtered spaces based on current tab and search query
const filteredSpaces = computed(() => {
  return (allSpaces.data || []).filter((space: Space) => {
    const matchesVisibility = Boolean(
      {
        Public: !space.archived_at,
        Private: space.is_private,
        Archived: space.archived_at,
      }[currentTab.value],
    )

    const matchesQuery = query.value
      ? space.title.toLowerCase().includes(query.value.toLowerCase())
      : true

    return matchesVisibility && matchesQuery
  })
})
</script>
