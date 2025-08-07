<template>
  <div
    class="border px-6 pt-6 pb-2.5 rounded-xl bg-surface-white hover:bg-surface-gray-1 overflow-hidden transition-colors flex flex-col w-full"
  >
    <div class="text-left text-lg font-semibold">{{ pod.title || 'Discussions' }}</div>
    <div class="divide-y flex-1 mt-1.5" v-if="discussions.data && discussions.data.length > 0">
      <div class="py-1.5" v-for="discussion in discussions.data" :key="discussion.name">
        <div class="flex items-center gap-2">
          <UserAvatar :user="discussion.owner" size="lg" />
          <div class="flex-1 min-w-0">
            <p class="text-ink-gray-8 text-p-sm font-medium truncate">
              {{ discussion.title }}
            </p>
            <div class="text-ink-gray-7 mt-0 text-p-sm truncate flex items-center">
              <div class="text-ink-gray-5">
                <Tooltip v-if="discussion.closed_at" text="Closed">
                  <LucideLock class="size-4 p-[1px] mr-1" />
                </Tooltip>
                <Tooltip v-else-if="discussion.last_post_type == 'GP Comment'" text="Comment">
                  <LucideReply class="size-4 mr-1" />
                </Tooltip>
                <Tooltip v-else-if="discussion.last_post_type == 'GP Poll'" text="Poll">
                  <LucideAlignLeft class="size-4 p-[1px] mr-1" />
                </Tooltip>
              </div>
              {{ useUser(discussion.last_post_by).full_name.trim() }}:
              {{ discussion.last_comment_content }}
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="flex-1 flex items-center justify-center text-ink-gray-6 text-p-sm">
      No discussions yet
    </div>
  </div>
</template>
<script setup lang="ts">
import { Tooltip } from 'frappe-ui'
import UserAvatar from '@/components/UserAvatar.vue'
import { useDiscussions } from '@/data/discussions'
import { useUser } from '@/data/users'
import { GPProjectTool } from '@/types/doctypes'

const props = defineProps<{
  spaceId: string
  pod: GPProjectTool
}>()

const discussions = useDiscussions({
  filters: () => ({ project: props.spaceId, project_tool: props.pod.name }),
  limit: 5,
  cacheKey: `SpaceOverviewDiscussions-${props.spaceId}`,
  immediate: true,
  orderBy: 'last_post_at desc',
})
</script>
