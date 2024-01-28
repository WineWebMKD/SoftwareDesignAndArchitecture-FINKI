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
      <div id="map" ref="map">

      </div>
    </div>
    <div class="right-block">
      <h2 class="h2-map">Details</h2>
      <div class="right-block-details">
        <label>Address:</label>
        <div class="address-result">
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
import L from 'leaflet';

export default {
  name: 'Map',

  data() {
    return {
      map: null,
      entries: []
    };
  },
  async mounted() {
    // Create the map
    var map = L.map(this.$refs.map).setView([51.505, -0.09], 13);

    // Add OpenStreetMap tile layer
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 22,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);
    var marker = L.marker([51.5, -0.09]).addTo(map);
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
@import "leaflet/dist/leaflet.css";

/* Your CSS styles can be placed here */
#map{
  width: 90%;
  height: 90%;
  overflow: hidden;
}
</style>
