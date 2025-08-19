import { useCall, useDoctype } from 'frappe-ui'
import { GPProject } from '@/types/doctypes'

interface ProjectUnreadCount {
  [spaceId: string]: number
}

const unreadCountByProject = useCall<ProjectUnreadCount>({
  url: '/api/v2/method/GP Project/get_unread_count_v2',
  immediate: true,
  cacheKey: 'unreadCountByProject',
})

export function getProjectUnreadCount(spaceId: string) {
  return unreadCountByProject.data?.[spaceId] ?? 0
}

const Project = useDoctype<GPProject>('GP Project')

export function markSpaceAsRead(spaceId: string) {
  return Project.runDocMethod
    .submit({
      name: spaceId,
      method: 'mark_all_as_read',
    })
    .then(() => {
      return unreadCountByProject.reload()
    })
}

export function markSpacesAsRead(spaceIds: string[]) {
  return Project.runMethod
    .submit({
      method: 'mark_all_as_read',
      params: {
        spaces: spaceIds,
      },
    })
    .then(() => {
      return unreadCountByProject.reload()
    })
}
