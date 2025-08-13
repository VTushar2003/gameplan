<template>
  <HoverCardRoot v-model:open="cardOpen">
    <HoverCardTrigger asChild>
      <slot />
    </HoverCardTrigger>
    <HoverCardPortal>
      <HoverCardContent side="top">
        <HoverCardArrow class="fill-surface-white" />
        <div class="bg-surface-white p-3 rounded-lg shadow-2xl">
          <slot name="content" />
        </div>
      </HoverCardContent>
    </HoverCardPortal>
  </HoverCardRoot>
</template>

<script setup lang="ts">
import {
  HoverCardRoot,
  HoverCardPortal,
  HoverCardTrigger,
  HoverCardContent,
  HoverCardArrow,
} from 'reka-ui'
import { ref } from 'vue'

defineOptions({
  inheritAttrs: false,
})

const cardOpen = ref(false)
</script>
