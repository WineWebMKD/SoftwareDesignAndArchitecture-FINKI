<template>
  <div class="outer-block-map">
    <div class="left-block">
      <div >
        <i id="search_icon"><img src="./WineWeb/Icons/Search_icon.png" alt="" @click="checkFilters()"/></i>
        <input v-model="search_input" class="search-bar-map" type="text" :style="{ color: search_input === 'No input' ? 'transparent' : 'white' }"
               :placeholder="language === 'EN' ? 'Name/Address' : 'Име/Адреса'">
      </div>
      <div>
        <label>{{ language === 'EN' ? 'City:' : 'Град:' }}</label>
        <select v-model="selectedCity" id="select-bar-map1" name="City" @change="checkFilters()">
          <option value="all">{{ language === 'EN' ? 'All' : 'Сите' }}</option>
          <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
          <!-- Options for City select -->
        </select >
        <label>{{ language === 'EN' ? 'Occupation:' : 'Занимање:' }}</label>
        <select v-model="selectedOcc" class="select-bar-map2" name="Occupation" @change="checkFilters()">
          <option value="any">{{ language === 'EN' ? 'Any' : 'Било какво' }}</option>
          <option value="vizba">{{ language === 'EN' ? 'Wine cellar' : 'Визба' }}</option>
          <option value="vinarija">{{ language === 'EN' ? 'Winery' : 'Винарија' }}</option>
          <!-- Options for Occupation select -->
        </select>
      </div>
      <label>{{ language === 'EN' ? 'Results:' : 'Резултати:' }}</label>
      <div class="left-block-results">
        <div class="left-block-results" id="filter_results">
        <!-- Results content -->
        </div>
      </div>
    </div>
    <div class="center-block">
      <div id="map" ref="map">

      </div>
    </div>
    <div class="right-block">
      <h2 class="h2-map">{{ language === 'EN' ? 'More information' : 'Повеќе информации' }}</h2>
      <div class="right-block-details">
        <label>{{ language === 'EN' ? 'Address:' : 'Адреса:' }}</label>
        <div class="address-result">
          {{ address }}
          <!-- Address result -->
        </div>
        <label>{{ language === 'EN' ? 'Working hours:' : 'Работно време' }}</label>
        <div class="working-hrs-result">
          {{ working_hours }}
          <!-- Working hours result -->
        </div>
        <label>{{ language === 'EN' ? 'Contact:' : 'Контакт:' }}</label>
        <div class="contact-result">
          <div>{{contact}}</div>
          <!-- Contact result -->
        </div>
        <div class="social-result">
          <a :href="facebook"><img class="fejs" :class="{ 'inactive-link': !facebook}" src="./WineWeb/Icons/Facebook_icon.png" alt="Facebook"></a>
          <a :href="instagram"><img class="insta" :class="{ 'inactive-link': !instagram}" src="./WineWeb/Icons/Insta_icon.png" alt="Instagram"></a>
          <a :href="webpage"><img class="web" :class="{ 'inactive-link': !webpage}" src="./WineWeb/Icons/WebPage_icon.png" alt="Site"></a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import L from 'leaflet';
import {transliterate} from "transliteration";
import {useStore} from "vuex";
import {computed} from "vue";
import cyrillicToTranslit from "cyrillic-to-translit-js";


