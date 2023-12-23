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
        <div id="address-result">
          {{ address }}
          <!-- Address result -->
        </div>
        <label>Working hours:</label>
        <div class="working-hrs-result">
          {{ working_hours }}
          <!-- Working hours result -->
        </div>
        <label>Contact:</label>
        <div class="contact-result">
          <!-- Contact result -->
        </div>
        <div class="social-result">
          <div>{{contact}}</div>
          <a :href="facebook"><img class="fejs" src="./WineWeb/Icons/Facebook_icon.png" alt="Facebook"></a>
          <a :href="instagram"><img class="insta" src="./WineWeb/Icons/Insta_icon.png" alt="Instagram"></a>
          <a :href="webpage"><img class="web" src="./WineWeb/Icons/WebPage_icon.png" alt="Site"></a>
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
      address: "null",
      working_hours: "null",
      facebook: null,
      instagram: null,
      webpage: null,
      contact: "no.",
      map: null,
      entries: []
    };
  },
  async mounted() {
    // Create the map
    let map = L.map(this.$refs.map).setView([51.505, -0.09], 13);

    // Add OpenStreetMap tile layer
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 22,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    try {
      console.log("Send request to backend")
      const response = await axios.get('http://127.0.0.1:8000/get_all_coordinates');
      const data = response.data['data'];
      console.log("Parse data..")
      const parsedData = JSON.parse(data);
      console.log("Parsed data is:")
      console.log(parsedData)
      console.log(parsedData[0])
      //map out data columns
      let Wineries = parsedData.map(obj => {
        return {
          ID: obj.ID,
          Latitude: obj.Latitude,
          Longitude: obj.Longitude,
          Name: obj.Name,
          Address: obj.Address
        };
      });
      console.log(Wineries)
      for (let i = 0; i < Wineries.length; i++) {
        //get specific coordinates
        let coordinate = Wineries[i];
        console.log(coordinate)
        //create marker and user interaction with it
        const marker = L.marker([coordinate.Latitude, coordinate.Longitude]).addTo(map);
        marker.bindPopup(`<b>${coordinate.Name}</b><br>Address: ${coordinate.Address}<br>`);
        marker.on('click', () => {
          this.getDataFromBackend(coordinate.ID);
        });
        //console print coordinates (check)
        console.log(`Coordinate ${coordinate.ID}: (${coordinate.Latitude}, ${coordinate.Longitude})`);
      }

    } catch (error) {
      console.error('Error fetching data:', error);
    }

  },

  methods: {
    async getDataFromBackend(markerId) {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/get_data/${markerId}`);// Replace with your backend endpoint
        const data = response.data['data'];
        console.log("Parse data..")
        const parsedData = JSON.parse(data);
        console.log("Data from backend:", parsedData);
        // Handle the received data, update UI, etc.
        let target = parsedData.map(obj => {
          return {
            ID: obj.ID,
            Address: obj.Address,
            Working_Hours: obj.Working_Hours,
            Facebook: obj.Facebook,
            Instagram: obj.Instagram,
            WebPage: obj.WebPage,
            Numbers: obj.Numbers
          };
        });
        console.log(target)
        this.address = `${target[0].Address}`
        this.working_hours = `${target[0].Working_hours}`
        this.facebook = `${target[0].Facebook}`
        this.instagram = `${target[0].Instagram}`
        this.webpage = `${target[0].WebPage}`
        this.contact = `${target[0].Numbers}`

      } catch (error) {
        console.error("Error fetching data:", error);
      }
    }}

};
</script>
<style scoped>
@import "leaflet/dist/leaflet.css";

/* Your CSS styles can be placed here */
#map{
  width: 98%;
  height: 98%;
  overflow: hidden;
}
</style>
