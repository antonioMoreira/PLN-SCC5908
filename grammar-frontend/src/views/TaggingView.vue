<script setup lang="ts">
import { computed, reactive, useTemplateRef } from "vue";
import { shuffle } from "es-toolkit";
import { animate } from "motion";
import TagWord from "../components/TagWord.vue";
import useInteractionEvents from "../composables/useInteraction";
import JSConfetti from "js-confetti";

const jsConfetti = new JSConfetti();

export type Word = {
  word: string;
  tag: string;
};

// Recebe a frase como props:
const { phrase, sessionId } = defineProps<{
  phrase: Word[];
  sessionId: string;
}>();

const wordsRef = useTemplateRef("wordsRef");
const { publishInteractionEvent } = useInteractionEvents(sessionId);

function shakeWords() {
  animate(
    wordsRef.value!,
    {
      x: [-10, 10, 0],
      "--background-color": [
        "var(--bulma-body-background-color)",
        "var(--bulma-danger)",
        "var(--bulma-body-background-color)",
      ],
    },
    {
      duration: 0.333,
    }
  );
}

function tagWord(targetIndex: number) {
  if (!draggedText) return;
  const { tag, tagSymbol } = draggedText;

  const correctTag = words[targetIndex].correctTag;
  const word = words[targetIndex].content;

  publishInteractionEvent({
    correctTag,
    draggedTag: tag,
    targetWord: word,
  });
  if (correctTag === tag) {
    words[targetIndex].tag = tag;
    words[targetIndex].tagSymbol = tagSymbol;
  } else {
    shakeWords();
  }
  if (allTagged.value) {
    jsConfetti.addConfetti({
      confettiNumber: 100,
    });
  }
}

const allTagged = computed(() => {
  return words.every((word) => word.tag === word.correctTag);
});

const words: {
  content: string;
  tag?: string;
  tagSymbol?: symbol;
  correctTag: string;
}[] = reactive(
  phrase.map((item) => ({
    content: item.word,
    correctTag: item.tag,
  }))
);

const tags = reactive(
  shuffle(
    phrase.map((item) => ({
      name: item.tag,
      tagSymbol: Symbol(),
    }))
  )
);

const tagList = computed(() => {
  return tags.map((item) => ({
    name: item.name,
    tagSymbol: item.tagSymbol,
    isUsed: words.some((word) => word.tagSymbol === item.tagSymbol),
  }));
});

function restart() {
  window.location.reload();
}

let draggedText:
  | {
      tag: string;
      tagSymbol: symbol;
    }
  | undefined;
</script>

<template>
  <div class="words" ref="wordsRef">
    <TagWord
      :word="word.content"
      v-for="(word, index) in words"
      :key="index"
      :tag="word.tag"
      :is-tagged="word.tag === word.correctTag"
      @dragover.prevent
      @drop.prevent="() => tagWord(index)"
    />
  </div>

  <div class="available-tags" :data-active="true">
    <div
      class="tag is-size-4 is-info"
      :data-used="tag.isUsed"
      :key="tag.tagSymbol"
      v-for="tag in tagList"
      draggable="true"
      @dragstart="
        () => (draggedText = { tag: tag.name, tagSymbol: tag.tagSymbol })
      "
      @dragend="() => (draggedText = undefined)"
    >
      {{ tag.name }}
    </div>
  </div>
  <small v-if="!allTagged"
    >Arraste a classe morfossintática para a palavra correspondente</small
  >
  <button
    class="button is-primary is-large has-text-centered btn-hover"
    @click="restart"
  >
    {{ allTagged ? "Fazer teste novamente" : "Reiniciar" }}
  </button>
</template>

<style scoped>
.tag {
  font-size: clamp(1rem, 0.7609rem + 1.1957vw, 1.6875rem);
}

[data-used="true"] {
  display: none;
}

.available-tags {
  margin-top: 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  align-items: center;
  font-size: 1.5rem;
  opacity: 0.25;
}

.available-tags[data-active="true"] {
  opacity: 1;
}

.words {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  align-items: center;
  font-size: 2.5rem;
  margin-bottom: calc(clamp(3rem, 1.6957rem + 6.5217vw, 6.75rem) * 0.8);
  background-color: var(--background-color);
}

small {
  display: block;
  margin-top: 2rem;
  font-size: 2rem;
  text-align: center;
}

@property --background-color {
  syntax: "<color>";
  inherits: false;
  initial-value: --bulma-body-background-color;
}

.restart-button {
  font-size: clamp(1.2rem, 1.0196rem + 0.9022vw, 1.7188rem);
  display: block;
  margin-inline: auto;
  margin-top: clamp(3rem, 1.6957rem + 6.5217vw, 6.75rem);
}

.btn-hover {
  padding: 10px 20px;
  /* background-color: var(--color-primary); */
  /* color: white; */
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: clamp(1.2rem, 1.0196rem + 0.9022vw, 1.7188rem);
  display: block;
  margin-inline: auto;
  margin-top: clamp(3rem, 1.6957rem + 6.5217vw, 6.75rem);
}

.btn-hover:hover {
  transform: translateY(-4px);
  /* box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15); */
}
</style>
