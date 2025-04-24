<script setup lang="ts">
const { word, tag } = defineProps<{
  word: string;
  tag?: string;
  correct: string;
}>();

defineEmits<{
  clear: [void];
  startTagging: [void];
}>();
</script>

<template>
  <div class="tag-word">
    <span class="tag is-info is-size-3" @click="$emit('startTagging')">{{
      word
    }}</span>
    <span
      class="tag is-size-5"
      :class="[tag === correct ? 'is-success' : 'is-danger']"
      @click="$emit('clear')"
      >{{ tag }}</span
    >
  </div>
</template>

<style scoped>
.tag-word {
  display: flex;
  align-items: center;
  margin: 0.5rem;
  flex-direction: column;
  gap: 0.5rem 0.2rem;
}

.tag-word .tag:empty {
  opacity: 0;
}
</style>