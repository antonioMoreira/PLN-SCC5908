<script setup lang="ts">
import { useUserMedia } from "@vueuse/core";
import { recordAudio } from "../utils/recordAudio";
import { blob2Base64 } from "../utils/blobToBase64";
import { ref } from "vue";
import { delay } from "es-toolkit";

// defineEmits is a macro in Vue 3.
const emit = defineEmits(["done"]);

const { stream } = useUserMedia({
  constraints: {
    audio: {
      sampleRate: 16000,
      channelCount: 1,
    },
  },
  autoSwitch: true,
  enabled: true,
});

const isRecording = ref(false);
const isLoading = ref(false);

let stopRecording: (() => Promise<Blob>) | undefined;

async function startRecording() {
  if (!stream.value) {
    // Se não tiver stream, não tem como gravar
    console.error("Não foi possível acessar o microfone");
    return;
  }

  isRecording.value = true;
  stopRecording = recordAudio(stream.value);
}

async function stopRecordingAndGetBlob() {
  if (!stopRecording) {
    console.error("Gravação não iniciada");
    return;
  }

  const blob = await stopRecording();
  stopRecording = undefined;

  // Aqui a gente pode fazer o que quiser com o blob
  // Por exemplo, enviar para o servidor ou salvar no disco
  console.log(blob);

  const base64 = await blob2Base64(blob, "audio/wav");
  isLoading.value = true;

  console.log(base64);

  const result = await fetch("http://localhost:5679/transcribe", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      audio_base64: base64,
    }),
  });

  if (!result.ok) {
    console.error("Erro ao transcrever áudio");
    isLoading.value = false;
    return;
  }

  const {transcription} = await result.json();

  isLoading.value = false;

  // getTranscription

  // Aqui a gente está emitindo o evento "done" com o resultado gravado
  emit("done", transcription);
}
</script>

<template>
  <button v-if="!isRecording" class="button is-link" @click="startRecording">
    Gravar
  </button>
  <button
    v-else
    class="button is-danger"
    :class="{ 'is-loading': isLoading }"
    @click="stopRecordingAndGetBlob"
  >
    Parar
  </button>
</template>
