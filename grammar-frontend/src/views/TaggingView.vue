<script setup lang="ts">
import { computed, reactive, ref } from "vue";
import { shuffle } from "es-toolkit";
import TagWord from "../components/TagWord.vue";

// Recebe a frase como props:
defineProps({
  result: {
    type: String,
    required: true,
  },
});

const taggingTarget = ref<number>(-1);

function tagWord(tag: string, symbol: symbol) {
  // Se o target for -1, não tem como marcar nada
  if (taggingTarget.value < 0) return;

  // Remove primeiro de outra palavra se está usando
  // o mesmo símbolo
  const otherWord = words.find((word) => word.tagSymbol === symbol);
  if (otherWord) {
    otherWord.tag = undefined;
    otherWord.tagSymbol = undefined;
  }

  words[taggingTarget.value].tag = tag;
  words[taggingTarget.value].tagSymbol = symbol;
  taggingTarget.value = -1;
}

function clearWord(index: number) {
  words[index].tag = undefined;
  words[index].tagSymbol = undefined;
}

const example = {
  data: [
    [
      {
        word: "Oi",
        tag: "PROPN",
      },
      {
        word: ",",
        tag: "PUNCT",
      },
      {
        word: "meu",
        tag: "DET",
      },
      {
        word: "nome",
        tag: "NOUN",
      },
      {
        word: "é",
        tag: "AUX",
      },
      {
        word: "Antonio",
        tag: "PROPN",
      },
      {
        word: "Moreira",
        tag: "PROPN",
      },
      {
        word: ".",
        tag: "PUNCT",
      },
    ],
  ],
};

const words: {
  content: string;
  tag?: string;
  tagSymbol?: symbol;
  correctTag: string;
}[] = reactive(
  example.data[0].map((item) => ({
    content: item.word,
    correctTag: item.tag,
  }))
);

const tags = reactive(
  shuffle(
    example.data[0].map((item) => ({
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

function resetTagging() {
  words.forEach((word) => {
    word.tag = undefined;
    word.tagSymbol = undefined;
  });
}
</script>

<template>
  <div class="words">
    <TagWord
      :word="word.content"
      v-for="(word, index) in words"
      :key="index"
      :tag="word.tag"
      :correct="word.correctTag"
      @start-tagging="() => (taggingTarget = index)"
      @clear="() => clearWord(index)"
    />
  </div>

  <div class="available-tags" :data-active="taggingTarget > -1">
    <div
      class="tag is-size-4"
      :class="[tag.isUsed ? 'is-light' : 'is-info']"
      :key="tag.tagSymbol"
      v-for="tag in tagList"
      @click="tagWord(tag.name, tag.tagSymbol)"
    >
      {{ tag.name }}
    </div>
  </div>

  <button class="button mt-4" @click="resetTagging">Resetar</button>
</template>

<style scoped>
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
  margin-bottom: 80px;
}
</style>
