import { computed, MaybeRefOrGetter, toValue } from 'vue'
import { useList } from 'frappe-ui/src/data-fetching'
import { GPPinnedProject } from '@/types/doctypes'
import { useUser } from '@/data/users'

export function usePinnedSpaces() {
  const sessionUser = useUser('sessionUser')

  const pinnedSpaces = useList<GPPinnedProject>({
    doctype: 'GP Pinned Project',
    fields: ['name', 'project', 'user', 'order'],
    filters: () => ({ user: sessionUser.name }),
    orderBy: 'order asc',
    cacheKey: 'pinnedSpaces',
    immediate: true,
  })

  const pinSpace = (spaceId: string) => {
    return pinnedSpaces.insert.submit({
      project: spaceId,
      user: sessionUser.name,
      order: (pinnedSpaces.data?.length || 0) + 1,
    })
  }

  const unpinSpace = (spaceId: string) => {
    const pinnedSpace = pinnedSpaces.data?.find((p) => p.project === spaceId)
    if (pinnedSpace) {
      return pinnedSpaces.delete.submit({ name: pinnedSpace.name })
    }
    return Promise.resolve()
  }

  const reorderSpaces = (orderedSpaceIds: string[]) => {
    const updatePromises = orderedSpaceIds
      .map((spaceId, index) => {
        const pinnedSpace = pinnedSpaces.data?.find((p) => p.project === spaceId)
        if (pinnedSpace) {
          return pinnedSpaces.setValue.submit({
            name: pinnedSpace.name,
            order: index + 1,
          })
        }
        return Promise.resolve()
      })
      .filter(Boolean)

    return Promise.all(updatePromises)
  }

  const isPinned = (spaceId: string) => {
    return pinnedSpaces.data?.some((p) => p.project === spaceId) || false
  }

  const pinnedSpaceIds = computed(() => {
    return pinnedSpaces.data?.map((p) => p.project) || []
  })

  return {
    pinnedSpaces,
    pinnedSpaceIds,
    pinSpace,
    unpinSpace,
    reorderSpaces,
    isPinned,
  }
}
