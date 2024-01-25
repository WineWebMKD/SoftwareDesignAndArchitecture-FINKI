<template>
  <div class="left-block-results" id="filter_results">
    <!-- Results content -->
  </div>
</template>
<script>
import axios from "axios";
import {transliterate} from "transliteration";
import cyrillicToTranslit from "cyrillic-to-translit-js";
import {useStore} from "vuex";
import {computed} from "vue";

export default {
  setup() {
    const store = useStore();
    const language = computed(() => store.state.language);
    return {
      language,
    };
  },
  data() {
    return {
      map: null,
    };
  },
  async mounted() {
    await this.get_all_data();
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
      console.log('spliting: ' + words)
      // Translate each word using the mapping
      const translatedWords = words.map(word => translations[word] || word);

      // Join the translated words back into a string
      const translatedText = translatedWords.join(' ');
      console.log(translatedText);

      return translatedText;
    },
    async map_data(parsedData){
      return parsedData.map(obj => {
        return {
          ID: obj.ID,
          Name: obj.Name,
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

        //map out data columns
        let Wineries = await this.map_data(parsedData)

        const resultSelect = document.getElementById("filter_results");
        while (resultSelect.firstChild) {
          resultSelect.removeChild(resultSelect.firstChild);
        }
        await this.resetDetails()
        for (const obj of Wineries) {
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
        div_result.dataset.id = ID.toString();
        div_result.addEventListener('click', () => {
          this.$emit('resultClicked', ID, 2);
          this.setAsSelected(div_result);
        });
        div_result.classList.add("result_divs")
        resultSelect.appendChild(div_result);

      } catch (error){
        console.error("Error fetching data:", error);
      }
    },
    setAsSelected(selectedDiv) {
      // Remove the 'selected' class from all divs in the results
      const resultDivs = document.querySelectorAll('.result_divs');
      resultDivs.forEach((div) => {
        div.classList.remove('selected');
      });

      // Add the 'selected' class to the clicked div
      selectedDiv.classList.add('selected');
    },
    findResult(markerID) {
      // Find the result associated with the markerID in your data
      const resultDivs = document.querySelectorAll('.result_divs');
      // Find the result element with a data-id attribute matching the markerID
      const result = Array.from(resultDivs).find(div => div.dataset.id === markerID.toString());
      console.log(result)
      // If a result is found, emit an event or perform any action you need
      if (result) {
        console.log("did it")
        this.setAsSelected(result)
        this.scrollAndSetAsSelected(result);
      }
    },
    scrollAndSetAsSelected(selectedDiv) {
      // Scroll to the selected div
      selectedDiv.scrollIntoView({
        behavior: 'smooth',
        block: 'start',
      });

      // Set the selected class
      this.setAsSelected(selectedDiv);
    },
  }
};
</script>
<style >
#filter_results {
  border-radius: 0;
  margin-right: 5%;
  width: 95%;
  height: 95%;
}
.result_divs{
  width: 97%;
  height: 10%;
  padding-top: 1%;
  padding-left: 1%;
  margin-top: 2%;
  margin-left: 2%;
  font-size: 1em;
  text-align: center;
  color: #7D1310;
  border-radius: 5px;
  background-color: #e1c6a8;
}
.result_divs.selected {
  background-color: #7D1310;
  color: white;
}
</style>