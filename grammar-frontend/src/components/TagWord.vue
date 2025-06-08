<script setup lang="ts">
const { word, tag, isTagged } = defineProps<{
  word: string;
  tag?: string;
  isTagged: boolean;
}>();

defineEmits<{
  clear: [void];
  startTagging: [void];
}>();
</script>

<template>
  <div class="tag-word">
    <span class="tag is-info" @click="isTagged || $emit('startTagging')">{{
      word
    }}</span>
    <span
      class="tag tag-class is-success"
      @click="isTagged || $emit('clear')"
      >{{ tag }}</span
    >
  </div>
</template>

<style scoped>
.tag {
  font-size: clamp(1.2rem, 1.0196rem + 0.9022vw, 1.7188rem);
}

.tag-word {
  display: flex;
  align-items: center;
  margin: 0.5rem;
  flex-direction: column;
  gap: 0.5rem 0.2rem;
  min-width: clamp(3rem, 1.6957rem + 6.5217vw, 6.75rem);
}

.tag-word .tag:empty {
  opacity: 0;
}

.tag-class {
  font-size: clamp(0.8333rem, 0.7406rem + 0.4638vw, 1.1rem);
}
</style>
