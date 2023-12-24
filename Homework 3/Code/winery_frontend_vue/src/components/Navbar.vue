<template>
  <div class="container">
    <nav class="navigation-bar">
      <ul>
        <li><router-link to="/home">{{ language === 'EN' ? 'HOME' : 'ДОМА' }}</router-link></li>
        <li><router-link to="/about">{{ language === 'EN' ? 'ABOUT' : 'ЗА НАС' }}</router-link></li>
        <li><router-link to="/map">{{ language === 'EN' ? 'MAP' : 'МАПА' }}</router-link></li>
        <li><router-link to="/contact">{{ language === 'EN' ? 'CONTACT' : 'КОНТАКТ' }}</router-link></li>
      </ul>
    </nav>
  </div>
</template>

<script setup>
import {useStore} from "vuex";
import {computed} from "vue";

const store = useStore();
const language = computed(() => store.state.language);
</script>

<style scoped>

</style>