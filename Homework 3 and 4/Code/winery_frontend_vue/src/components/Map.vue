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
        <results-component ref="ResultsComponent" @resultClicked="getMoreInfo"></results-component>
      </div>
    </div>
    <div class="center-block">
      <map-component ref="MapComponent" @markerClicked="getMoreInfo"></map-component>
    </div>
    <div class="right-block">
      <h2 class="h2-map">{{ language === 'EN' ? 'More information' : 'Повеќе информации' }}</h2>
        <information-component ref="InformationComponent"></information-component>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import {transliterate} from "transliteration";
import {useStore} from "vuex";
import {computed} from "vue";
import cyrillicToTranslit from "cyrillic-to-translit-js";
import MapComponent from "@/components/MapComponent.vue";
import ResultsComponent from "@/components/FilterResults.vue";
import InformationComponent from "@/components/MoreInformation.vue";


export default {
  components: {
    MapComponent,
    ResultsComponent,
    InformationComponent
  },
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
      cities: [],
      selectedCity: '',
      selectedOcc: '',
      search_input: ''
    };
  },
  async mounted() {
    // await this.get_all_data();
    await this.createCities();

  },
  watch: {
    language: async function (newLanguage) {
      try {
        console.log('Language changed:', newLanguage);
        await this.handleLanguageChange(newLanguage);
      } catch (error) {
        console.error('Error in watcher callback:', error);
      }
    }
  },
  methods: {
    // ne znam
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
        'do': 'till',
        'Kavadarci': 'Кавадарци',
        'Кавадарци': 'Kavadarci'
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
    //map.vue
    async createCities(){
      try {
        console.log("Send request to backend for cities")
        const response = await axios.get('http://127.0.0.1:8000/get_all_cities');
        const data = response.data['data'];
        console.log("Parse data..")
        const parsedData = JSON.parse(data);
        console.log("Parsed data is:")
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
    //check
    async map_data(parsedData){
      return parsedData.map(obj => {
        return {
          ID: obj.ID,
          Name: obj.Name,
          Latitude: obj.Latitude,
          Longitude: obj.Longitude,
          Address: obj.Address,
          Working_Hours: obj['Working Hours'],
          Facebook: obj.Facebook,
          Instagram: obj.Instagram,
          WebPage: obj.WebPage,
          Numbers: obj.Numbers
        };
      })
    },
    getMoreInfo(markerID, optionClicked){
      this.$refs.InformationComponent.getDataFromBackend(markerID);
      if(optionClicked === 2) this.$refs.MapComponent.findMarker(markerID);
      else this.$refs.ResultsComponent.findResult(markerID);
    },
    // map.vue
    async checkFilters(){
      if(this.search_input === ""){this.search_input = "No input"}
      if(this.selectedCity === ""){ this.selectedCity = "all"}
      if(this.selectedOcc === ""){ this.selectedOcc = "any"}

      if(this.selectedCity === "all" && this.selectedOcc === "any" && this.search_input === "No input"){
        await this.$refs.MapComponent.get_all_data()
        await this.$refs.ResultsComponent.get_all_data()
      }else await this.filterResults()
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
        // console.log("Data from backend:", parsedData);

        const resultSelect = document.getElementById("filter_results");
        while (resultSelect.firstChild) {
          resultSelect.removeChild(resultSelect.firstChild);
        }
        await this.$refs.InformationComponent.resetDetails()
        await this.$refs.MapComponent.removeAllMarkers()
        const mappedData = await this.map_data(parsedData)
        for (const obj of mappedData) {
          await this.$refs.MapComponent.addNewMarker(obj.Latitude, obj.Longitude, obj.ID, obj.Name)
          await this.$refs.ResultsComponent.detailed_results(obj.Name, obj.ID)
        }
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
        await this.$refs.InformationComponent.resetDetails();
      } catch (error){
        console.error("Error changing language:", error);
      }
    }
  }
};
</script>
<style scoped>
.outer-block-map {
  background: #CFAA87;
  width: 90%;
  height: 100%;
  display: flex; /* Use flexbox for the outer container */
  margin: 0 auto;
  padding-top: 20px;
  padding-bottom: 20px;

}
.center-block {
  background: #e1c6a8;
  flex: 1; /* Allow the block to grow and take remaining space */
  display: flex;
  justify-content: center; /* Horizontally center the content */
  align-items: center; /* Vertically center the content */
}
.left-block {
  background: #CFAA87;
  width: 30%;
  display: flex;
  flex-direction: column;
  /* Avoid specifying height unless necessary */
}

.right-block {
  background: #CFAA87;
  width: 30%;
  display: flex;
  justify-content: center;
  align-content: center;
  flex-direction: column;
}
/* Define scrollbar styles for WebKit browsers (Chrome, Safari) */
.left-block-results::-webkit-scrollbar {
  margin-right: 5px;
  width: 5px; /* Set the width of the scrollbar */
  background-color: #fff;
}

.left-block-results::-webkit-scrollbar-thumb {
  background-color: #8d0e0e; /* Set the color of the scrollbar thumb */
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
div.outer-block-map > div.left-block > div > input{
  background: #B18B6A;
  margin-left: 4%;
  border-radius: 5px;
  height: 30px;
  width: 78%;
  color: white;
}
div.outer-block-map > div.left-block > div > label{
  padding-top: 1%;
  padding-left: 5%;
  color: white;
}
div.outer-block-map > div.left-block > label{
  padding-top: 1%;
  padding-left: 5%;
  color: white;
}
div.outer-block-map > div.left-block > div{
  display: flex;
  margin-top: 1%;
}
div.outer-block-map > div.left-block > div > select{
  display: flex;
  justify-content: center;
  align-content: center;
  height: 20px;
  width: 25%;
  background: #B18B6A;
  margin-top: 1%;
  margin-left: 1%;
  border-radius: 5px;
  color: white;
}
.left-block-results{
  width: 90%;
  height: 90%;
  overflow-y: auto;
  direction: rtl;
  background: #B18B6A;
  margin-top: 2%;
  margin-left: 5%;
  border-radius: 10px;
}
.h2-map{
  display: flex;
  justify-content: center; /* Center horizontally */
  align-items: center;
  margin-block-start: 0.83em;
  margin-block-end: 0.83em;
  color: #7D1310;
}
.center-block div {
  width: 100%;
  height: 100%;
}
</style>
