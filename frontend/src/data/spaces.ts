import { computed, MaybeRefOrGetter, toValue } from 'vue'
import { useCall, useList } from 'frappe-ui/src/data-fetching'
import { GPProject, GPMember } from '@/types/doctypes'

interface Member extends Pick<GPMember, 'user'> {}

export interface Space
  extends Pick<
    GPProject,
    | 'name'
    | 'title'
    | 'description'
    | 'icon'
    | 'team'
    | 'archived_at'
    | 'is_private'
    | 'modified'
    | 'tasks_count'
    | 'discussions_count'
    | 'cover_image'
    | 'cover_image_position'
  > {
  members: Member[]
}

export let spaces = useList<Space>({
  doctype: 'GP Project',
  fields: [
    'name',
    'title',
    'description',
    'icon',
    'team',
    'archived_at',
    'is_private',
    'modified',
    'tasks_count',
    'discussions_count',
    'cover_image',
    'cover_image_position',
    { members: ['user'] },
  ],
  initialData: [],
  orderBy: 'title asc',
  limit: 99999,
  cacheKey: 'spaces',
  transform(data) {
    for (let space of data) {
      space.name = space.name.toString()
    }
    return data
  },
  immediate: true,
  onSuccess() {
    unreadCount.submit()
  },
})

export function useSpace(name: MaybeRefOrGetter<string | undefined>) {
  return computed(() => {
    let _name = toValue(name)
    if (!_name) return null
    return spaces.data?.find((space) => space.name.toString() === _name?.toString()) ?? null
  })
}

export const joinedSpaces = useCall<string[]>({
  url: '/api/v2/method/GP Project/get_joined_spaces',
  cacheKey: 'joinedSpaces',
  initialData: [],
})

export function hasJoined(spaceId: MaybeRefOrGetter<string>) {
  return joinedSpaces.data?.includes(toValue(spaceId))
}

export const unreadCount = useCall<{ [spaceId: number]: number }>({
  url: '/api/v2/method/GP Project/get_unread_count',
  immediate: false,
  cacheKey: 'unreadCount',
})

export function getSpaceUnreadCount(spaceId: string) {
  let spaceIdInt = parseInt(spaceId)
  return unreadCount.data?.[spaceIdInt] ?? 0
}

export function useSpaceOptions({
  filterFn = (_p: Space) => true,
}: { filterFn?: (space: Space) => boolean } = {}) {
  return computed(() => {
    return (spaces.data || []).filter(filterFn).map((space) => ({
      label: space.title + (space.archived_at ? ' (Archived)' : ''),
      value: space.name,
      icon: space.icon,
    }))
  })
}
