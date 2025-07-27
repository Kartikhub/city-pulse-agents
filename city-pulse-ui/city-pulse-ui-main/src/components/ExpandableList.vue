<template>
  <div class="relative rounded-lg"
       :class="{ 'cursor-pointer': showExpandButton || isExpanded }"
       @click="toggleExpand">
    <div ref="listContentRef" :class="{ 'max-h-[150px]': !isExpanded, 'overflow-hidden': !isExpanded }">
      <ul class="list-disc list-inside text-customText">
        <slot></slot>
      </ul>
    </div>
    <div v-if="!isExpanded && showExpandButton" class="absolute bottom-0 left-0 right-0 h-8 bg-gradient-to-t from-customBackground to-transparent"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUpdated, nextTick, defineEmits, watch } from 'vue'

const emit = defineEmits(['update:isExpanded'])

const isExpanded = ref(false)
const showExpandButton = ref(false)
const listContentRef = ref(null) // Ref is now on the inner div

const checkOverflow = () => {
  if (listContentRef.value) {
    const scrollHeight = listContentRef.value.scrollHeight
    const clientHeight = listContentRef.value.clientHeight
    console.log('scrollHeight:', scrollHeight, 'clientHeight:', clientHeight)
    showExpandButton.value = scrollHeight > clientHeight
  }
}

const toggleExpand = () => {
  // Always toggle isExpanded when clicked
  isExpanded.value = !isExpanded.value
}

watch(isExpanded, (newValue) => {
  emit('update:isExpanded', newValue)
  // Re-check overflow after expansion/collapse to update showExpandButton correctly
  nextTick(() => {
    checkOverflow()
  })
})

onMounted(() => {
  checkOverflow()
})

onUpdated(() => {
  // Re-check overflow if content changes after initial mount
  nextTick(() => {
    checkOverflow()
  })
})
</script>
