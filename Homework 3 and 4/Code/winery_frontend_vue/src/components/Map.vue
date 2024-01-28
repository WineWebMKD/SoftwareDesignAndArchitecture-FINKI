<template>
  <div class="outer-block-map">
    <div class="left-block">
      <div >
        <i id="search_icon"><img src="./Icons/Search_icon.png" alt="" @click="checkFilters()"/></i>
        <input v-model="search_input" class="search-bar-map" type="text" :style="{ color: search_input === 'No input' ? 'transparent' : 'white' }"
               :placeholder="language === 'EN' ? 'Name/Address' : 'Име/Адреса'">
      </div>
      <div>
        <label>{{ language === 'EN' ? 'City:' : 'Град:' }}</label>
        <select v-model="selected_city" id="select-bar-map1" name="City" @change="checkFilters()">
          <option value="all">{{ language === 'EN' ? 'All' : 'Сите' }}</option>
          <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
          <!-- Options for City select -->
        </select >
        <label>{{ language === 'EN' ? 'Occupation:' : 'Занимање:' }}</label>
        <select v-model="selected_occupation" class="select-bar-map2" name="Occupation" @change="checkFilters()">
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
import { translate } from '@/translation';


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
      language
    };
  },
  data() {
    return {
      cities: [],
      selected_city: '',
      selected_occupation: '',
      search_input: ''
    };
  },
  async mounted() {
    await this.createCities();
  },
  watch: {
    language: async function (new_language) {
      try {
        // Handle language change
        await this.handleLanguageChange(new_language);
      } catch (error) {
        console.error('Error when handling language:', error);
      }
    }
  },
  methods: {
    async createCities(){
      try {
        // Send request to backend for city options
        const response = await axios.get('http://127.0.0.1:8000/get_all_cities');
        const data = response.data['data'];
        const parsed_data = JSON.parse(data);

        let latin = false;
        if(this.language === 'EN'){
          latin = true;
        }
        parsed_data.forEach(obj => {
          if(latin){
            this.cities.push(transliterate(obj.City));
          }else{
            this.cities.push(obj.City);
          }
        });
      } catch (error) {
        console.error('Error fetching cities:', error);
      }
    },
    getMoreInfo(winery_id, option_clicked){
      //More information for selected winery
      this.$refs.InformationComponent.getDataFromBackend(winery_id);
      //Find selected marker if winery name was clicked
      if(option_clicked === 2) this.$refs.MapComponent.findMarker(winery_id);
      //Find selected winery name if marker was clicked
      else this.$refs.ResultsComponent.findResult(winery_id);
    },
    async checkFilters(){
      if(this.search_input === ""){this.search_input = "No input"}
      if(this.selected_city === ""){ this.selected_city = "all"}
      if(this.selected_occupation === ""){ this.selected_occupation = "any"}

      if(this.selected_city === "all" && this.selected_occupation === "any" && this.search_input === "No input"){
        await this.$refs.MapComponent.getAllCoordinates();
        await this.$refs.ResultsComponent.getAllData();
      }else await this.filterResults();
    },
    async filterResults() {
      try{
        const encoded_city = transliterate(this.selected_city);
        const encoded_input = transliterate(this.search_input);
        const response = await axios.get(
            `http://127.0.0.1:8000/get_filtered_data/${encoded_city}/${this.selected_occupation}/${encoded_input}`);
        const data = response.data['data'];
        const parsed_data = JSON.parse(data);

        //Reset previous data
        await this.$refs.InformationComponent.resetDetails();
        await this.$refs.MapComponent.removeAllMarkers();
        //Create new filtered markers
        const winery_ids = parsed_data.map(obj => parseInt(obj.ID, 10));
        console.log(winery_ids)
        await this.$refs.MapComponent.checkLocation(winery_ids);
        //Create new filtered results
        await this.$refs.ResultsComponent.createResultDivs(parsed_data);
      } catch (error){
        console.error("Error fetching filtered data:", error);
      }
    },
    async handleLanguageChange(new_language){
      try {
        let old_selection = this.selected_city;
        this.cities = [];
        await this.createCities();
        if (old_selection !== 'all'){
          if(new_language === 'EN'){
            this.selected_city = transliterate(old_selection);
          }else{
            this.selected_city = translate(cyrillicToTranslit().reverse(old_selection));
          }
        }else{
          this.selected_city = old_selection;
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
  display: flex;
  margin: 0 auto;
  padding-top: 20px;
  padding-bottom: 20px;

}
.center-block {
  background: #e1c6a8;
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}
.left-block {
  background: #CFAA87;
  width: 30%;
  display: flex;
  flex-direction: column;
}
.right-block {
  background: #CFAA87;
  width: 30%;
  display: flex;
  justify-content: center;
  align-content: center;
  flex-direction: column;
}
.left-block-results::-webkit-scrollbar {
  background-color: #fff;
  width: 5px;
  margin-right: 5px;
}
.left-block-results::-webkit-scrollbar-thumb {
  background-color: #8d0e0e;
}
.left-block-results::-webkit-scrollbar-track {
  background-color: transparent;
}
#search_icon {
  width: 25px;
  height: 25px;
  margin-left: 5%;
  margin-top: 1%;
}
#search_icon > img {
  width: 25px;
  height: 25px;
  align-content: center;
  justify-content: center;
}
body {
  background-color: #e1c6a8;
}
::placeholder {
  color: white;
}
div.outer-block-map > div.left-block > div > input {
  background: #B18B6A;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.6);
  color: white;
  height: 30px;
  width: 78%;
  margin-left: 3.8%;
  border-radius: 5px;
  border: transparent;
}
div.outer-block-map > div.left-block > div > label {
  color: white;
  padding-top: 1%;
  padding-left: 5%;
}
div.outer-block-map > div.left-block > label {
  color: white;
  padding-top: 1%;
  padding-left: 5%;
}
div.outer-block-map > div.left-block > div {
  display: flex;
  margin-top: 1%;
}
div.outer-block-map > div.left-block > div > select {
  background: #B18B6A;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.6);
  color: white;
  height: 20px;
  width: 25%;
  display: flex;
  justify-content: center;
  align-content: center;
  margin-top: 1%;
  margin-left: 1%;
  border-radius: 5px;
  border: none;
}
.left-block-results {
  background: #B18B6A;
  width: 90%;
  height: 90%;
  overflow-y: auto;
  direction: rtl;
  margin-top: 2%;
  margin-left: 5%;
  border-radius: 10px;
}
.h2-map {
  color: #7D1310;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-block-start: 0.83em;
  margin-block-end: 0.83em;
}
.center-block div {
  width: 100%;
  height: 100%;
}
</style>