export default {
  name: 'Map',
  setup() {
    const store = useStore();
    const language = computed(() => store.state.language);
    return {
      language,
    };
  },
  data() {
    return {
      address: null,
      working_hours: null,
      facebook: null,
      instagram: null,
      webpage: null,
      contact: null,
      map: null,
      entries: [],
      cities: [],
      selectedCity: '',
      selectedOcc: '',
      search_input: ''
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
    await this.get_all_data();
    await this.createCities();

  },
  watch: {
    language: async function (newLanguage) {
      try {
        console.log('Language changed:', newLanguage);
        // Call the logic you want to execute when the language changes
        await this.handleLanguageChange(newLanguage);
      } catch (error) {
        console.error('Error in watcher callback:', error);
      }
    }
  },
  methods: {
    translate(text) {
      const translations = {
        'Okhrid': 'Ohrid',
        'Vinari\u0458a': 'Winery',
        'Vineri\u0458a-Kralitsa': 'Winery-Queen',
        'vineri\u0458a': 'Winery',
        'Vineri': 'Winery',
        'Gotse': 'Goce',
        'Vinski': 'Wine',
        'podrum': 'Cellar',
        'Tikvesh-Prodavnitsa': 'Tikvesh',
        'Tsentar': ' ',
        'Direktsi\u0458a': 'directorate',
        'direktsi\u0458a': 'directorate',
        'vinari\u0458a': 'Winery',
        'Vinari': 'Winery',
        'vinari': 'Winery',
        'Vinarska': 'Winery',
        'vizba': 'Cellar',
        'Vizba': 'Cellar',
        'Va\u0458n': 'Wine',
        'va\u0458n': 'Wine',
        'Vino': 'Wine',
        'vino': 'Wine',
        'Rabotno': 'Open',
        'vreme:': ':',
        'Pon': 'Mon',
        'Pet': 'Fri',
        'Sab': 'Sat',
        'Ned': 'Sun',
        'Sre': 'Wed',
        'Chet': 'Thr',
        'od': 'from',
        'do': 'till'
        // Add more translations as needed
      };
      // Convert both text and translation keys to lowercase and remove extra spaces
      const words = text.split(' ');
      console.log('spliting: '+words)
      // Translate each word using the mapping
      const translatedWords = words.map(word => translations[word] || word);

      // Join the translated words back into a string
      const translatedText = translatedWords.join(' ');
      console.log(translatedText);

      return translatedText;
    },
    async createCities(){
      try {
        console.log("Send request to backend for cities")
        const response = await axios.get('http://127.0.0.1:8000/get_all_cities');
        const data = response.data['data'];
        console.log("Parse data..")
        const parsedData = JSON.parse(data);
        console.log("Parsed data is:")
        console.log(parsedData)
        console.log(parsedData[0])
        let latin = false;
        if(this.language === 'EN'){
          latin = true;
        }
        parsedData.forEach(obj => {
          if(latin){
            this.cities.push(transliterate(obj.City))
          }else{
            this.cities.push(obj.City)
          }
        });
      } catch (error) {
        console.error('Error fetching cities:', error);
      }
    },
    async removeAllMarkers() {

      this.map.eachLayer(layer => {
        if (layer instanceof L.Marker) {
          this.map.removeLayer(layer);
        }
      });
    },
    async addNewMarker(latitude, longitude, id, name) {
      // Assuming 'this.map' is your Leaflet map object
      let redIcon = L.icon({
        iconUrl: 'src/components/WineWeb/Icons/custom_red_marker.png',
        iconSize:     [50, 50], // size of the icon
        iconAnchor:   [25, 50], // point of the icon which will correspond to marker's location
        popupAnchor:  [0, -25] // point from which the popup should open relative to the iconAnchor
      });

      //Create a marker with the red icon
      const marker = L.marker([latitude, longitude], { icon: redIcon }).addTo(this.map);
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
        const response = await axios.get('http://127.0.0.1:8000/get_all_data');
        const data = response.data['data'];
        console.log("Parse data..")
        const parsedData = JSON.parse(data);
        console.log("Parsed data is:")
        console.log(parsedData)
        console.log(parsedData[0])

        //map out data columns
        let Wineries = await this.map_data(parsedData)
        //console.log(Wineries)
        const resultSelect = document.getElementById("filter_results");
        while (resultSelect.firstChild) {
          resultSelect.removeChild(resultSelect.firstChild);
        }
        await this.resetDetails()
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
    async resetDetails(){
      this.address = null
      this.working_hours = null
      this.facebook = null
      this.instagram = null
      this.webpage = null
      this.contact = null
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
        let latin = false;
        if(this.language === 'EN'){
          latin = true;
        }

        if(latin){
          this.address = cyrillicToTranslit().transform(`${target[0].Address}`, " ");
          let temp = cyrillicToTranslit().transform(`${target[0].Working_Hours}`, " ");
          this.working_hours = await this.translate(temp);

        }else{
          this.address = cyrillicToTranslit().reverse(`${target[0].Address}`)
          let temp = cyrillicToTranslit().reverse(`${target[0].Working_Hours}`);
          this.working_hours = this.translate(temp);
        }
        this.facebook = `${target[0].Facebook}`
        this.instagram = `${target[0].Instagram}`
        this.webpage = `${target[0].WebPage}`
        this.contact = `${target[0].Numbers}`
        //Checking links
        this.facebook = target[0].Facebook !== 'https://' ? target[0].Facebook : null;
        this.instagram = target[0].Instagram !== 'https://' ? target[0].Instagram : null;
        this.webpage = target[0].WebPage !== 'https://' ? target[0].WebPage : null;

      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    async filterInput(){
      try{
        console.log(this.search_input)
        const encoded_input = transliterate(this.search_input);
        console.log(encoded_input)
        const response = await axios.get(`http://127.0.0.1:8000/get_input_data/${encoded_input}`);// Replace with your backend endpoint
        const data = response.data['data'];
        console.log("Parse data..")
        const parsedData = JSON.parse(data);
        console.log("Data from backend:", parsedData);

        const resultSelect = document.getElementById("filter_results");
        while (resultSelect.firstChild) {
          resultSelect.removeChild(resultSelect.firstChild);
        }
        await this.resetDetails()
        await this.removeAllMarkers()
        const mappedData = await this.map_data(parsedData)
        for (const obj of mappedData) {
          await this.addNewMarker(obj.Latitude, obj.Longitude, obj.ID, obj.Name)
          await this.detailed_results(obj.Name, obj.ID)
        }
      } catch (error){
        console.error("Error fetchigit ng data:", error);
      }
    },
    async checkFilters(){
      if(this.search_input === ""){this.search_input = "No input"}
      if(this.selectedCity === ""){ this.selectedCity = "all"}
      if(this.selectedOcc === ""){ this.selectedOcc = "any"}

      if(this.selectedCity === "all"){
        if(this.selectedOcc === "any") {
          if(this.search_input === "No input") {
            await this.get_all_data()
          } else {
            await this.filterInput()
          }
        } else if(this.search_input === "No input"){
          await this.filterOccupation()
        } else {
          await this.filterResults()
        }
      }else{
        await this.filterResults()
      }
    },
    async filterResults() {
      try{
        console.log(this.selectedCity)
        const encoded_city = transliterate(this.selectedCity);
        console.log(encoded_city)
        console.log(this.search_input)
        const encoded_input = transliterate(this.search_input);
        console.log(encoded_input)
        const response = await axios.get(
            `http://127.0.0.1:8000/get_filtered_data/${encoded_city}/${this.selectedOcc}/${encoded_input}`);
        const data = response.data['data'];
        console.log("Parse data..")
        console.log(data)
        const parsedData = JSON.parse(data);
        console.log("Data from backend:", parsedData);

        const resultSelect = document.getElementById("filter_results");
        while (resultSelect.firstChild) {
          resultSelect.removeChild(resultSelect.firstChild);
        }
        await this.resetDetails()
        await this.removeAllMarkers()
        const mappedData = await this.map_data(parsedData)
        for (const obj of mappedData) {
          await this.addNewMarker(obj.Latitude, obj.Longitude, obj.ID, obj.Name)
          await this.detailed_results(obj.Name, obj.ID)
        }
      } catch (error){
        console.error("Error fetching data:", error);
      }
    },
    async filterOccupation(){
      try{
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
        await this.resetDetails()
        await this.removeAllMarkers()
        const mappedData = await this.map_data(parsedData)
        for (const obj of mappedData) {
          await this.addNewMarker(obj.Latitude, obj.Longitude, obj.ID, obj.Name)
          await this.detailed_results(obj.Name, obj.ID)
        }
      } catch (error){
      console.error("Error fetching data:", error);
      }
    },
    async detailed_results(Name, ID){
      try {
        const resultSelect = document.getElementById("filter_results");
        const div_result = document.createElement("div");

        let latin = false;
        if(this.language === 'EN'){
          latin = true;
        }
        if(latin){
          let temp = cyrillicToTranslit().transform(Name, " ");
          console.log("Name:" +Name)
          console.log("Change:"+temp)
          div_result.textContent = await this.translate(temp)
        }else{
          div_result.textContent = cyrillicToTranslit().reverse(Name, " ");
        }

        div_result.addEventListener('click', () => {
          this.getDataFromBackend(ID);
        });
        div_result.classList.add("result_divs")
        resultSelect.appendChild(div_result);

      } catch (error){
        console.error("Error fetching data:", error);
      }
    },
    async handleLanguageChange(newLanguage){
      try {
        let old_selection = this.selectedCity
        this.cities = []
        await this.createCities();
        if (old_selection !== 'all'){
          if(newLanguage === 'EN'){
            this.selectedCity = cyrillicToTranslit().transform(old_selection, " ");
          }else{
            this.selectedCity = cyrillicToTranslit().reverse(old_selection);
          }
        }else{
          this.selectedCity = old_selection
        }
        await this.checkFilters();
        await this.resetDetails();
      } catch (error){
        console.error("Error changing language:", error);
      }
    }
  }
};
</script>
<style scoped>
@import "leaflet/dist/leaflet.css";

/* Your CSS styles can be placed here */
.social-result .inactive-link {
  pointer-events: none;  /* Make the link non-clickable */
  opacity: 0.5;          /* Adjust the opacity as needed (0.5 for 50% transparency) */
}

#map {
  width: 98%;
  height: 98%;
  overflow: hidden;
}

#filter_results {
  border-radius: 0;
  margin-right: 5%;
  width: 95%;
  height: 95%;
}
/* Define scrollbar styles for WebKit browsers (Chrome, Safari) */
.left-block-results::-webkit-scrollbar {
  margin-right: 5px;
  width: 5px; /* Set the width of the scrollbar */
  background-color: #fff;
}

.left-block-results::-webkit-scrollbar-thumb {
  background-color: #fff; /* Set the color of the scrollbar thumb */
  border: 10px solid #ccc; /* Set the width and color of the border around the thumb */
}

.left-block-results::-webkit-scrollbar-track {
  background-color: transparent; /* Set the color of the scrollbar track */
}

#search_icon {
  margin-left: 5%;
  margin-top: 1%;
  width: 25px;
  height: 25px;
}
#search_icon > img {
  align-content: center;
  justify-content: center;
  width: 25px;
  height: 25px;
}
body{
  background-color: #e1c6a8;
}
::placeholder {
  color: white;
}

</style>
