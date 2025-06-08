<script setup lang="ts">
import TranscriptorView from "./views/TranscriptorView.vue";
import TaggingView, { type Word } from "./views/TaggingView.vue";
import TextView from "./views/TextView.vue";
import NewSessionView from "./views/NewSessionView.vue";
import { nanoid } from "nanoid";
import useInteractionEvents from "./composables/useInteraction";
import { ref } from "vue";

const page = ref<"newSession" | "transcriptor" | "confirm" | "tagging">(
  "newSession"
);

const transcription = ref<string>("");
const text = ref<Word[]>([]);
const schoolYear = ref("");
const sessionId = nanoid(10);
const { publishNewSessionEvent } = useInteractionEvents(sessionId);

// O evento @done é emitido pelo TranscriptorView
// E passa como argumento a frase gravada
function handleTranscription(result: string) {
  page.value = "confirm";
  transcription.value = result;
}

async function handleConfirm(confirmedText: string) {
  // "http://localhost:5678/tagger"
  const result = await fetch("https://auth.legenda.live/ws-7/tagger", {
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
  text.value = data as unknown;

  // data precisa ser um Word[] para isso aqui funcionar
  publishNewSessionEvent(schoolYear.value, data);
}

function handleSelectYear(selectedYear: string) {
  schoolYear.value = selectedYear;
  page.value = "transcriptor";
}
</script>

<template>
  <div class="container mt-6">
    <NewSessionView
      @select-year="handleSelectYear"
      v-if="page === 'newSession'"
    />
    <TranscriptorView
      @done="handleTranscription"
      v-else-if="page === 'transcriptor'"
    />
    <TextView
      @confirm="handleConfirm"
      :result="transcription"
      v-else-if="page === 'confirm'"
    />
    <TaggingView :phrase="text" :session-id v-else-if="page === 'tagging'" />
  </div>
</template>
