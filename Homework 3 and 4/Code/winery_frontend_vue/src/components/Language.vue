<template>
  <div class="container">
    <div class="navigation-bar bottom">
      <span>{{ language === 'EN' ? 'Language' : 'Јазик' }}:</span>
      <button :class="{ 'inactive': language === 'EN' }" @click="setLanguage('EN')">EN</button>
      <button :class="{ 'inactive': language === 'MK' }" @click="setLanguage('MK')">MK</button>
    </div>
  </div>
</template>

<script setup>
import { useStore } from 'vuex';
import {computed} from "vue";
const store = useStore();
const language = computed(() => store.state.language);
const setLanguage = (language) => {
  console.log('Setting language:', language);
  store.commit('setLanguage', language);
};
</script>

<style scoped>
button {
  color: #FFFFFF;
  width: 5%;
  background-color: transparent;
  border-radius: 16px;
  border-width: 0 0 4px;
  border-right: solid;
  border-color: #282828;
  box-sizing: border-box;
  cursor: pointer;
  display: inline-block;
  font-size: 1em;
  outline: none;
  overflow: visible;
  text-align: center;
  text-transform: uppercase;
  touch-action: manipulation;
  vertical-align: middle;
  white-space: nowrap;
}
span {
  color: white;
  margin-right: 2%;
}
button.inactive {
  color: lightgray;
  pointer-events: none;
}
</style>