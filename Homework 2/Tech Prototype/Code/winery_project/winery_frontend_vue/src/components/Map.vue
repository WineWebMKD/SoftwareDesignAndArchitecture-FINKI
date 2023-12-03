<template>
  <div class="outer-block-map">
    <div class="left-block">
      <input class="search-bar-map" type="text" placeholder="         Name/Address">
      <label>City</label>
      <select class="select-bar-map1" name="City">
        <!-- Options for City select -->
      </select>
      <label>Occupation</label>
      <select class="select-bar-map2" name="Occupation">
        <!-- Options for Occupation select -->
      </select>
      <label>Results</label>
      <div class="left-block-results">
        <!-- Results content -->
      </div>
    </div>
    <div class="center-block">

      <!-- Content for the new centered block -->
      <div>
        <h2 class="h2-map" style="margin-left:0px;">Connecting to backend:</h2>
        <!-- Render divs for each entry -->
        <div v-for="(entry, index) in entries" :key="index" class="entry">
          <h3>{{ entry.Name }}</h3>
          <p>City: {{ entry.City }}</p>
          <p>Address: {{ entry.Address }}</p>
          <p>See more...</p>
          <!-- Add more properties as needed -->
        </div>
      </div>
    </div>
<!--    <div class="map-block">-->
<!--      &lt;!&ndash; Map content &ndash;&gt;-->
<!--    </div>-->
    <div class="right-block">
      <h2 class="h2-map">Details</h2>
      <div class="right-block-details">
        <label>Adress:</label>
        <div class="adress-result">
          <!-- Address result -->
        </div>
        <label>Working hours:</label>
        <div class="working-hrs-result">
          <!-- Working hours result -->
        </div>
        <label>Contact:</label>
        <div class="contact-result">
          <!-- Contact result -->
        </div>
        <div class="social-result">
          <img class="fejs" src="./WineWeb/Icons/Facebook_icon.png" alt="Facebook">
          <img class="insta" src="./WineWeb/Icons/Insta_icon.png" alt="Instagram">
          <img class="web" src="./WineWeb/Icons/WebPage_icon.png" alt="Site">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      entries: []
    };
  },
  async mounted() {
    try {
      console.log("Send request to backend")
      const response = await axios.get('http://127.0.0.1:8000/get_data');
      const data = response.data['data'];
      console.log("Parse data..")
      const parsedData = JSON.parse(data);
      console.log("Parsed data is:")
      console.log(parsedData)
      console.log(parsedData[0])
      this.entries = parsedData.slice(0, 5)

      // Assuming the received JSON data contains a list of entries named 'entries'
      // const entries = data.entries;

      // Update the UI by setting the entries in the center-block div
      // this.displayEntries(entries);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  },
  methods: {}

};
</script>

<style scoped>
/* Your CSS styles can be placed here */
</style>
