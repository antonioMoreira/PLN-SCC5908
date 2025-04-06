<script setup lang="ts">
import { useTemplateRef } from "vue";

// Recebe a frase como props:
defineProps({
  result: {
    type: String,
    required: true,
  },
});

const emit = defineEmits(["confirm"]);
const editableText = useTemplateRef("editableText");

function confirmText() {
  // Emitindo o evento "done" com o resultado gravado
  emit("confirm", editableText.value?.innerText);
}
</script>

<template>
  <h1 class="title is-1">Confirme o texto</h1>
  <div class="editable" contenteditable ref="editableText">{{ result }}</div>
  <button class="button is-link mt-4" @click="confirmText">Confirmar</button>
</template>

<style scoped>
.editable {
  width: fit-content;
  margin: 0 auto;
}
</style>
