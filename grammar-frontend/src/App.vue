<script setup lang="ts">
import TranscriptorView from "./views/TranscriptorView.vue";
import TaggingView from "./views/TaggingView.vue";
import TextView from "./views/TextView.vue";

import { ref } from "vue";

// Esse <> é para dizer para o typescript que a variável
// que a `ref` vai ser  "transcriptor" ou "tagging"
const page = ref<"transcriptor" | "confirm" | "tagging">("transcriptor");
const transcription = ref<string>("");
const text = ref<string>("");

// O evento @done é emitido pelo TranscriptorView
// E passa como argumento a frase gravada
function handleTranscription(result: string) {
  page.value = "confirm";
  transcription.value = result;
}

function handleConfirm(result: string) {
  page.value = "tagging";
  text.value = result;
}
</script>

<template>
  <div class="container mt-6 has-text-centered">
    <!-- Aqui a função @done pode receber argumentos do evento -->
    <TranscriptorView
      @done="handleTranscription"
      v-if="page === 'transcriptor'"
    />
    <TextView
      @confirm="handleConfirm"
      :result="transcription"
      v-else-if="page === 'confirm'"
    />
    <TaggingView :result="text" v-else-if="page === 'tagging'" />
  </div>
</template>
