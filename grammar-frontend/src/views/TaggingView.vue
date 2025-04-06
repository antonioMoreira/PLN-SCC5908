<script setup lang="ts">
// Recebe a frase como props:
defineProps({
  result: {
    type: String,
    required: true,
  },
});

function refresh() {
  window.location.reload();
}
</script>

<template>
  <h1 class="title is-1">Tagging: {{ result }}</h1>
  <div>{{ result }}</div>
  <button class="button mt-4" @click="refresh">Refresh</button>
</template>
