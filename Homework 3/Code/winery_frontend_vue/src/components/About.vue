<template>
  <div class="outer-block-about">
    <h2 class="title">{{ language === 'EN' ? 'WHY WINERIES?' : 'ЗОШТО ВИНАРИИ?' }}</h2>
    <div class="inner-block-about">
      <div class="content">
        <p>{{ language === 'EN' ? "Wine production holds a pivotal role in Macedonia's culture and economy. " +
            "The region benefits from favorable climatic and agricultural conditions, creating an ideal environment for cultivating vines and crafting exceptional wines renowned for their rich aromas and flavors. " +
            "Despite Macedonia's prominent standing on the global wine stage, many remain unfamiliar with its winemaking traditions, and a vast majority have yet to experience the opportunity of visiting a winery and savoring the authentic taste of Macedonian wine."
            : "Производството на вино има клучна улога во македонската култура и економија." +
            " Регионот има поволните климатски и земјоделски услови, создавајќи идеална средина за одгледување винова лоза и изработка на исклучителни вина познати по своите богати ароми и вкусови." +
            " Покрај истакнатата позиција на Македонија на глобалната винска сцена, многумина не се запознаени со нејзините традиции за производство на вино, а огромното мнозинство допрва треба да ја искусат можноста да посетат винарија и да го вкусат автентичниот вкус на македонското вино." }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import {computed} from 'vue';
import {useStore} from "vuex";

export default {
  setup() {
    const store = useStore();
    const language = computed(() => store.state.language);

    return {
      language,
    };
  },
};
</script>

<style scoped>
/* Your CSS styles can be placed here */
.inner-block-about {
  background-color: #B18B6A;
  padding: 5%;

  margin: 0 auto;
  text-align: center;
  text-overflow: clip;
  height: 70%;
  width: 80%;
}
.outer-block-about > h2 {
  display: flex;
  justify-content: center; /* Center horizontally */
  align-items: center;
  margin-block-start: 0.83em;
  margin-block-end: 0.83em
}
.inner-block-about > div {
  background-color: #B18B6A;
  font-size: 1.4em;
  margin: 0 auto;
  text-align: center;
  overflow: auto;
  height: 100%;
  width: 100%;
}
</style>
