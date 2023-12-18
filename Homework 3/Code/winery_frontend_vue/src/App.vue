<template>
  <header>
    <link href='https://fonts.googleapis.com/css?family=Montserrat' rel='stylesheet'>
  </header>

  <main>
    <div id="app">
      <Navbar />
      <router-view></router-view>
      <div class="container">
        <div class="navigation-bar bottom">
        </div>
      </div>
    </div>
<!--    <Contact />-->
  </main>
</template>

<script>
import {defineComponent} from "vue";
import Navbar from "@/components/Navbar.vue";

export default defineComponent({
  components: {Navbar}
})
</script>
<style scoped>
@import "leaflet/dist/leaflet.css";
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
