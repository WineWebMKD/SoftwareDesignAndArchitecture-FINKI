<template>
  <div class="container">
    <div class="navigation-bar bottom">
      <span>Language: </span>
      <button @click="setLanguage('EN')">EN</button>
      <button @click="setLanguage('MK')">MK</button>
    </div>
  </div>
</template>

<script setup>
import { useStore } from 'vuex';
const store = useStore();
const setLanguage = (language) => {
  console.log('Setting language:', language);
  store.commit('setLanguage', language);
};
</script>

<style scoped>

</style>