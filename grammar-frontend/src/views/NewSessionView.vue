<script setup lang="ts">
defineEmits<{
  selectYear: [string];
}>();

const years = [
  { id: "4-ensino-fundamental", name: "4º ano do Ensino Fundamental" },
  { id: "5-ensino-fundamental", name: "5º ano do Ensino Fundamental" },
  { id: "6-ensino-fundamental", name: "6º ano do Ensino Fundamental" },
  { id: "7-ensino-fundamental", name: "7º ano do Ensino Fundamental" },
  { id: "8-ensino-fundamental", name: "8º ano do Ensino Fundamental" },
  { id: "9-ensino-fundamental", name: "9º ano do Ensino Fundamental" },
  { id: "1-ensino-medio", name: "1º ano do Ensino Médio" },
  { id: "2-ensino-medio", name: "2º ano do Ensino Médio" },
  { id: "3-ensino-medio", name: "3º ano do Ensino Médio" },
];
</script>

<template>
  <div class="container mt-2">
    <div class="content">
      <h1>Bem vindo ao GramatiQuizz</h1>
      <h2>Instruções:</h2>
      <ol>
        <li>Selecionar sua série;</li>
        <li>Ler a frase proposta para o teste</li>
        <li>
          Para cada palavra da frase você deve selecionar a classe
          morfossintática que ela pertence
        </li>
      </ol>
      <h2>Considerações</h2>
      <ul>
        <li>Não se preocupe se você errar</li>
        <li>Você pode responder na ordem que quiser</li>
        <li>Você pode fazer o teste quantas vezes quiser</li>
      </ul>
    </div>
    <div class="buttons mt-6">
      <button
        v-for="year in years"
        :key="year.id"
        class="button is-large"
        :class="[
          year.id.endsWith('ensino-fundamental') ? 'is-success' : 'is-info',
        ]"
        @click="() => $emit('selectYear', year.id)"
      >
        {{ year.name }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.buttons {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: clamp(1.125rem, 0.0815rem + 5.2174vw, 4.125rem);
}

.content {
  padding-inline: clamp(1.125rem, 0.0815rem + 5.2174vw, 4.125rem);
}

li {
  font-size: 1.1rem;
}
</style>
