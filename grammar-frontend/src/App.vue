<script setup lang="ts">
import TranscriptorView from "./views/TranscriptorView.vue";
import TaggingView from "./views/TaggingView.vue";
import TextView from "./views/TextView.vue";

import { ref } from "vue";

// Esse <> é para dizer para o typescript que a variável
// que a `ref` vai ser  "transcriptor" ou "tagging"
// x:Literal["transcriptor", "confirm", "tagging"] = "transcriptor"
const page = ref<"transcriptor" | "confirm" | "tagging">("transcriptor");
const transcription = ref<string>("");
const text = ref<string>("");

// O evento @done é emitido pelo TranscriptorView
// E passa como argumento a frase gravada
function handleTranscription(result: string) {
  page.value = "confirm";
  transcription.value = result;
}

async function handleConfirm(confirmedText: string) {
  const result = await fetch("http://localhost:5678/tagger", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      sentence: confirmedText,
    }),
  });
  if (!result.ok) {
    console.error("Erro ao transcrever áudio");
    return;
  }
  const { data } = await result.json();
  page.value = "tagging";
  text.value = data;
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
