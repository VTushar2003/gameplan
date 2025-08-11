<template>
  <div>
    <!-- easing function created from https://pqina.nl/blog/css-spring-animation-with-linear-easing-function/ -->
    <draggable
      v-model="items"
      group="people"
      :force-fallback="false"
      ghost-class="sortable-ghost"
      chosen-class="sortable-chosen"
      drag-class="sortable-drag"
      :animation="458"
      easing="linear(0.00, -0.00768, 0.0279, 0.0884, 0.161, 0.238, 0.315, 0.389, 0.457, 0.520, 0.577, 0.628, 0.673, 0.714, 0.749, 0.781, 0.808, 0.833, 0.853, 0.872, 0.888, 0.903, 0.915, 0.926, 0.935, 0.943, 0.951, 0.957, 0.962, 0.967, 0.972, 0.975, 0.978, 0.981, 0.984, 0.986, 0.988, 0.989, 0.991, 0.992, 0.993, 0.994, 0.995, 0.995, 0.996, 0.996, 0.997, 0.997, 0.998, 0.998, 0.998, 0.998, 0.999, 0.999, 0.999, 0.999, 1.00)"
      @start="dragStart"
      @end="dragEnd"
      item-key="name"
      ref="gridContainer"
      class="flex flex-wrap gap-4"
    >
      <template #item="{ element }">
        <div
          class="select-none cursor-grab"
          :class="{ 'cursor-grabbing': isDragging }"
          :style="{ width: cardWidth + 'px' }"
        >
          <SpaceCard :space-id="element.project" :customize-mode="true" />
        </div>
      </template>
    </draggable>
  </div>
</template>
<script setup lang="ts">
import draggable from 'vuedraggable'
import { computed, onMounted, ref, useTemplateRef, watch } from 'vue'
import { useElementSize } from '@vueuse/core'
import SpaceCard from './SpaceCard.vue'
import { GPPinnedProject } from '@/types/doctypes'

const props = defineProps<{
  items: GPPinnedProject[]
}>()

const emits = defineEmits<{
  (e: 'update:items', value: GPPinnedProject[]): void
}>()

const isDragging = ref(false)

const container = useTemplateRef<HTMLElement | null>('gridContainer')
const containerSize = useElementSize(container)

const cardWidth = computed(() => {
  let columns = 3
  let gap = 16
  return (containerSize.width.value - gap * (columns - 1)) / columns
})

const items = ref<GPPinnedProject[]>([])

onMounted(() => {
  items.value = props.items.slice()
})

function dragStart() {
  document.body.classList.add('cursor-grabbing')
  isDragging.value = true
}

function dragEnd() {
  document.body.classList.remove('cursor-grabbing')
  isDragging.value = false

  emits('update:items', items.value)
}
</script>
<style scoped>
:deep(.sortable-chosen) {
  opacity: 1;
  transform: scale(1.05);
  cursor: grabbing;
}
</style>
