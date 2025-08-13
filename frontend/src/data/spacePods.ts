import { computed, MaybeRefOrGetter } from 'vue'
import { useList } from 'frappe-ui'
import { GPPod } from '@/types/doctypes'

export function useSpacePods(spaceId: MaybeRefOrGetter<string>) {
  const pods = useList<GPPod>({
    doctype: 'GP Pod',
    fields: ['name', 'project', 'type', 'title', 'idx', 'enabled'],
    filters: { project: spaceId },
    orderBy: 'idx asc',
    cacheKey: `project-tools-${spaceId}`,
    immediate: true,
  })

  const enabledPods = computed(() => (pods.data || []).filter((tool) => tool.enabled))

  return {
    pods,
    enabledPods,
  }
}
