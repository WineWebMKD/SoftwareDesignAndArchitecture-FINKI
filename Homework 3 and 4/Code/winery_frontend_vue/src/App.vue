<template>
  <header>
    <link href='https://fonts.googleapis.com/css?family=Montserrat' rel='stylesheet'>
  </header>

  <main>
    <div id="app">
      <Navbar />
      <router-view></router-view>
      <Language />
    </div>
  </main>
</template>

<script>
import {defineComponent} from "vue";
import Navbar from "@/components/Navbar.vue";
import Language from "@/components/Language.vue";
import { useStore } from 'vuex';

export default defineComponent({
  components: {Navbar, Language},
  setup() {
    const store = useStore();
    const language = store.state.language;

    return {
      language
    };
  },
})
</script>
<style scoped>
@import "leaflet/dist/leaflet.css";
header {
  line-height: 1.5;
}
@media (min-width: 1024px) {
  header{
    display: flex;
    place-items: flex-start;
    padding-right: calc(var(--section-gap) / 2);
    flex-wrap: wrap;
  }
}
</style>
