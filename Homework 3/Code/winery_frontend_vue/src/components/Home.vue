<template>
  <div class="outer-block-home">
    <div class="inner-block-home">
      <div class="image-container">
        <div class="image-text">
          Discover top wineries with just one click - your gateway to the finest wine experiences!
        </div>
        <img class="image" src="./WineWeb/HomePage_logo/Bright_Colorful_Playful_Funny_Donuts_Food_Circle_Logo__2_-removebg-preview.png" alt="HomePageImage">
      </div>
<!--      <img class="image" src="./WineWeb/HomePage_logo/Bright_Colorful_Playful_Funny_Donuts_Food_Circle_Logo__2_-removebg-preview.png" alt="HomePageImage">-->
<!--      <div class="image-text">-->
<!--        Discover top wineries with just one click - your gateway to the finest wine experiences!-->
<!--      </div>-->
      <router-link to="/map"><button class="home-page-button">SEARCH NOW</button></router-link>
    </div>
  </div>
</template>

<script>
export default {
  // Component logic can be added here
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
</style>
