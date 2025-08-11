import { useBulkUpdate, useList } from 'frappe-ui/src/data-fetching'
import { GPPinnedProject } from '@/types/doctypes'

export function usePinnedSpaces() {
  const pinnedSpaces = useList<GPPinnedProject>({
    doctype: 'GP Pinned Project',
    fields: ['name', 'project', 'user', 'order'],
    orderBy: 'order asc',
    cacheKey: 'pinnedSpaces',
    immediate: true,
  })

  const pinSpace = (spaceId: string) => {
    return pinnedSpaces.insert.submit({
      project: spaceId,
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

  const isPinned = (spaceId: string) => {
    return pinnedSpaces.data?.some((p) => p.project === spaceId) || false
  }

  type UpdatedPinnedSpace = Pick<GPPinnedProject, 'name' | 'order'>

  const _reorderSpaces = useBulkUpdate()
  const reorderSpaces = (updatedPinnedSpaces: UpdatedPinnedSpace[]) => {
    // optimistic update
    for (let pinnedSpace of updatedPinnedSpaces) {
      pinnedSpaces.updateRow({
        name: pinnedSpace.name,
        order: pinnedSpace.order,
      })
    }

    let docs = updatedPinnedSpaces.map((pinnedSpace) => ({
      ...pinnedSpace,
      doctype: 'GP Pinned Project',
    }))

    return _reorderSpaces.submit(docs)
  }

  return {
    pinnedSpaces,
    pinSpace,
    unpinSpace,
    reorderSpaces,
    isPinned,
  }
}
