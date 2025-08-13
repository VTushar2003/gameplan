<template>
  <ScrollAreaViewport
    class="inline-flex h-full flex-1 flex-col overflow-y-auto border-r bg-surface-menu-bar pb-40 w-60"
  >
    <div class="flex flex-col px-2 py-2">
      <UserDropdown />
    </div>
    <div class="flex-1">
      <nav class="space-y-0.5 px-2">
        <AppSidebarLink
          v-for="link in navigation"
          :key="link.name"
          :to="link.route"
          :isActive="link.isActive"
        >
          <template #prefix>
            <component :is="link.icon" class="h-4 w-4 text-ink-gray-6" />
          </template>
          {{ link.name }}
          <template #suffix>
            <span v-if="link.count" class="block text-xs text-ink-gray-5">
              {{ link.count }}
            </span>
            <span v-if="link.name === 'Search'">
              <span class="text-sm text-ink-gray-4">
                <template v-if="$platform === 'mac'">⌘K</template>
                <template v-else>Ctrl+K</template>
              </span>
            </span>
          </template>
        </AppSidebarLink>
      </nav>
      <div class="mt-6 flex items-center justify-between px-2">
        <h3 class="px-2 py-1.5 text-sm text-ink-gray-5">Spaces</h3>
        <div class="space-x-1 flex items-center">
          <DropdownMoreOptions
            placement="right"
            :options="[
              {
                label: 'Browse all spaces',
                icon: LucideLayoutGrid,
                onClick: () => $router.push({ name: 'Spaces' }),
              },
              {
                label: 'Configure sidebar',
                icon: LucideSettings2,
                onClick: () => (showSidebarConfigureDialog = true),
              },
            ]"
          />
        </div>
      </div>
      <nav class="mt-1 space-y-0.5 px-2">
        <AppLink
          v-for="space in spacesList"
          :key="space.name"
          :to="{ name: 'Space', params: { spaceId: space.name } }"
          class="flex h-7 items-center rounded px-2 text-ink-gray-7 transition"
          activeClass="bg-surface-selected shadow-sm"
          inactiveClass="hover:bg-surface-gray-2"
        >
          <span class="inline-flex min-w-0 items-center w-full">
            <span class="flex-shrink-0 flex h-5 w-6 items-center justify-center text-xl">
              {{ space.icon }}
            </span>
            <span class="truncate text-sm flex-grow w-full ml-2">
              {{ space.title }}
            </span>
            <LucideLock v-if="space.is_private" class="flex-shrink-0 h-3 w-3 ml-2" />
            <span
              v-if="getSpaceUnreadCount(space.name) > 0"
              class="ml-auto pl-2 text-xs text-ink-gray-5"
            >
              {{ getSpaceUnreadCount(space.name) }}
            </span>
          </span>
        </AppLink>
        <div
          class="flex h-7 items-center px-2 text-sm text-ink-gray-5"
          v-if="spacesList.length === 0"
        >
          No spaces
        </div>
      </nav>
    </div>
    <Dialog :options="{ title: 'Configure Sidebar' }" v-model="showSidebarConfigureDialog">
      <template #body-content>
        <FormControl
          label="Show spaces"
          :type="'select'"
          v-model="sidebarSpaceFilter"
          :options="[
            { label: 'Only joined spaces', value: 'joined' },
            { label: 'All spaces', value: 'all' },
          ]"
        />
        <div class="mt-3 text-sm text-ink-gray-6">
          <p v-if="sidebarSpaceFilter === 'joined'">
            Only spaces you have joined will appear in the sidebar.
          </p>
          <p v-else>All spaces will appear in the sidebar.</p>
        </div>
      </template>
      <template #actions>
        <div class="flex justify-end">
          <Button variant="solid" @click="showSidebarConfigureDialog = false"> Done </Button>
        </div>
      </template>
    </Dialog>
  </ScrollAreaViewport>
  <ScrollBar />
</template>
<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useLocalStorage } from '@vueuse/core'
import { Dialog, FormControl, Button } from 'frappe-ui'
import { unreadNotifications } from '@/data/notifications'
import { spaces, joinedSpaces, getSpaceUnreadCount } from '@/data/spaces'
import { useSessionUser } from '@/data/users'
import AppLink from './AppLink.vue'
import UserDropdown from './UserDropdown.vue'
import { ScrollAreaViewport } from 'reka-ui'
import ScrollBar from './ScrollBar.vue'

import LucideFiles from '~icons/lucide/files'
import LucideInbox from '~icons/lucide/inbox'
import LucideListTodo from '~icons/lucide/list-todo'
import LucideNewspaper from '~icons/lucide/newspaper'
import LucideUsers2 from '~icons/lucide/users-2'
import LucideSearch from '~icons/lucide/search'
import LucideHome from '~icons/lucide/home'
import LucideUserPlus from '~icons/lucide/user-plus'
import LucideLayoutGrid from '~icons/lucide/layout-grid'
import LucideSettings2 from '~icons/lucide/settings-2'

const showSidebarConfigureDialog = ref(false)
const sidebarSpaceFilter = useLocalStorage<'all' | 'joined'>('sidebar-space-filter', 'joined')

const route = useRoute()
const sessionUser = useSessionUser()

// List of spaces based on the selected filter
const spacesList = computed(() => {
  const filteredSpaces = (spaces.data || []).filter((space) => !space.archived_at)

  if (sidebarSpaceFilter.value === 'joined') {
    return filteredSpaces.filter((space) => joinedSpaces.data?.includes(space.name))
  }

  return filteredSpaces
})

const navigation = computed(() => {
  return [
    {
      name: 'Home',
      icon: LucideHome,
      route: {
        name: 'MySpaces',
      },
      isActive: testRoute(/MySpaces/g),
    },
    {
      name: 'Inbox',
      icon: LucideInbox,
      route: {
        name: 'Notifications',
      },
      count: unreadNotifications.data || 0,
      isActive: testRoute(/Notifications/g),
    },
    {
      name: 'Discussions',
      icon: LucideNewspaper,
      route: {
        name: 'Discussions',
      },
      isActive: testRoute(/Discussions/g),
    },
    {
      name: 'Tasks',
      icon: LucideListTodo,
      route: {
        name: 'MyTasks',
      },
      isActive: testRoute(/MyTasks|Task/g),
    },
    {
      name: 'Pages',
      icon: LucideFiles,
      route: {
        name: 'MyPages',
      },
      isActive: testRoute(/MyPages|Page/g),
    },
    {
      name: 'People',
      icon: LucideUsers2,
      route: {
        name: 'People',
      },
      isActive: testRoute(/People|PersonProfile/g),
      condition: () => sessionUser.isNotGuest,
    },
    {
      name: 'Search',
      icon: LucideSearch,
      route: {
        name: 'Search',
      },
      isActive: testRoute(/Search/g),
    },
  ].filter((nav) => (nav.condition ? nav.condition() : true))
})

function testRoute(regex: RegExp) {
  return route.name ? regex.test(route.name.toString()) : false
}
</script>
