<template>
  <div class="container">
    <nav class="navigation-bar">
      <ul>
        <li :class="{ 'active': $route.path === '/home' }"><router-link to="/home">{{ language === 'EN' ? 'HOME' : 'ДОМА' }}</router-link></li>
        <li :class="{ 'active': $route.path === '/about'}"><router-link to="/about">{{ language === 'EN' ? 'ABOUT' : 'ЗА НАС' }}</router-link></li>
        <li :class="{ 'active': $route.path === '/map'}"><router-link to="/map">{{ language === 'EN' ? 'MAP' : 'МАПА' }}</router-link></li>
        <li :class="{ 'active': $route.path === '/contact'}"><router-link to="/contact">{{ language === 'EN' ? 'CONTACT' : 'КОНТАКТ' }}</router-link></li>
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
ul {
  list-style-type: none;
  margin: 5%;
  display: flex;
}
.navigation-bar li.active {
  color: inherit;
  font-weight: 1000;
  pointer-events: none;
}
a {
  color: white;
  width: 50%;
  text-decoration: none;
  font-size: 25px;
}
a:hover {
  color: #9a3f3f;
}
a:active{
  font-weight: bold;
}
li {
  width: 120px;
  text-align: center;
  margin-right: 45px;
}
</style>