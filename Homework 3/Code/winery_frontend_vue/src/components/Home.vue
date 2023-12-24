<template>
  <div class="outer-block-home">
    <div class="inner-block-home">
      <div class="image-container">
        <div class="image-text">
          {{ language === 'EN' ? 'Discover top wineries with just one click - your gateway to the finest wine experiences!'
                                : 'Пронајди врвни винарии со само еден клик - вашата влезна точка до најдобрите вински искуства!' }}
        </div>
        <img class="image" src="./WineWeb/HomePage_logo/Bright_Colorful_Playful_Funny_Donuts_Food_Circle_Logo__2_-removebg-preview.png" alt="HomePageImage">
      </div>
      <router-link to="/map">
        <button class="home-page-button">
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
      language,
    };
  },
};
</script>

<style scoped>
/* Your CSS styles can be placed here */
.image-container {
  position: relative;
  text-align: center; /* Center the text horizontally */
}

.image {
  display: block;
  width: 100%; /* Adjust this as needed */
  height: auto; /* Adjust this as needed */
}

.image-text {
  position: absolute;
  top: 50%; /* Adjust as needed */
  left: 50%; /* Adjust as needed */
  transform: translate(-50%, -50%);
  padding-top: 10vh; /* Optional: Add padding to the text */
}


.image-text{
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 350px;
  font-size: 26px;
  color: white;
}

.home-page-button{
  position: absolute;
  top: 58%;
  left: 50%;
  transform: translate(-50%, -50%);
  -ms-transform: translate(-50%, -50%);
  background-color: #7D1310;
  color: white;
  font-size: 20px;
  padding: 12px 24px;
  border: none;
  cursor: pointer;
  border-radius: 30px;
  width: 250px;
  height: 50px;
}
</style>
