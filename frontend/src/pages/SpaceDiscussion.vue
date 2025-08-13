<template>
  <PageHeader>
    <SpaceBreadcrumbs
      :spaceId="spaceId"
      :items="[
        {
          label: discussion.doc?.pod_title || 'Discussions',
          route: {
            name: 'SpaceDiscussions',
            params: { spaceId: spaceId, podId: discussion.doc?.pod },
          },
        },
      ]"
    />
  </PageHeader>
  <div class="flex" v-if="space">
    <DiscussionView
      class="w-full"
      :postId="postId"
      :read-only-mode="Boolean(space?.archived_at) || $readOnlyMode"
    />
  </div>
</template>

<script setup lang="ts">
import SpaceBreadcrumbs from '@/components/SpaceBreadcrumbs.vue'
import DiscussionView from '@/components/DiscussionView.vue'
import PageHeader from '@/components/PageHeader.vue'
import { useDiscussion } from '@/data/discussions'
import { useSpace } from '@/data/spaces'

interface Props {
  spaceId: string
  postId: string
  slug?: string
}

const props = defineProps<Props>()
const space = useSpace(() => props.spaceId)
const discussion = useDiscussion(() => props.postId)
</script>
