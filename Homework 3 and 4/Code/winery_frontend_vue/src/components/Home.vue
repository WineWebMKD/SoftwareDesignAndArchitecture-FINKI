<template>
  <div class="outer-block-home">
    <div class="inner-block-home">
      <div class="image-container">
        <div class="image-text">
          {{ language === 'EN' ? 'Discover top wineries with just one click - your gateway to the finest wine experiences!'
                                : 'Пронајди врвни винарии со само еден клик - вашата влезна точка до најдобрите вински искуства!' }}
        </div>
        <img class="image" src="@/components/WineWeb/HomePageImages/WineWebLetters.png" alt="HomePageImage">
      </div>
      <router-link to="/map">
        <button class="home-button">
          {{ language === 'EN' ? 'SEARCH NOW' : 'ПРЕБАРАЈ ОДМА' }}
        </button>
      </router-link>
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
      language
    };
  },
};
</script>

<style scoped>
.outer-block-home {
  background-color: #CFAA87;
  width: 50%;
  height: 100%;
  margin: 0 auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.inner-block-home {
  display: flex;
  justify-content: center;

}
.image-container {
  position: relative;
  text-align: center;
}
.image {
  width: 100%;
  height: auto;
  display: block;
}
.image-text {
  color: white;
  width: 350px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 26px;
  padding-top: 10vh;
}
.home-button {
  background-color: #7D1310;
  color: white;
  width: 250px;
  height: 50px;
  position: absolute;
  top: 73%;
  left: 50%;
  transform: translate(-50%, -50%);
  -ms-transform: translate(-50%, -50%);
  font-size: 1.2em;
  padding: 12px 24px;
  border: none;
  border-radius: 30px;
  cursor: pointer;
}
</style>