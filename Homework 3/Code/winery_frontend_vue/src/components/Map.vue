<template>
  <div class="outer-block-map">
    <div class="left-block">
      <input class="search-bar-map" type="text" placeholder="         Name/Address">
      <label>City</label>
      <select v-model="selectedCity" id="select-bar-map1" name="City" @change="filterResults">
        <option value="all">All</option>
        <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
        <!-- Options for City select -->
      </select >
      <label>Occupation</label>
      <select v-model="selectedOcc" class="select-bar-map2" name="Occupation" @change="filterResults">
        <option value="any">Any</option>
        <option value="vizba">Визба</option>
        <option value="vinarija">Винарија</option>
        <!-- Options for Occupation select -->
      </select>
      <label>Results</label>
      <div class="left-block-results" id="filter_results">
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
          <div>{{contact}}</div>
          <!-- Contact result -->
        </div>
        <div class="social-result">
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
import {transliterate} from "transliteration";

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
      entries: [],
      cities: [],
      selectedCity: '',
      selectedOcc: ''
    };
  },
  async mounted() {
    // Create the map
    this.map = L.map(this.$refs.map).setView([41.6086, 21.7453], 8);
    // Add OpenStreetMap tile layer
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 22,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(this.map);
    await this.get_all_data()

    try {
      console.log("Send request to backend for cities")
      const response = await axios.get('http://127.0.0.1:8000/get_all_cities');
      const data = response.data['data'];
      console.log("Parse data..")
      const parsedData = JSON.parse(data);
      console.log("Parsed data is:")
      console.log(parsedData)
      console.log(parsedData[0])

      parsedData.forEach(obj => {
        this.cities.push(obj.City)
      });

    } catch (error) {
      console.error('Error fetching cities:', error);
    }
  },

  methods: {
    async removeAllMarkers() {

      this.map.eachLayer(layer => {
        if (layer instanceof L.Marker) {
          this.map.removeLayer(layer);
        }
      });
    },
    async addNewMarker(latitude, longitude, id, name) {
      // Assuming 'this.map' is your Leaflet map object
      const marker = L.marker([latitude, longitude]).addTo(this.map);
      marker.bindPopup(`<b>${name}</b>`);
      marker.on('click', () => {
          this.getDataFromBackend(id);
      });
    },
    async map_data(parsedData){
      return parsedData.map(obj => {
        return {
          ID: obj.ID,
          Latitude: obj.Latitude,
          Longitude: obj.Longitude,
          Name: obj.Name,
          Address: obj.Address,
          Working_Hours: obj['Working Hours'],
          Facebook: obj.Facebook,
          Instagram: obj.Instagram,
          WebPage: obj.WebPage,
          Numbers: obj.Numbers
        };
      })
    },
    async get_all_data() {
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
        let Wineries = await this.map_data(parsedData)
        console.log(Wineries)

        await this.removeAllMarkers()
        for (const obj of Wineries) {
          //get specific coordinates
          console.log(obj)
          //create marker and user interaction with it
          await this.addNewMarker(obj.Latitude, obj.Longitude, obj.ID, obj.Name)
          console.log(`Coordinate ${obj.ID}: (${obj.Latitude}, ${obj.Longitude})`);
          await this.detailed_results(obj.Name, obj.ID)
        }

      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    async getDataFromBackend(markerId) {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/get_data/${markerId}`);// Replace with your backend endpoint
        const data = response.data['data'];
        console.log("Parse data..")
        const parsedData = JSON.parse(data);
        console.log("Data from backend:", parsedData);
        // Handle the received data, update UI, etc.
        let target = await this.map_data(parsedData)

        console.log(target)
        this.address = `${target[0].Address}`
        this.working_hours = `${target[0].Working_Hours}`
        this.facebook = `${target[0].Facebook}`
        this.instagram = `${target[0].Instagram}`
        this.webpage = `${target[0].WebPage}`
        this.contact = `${target[0].Numbers}`

      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    async filterResults() {
      try{
        if(this.selectedCity === "all"){
          if(this.selectedOcc === "any"){
            await this.get_all_data()
          }else {
            await this.filterOccupation()
          }
        }else{
          console.log(this.selectedCity)
          const encoded_city = transliterate(this.selectedCity);
          console.log(encoded_city)
          const response = await axios.get(`http://127.0.0.1:8000/get_filtered_data/${encoded_city}/${this.selectedOcc}`);// Replace with your backend endpoint
          const data = response.data['data'];
          console.log("Parse data..")
          const parsedData = JSON.parse(data);
          console.log("Data from backend:", parsedData);

          const resultSelect = document.getElementById("filter_results");
          while (resultSelect.firstChild) {
            resultSelect.removeChild(resultSelect.firstChild);
          }
          await this.removeAllMarkers()
          const mappedData = await this.map_data(parsedData)
          for (const obj of mappedData) {
            await this.addNewMarker(obj.Latitude, obj.Longitude, obj.ID, obj.Name)
            await this.detailed_results(obj.Name, obj.ID)
          }
        }
      } catch (error){
        console.error("Error fetching data:", error);
      }
    },
    async filterOccupation(){
      try{
        if(this.selectedOcc === ""){
          await this.get_all_data()
        }else{
          console.log(this.selectedOcc)
          const occupation = this.selectedOcc
          const response = await axios.get(`http://127.0.0.1:8000/get_occupation/${occupation}`);// Replace with your backend endpoint
          const data = response.data['data'];
          console.log("Parse data..")
          const parsedData = JSON.parse(data);
          console.log("Data from backend:", parsedData);

          const resultSelect = document.getElementById("filter_results");
          while (resultSelect.firstChild) {
            resultSelect.removeChild(resultSelect.firstChild);
          }
          await this.removeAllMarkers()
          const mappedData = await this.map_data(parsedData)
          for (const obj of mappedData) {
            await this.addNewMarker(obj.Latitude, obj.Longitude, obj.ID, obj.Name)
            await this.detailed_results(obj.Name, obj.ID)
          }
        }
      } catch (error){
      console.error("Error fetching data:", error);
      }
    },
    async detailed_results(Name, ID){
      try {
        const resultSelect = document.getElementById("filter_results");
        const div_result = document.createElement("div");
        div_result.textContent = Name;
        div_result.addEventListener('click', () => {
          this.getDataFromBackend(ID);
        });
        resultSelect.appendChild(div_result);

      } catch (error){
        console.error("Error fetching data:", error);
      }
    }
  }
};
</script>
<style scoped>
@import "leaflet/dist/leaflet.css";

/* Your CSS styles can be placed here */
#map {
  width: 98%;
  height: 98%;
  overflow: hidden;
}

/* Define scrollbar styles for WebKit browsers (Chrome, Safari) */
.left-block-results::-webkit-scrollbar {
  margin-right: 5px;
  width: 5px; /* Set the width of the scrollbar */
  background-color: #fff;
}

.left-block-results::-webkit-scrollbar-thumb {
  margin-right: -5px;
  background-color: #fff; /* Set the color of the scrollbar thumb */
  border: 10px solid #ccc; /* Set the width and color of the border around the thumb */
}

.left-block-results::-webkit-scrollbar-track {
  background-color: transparent; /* Set the color of the scrollbar track */
}
</style>
