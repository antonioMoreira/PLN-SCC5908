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

  await delay(2000); // Simulando um delay de 2 segundos

  isLoading.value = false;

  // getTranscription

  // Aqui a gente está emitindo o evento "done" com o resultado gravado
  emit("done", "Frase gravada com sucesso!");
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
