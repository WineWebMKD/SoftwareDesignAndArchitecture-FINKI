<template>
  <div class="left-block-results" id="filter_results">
    <!-- Results divs -->
  </div>
</template>
<script>
import axios from "axios";
import cyrillicToTranslit from "cyrillic-to-translit-js";
import {useStore} from "vuex";
import {computed} from "vue";
import {translate} from "@/translation";

export default {
  setup() {
    const store = useStore();
    const language = computed(() => store.state.language);
    return {
      language
    };
  },
  data() {
    return {
      map: null
    };
  },
  async mounted() {
    await this.getAllData();
  },
  methods: {
    async mapData(parsed_data){
      return parsed_data.map(obj => {
        return {
          ID: obj.ID,
          Name: obj.Name
        };
      })
    },
    async getAllData() {
      try {
        // Get all winery names
        const response = await axios.get('http://127.0.0.1:8000/get_winery_name');
        const data = response.data['data'];
        const parsed_data = JSON.parse(data);
        await this.createResultDivs(parsed_data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    async createResultDivs(data){
      //map out data columns
      let Wineries = await this.mapData(data);
      const result_select = document.getElementById("filter_results");
      // Resetting the results
      while (result_select.firstChild) {
        result_select.removeChild(result_select.firstChild);
      }
      for (const obj of Wineries) {
        await this.addResultDiv(obj.Name, obj.ID);
      }
    },
    async addResultDiv(name, id){
      try {
        const result_select = document.getElementById("filter_results");
        const div_result = document.createElement("div");
        // Check language
        let latin = false;
        if(this.language === 'EN'){
          latin = true;
        }
        if(latin){
          div_result.textContent = translate(cyrillicToTranslit().transform(name, " "));
        }else{
          div_result.textContent = translate(cyrillicToTranslit().reverse(name, " "));
        }
        div_result.dataset.id = id.toString();
        div_result.addEventListener('click', () => {
          // Emit event when clicked
          this.$emit('resultClicked', id, 2);
          this.setAsSelected(div_result);
        });
        div_result.classList.add("result_divs");
        // Add the new div to the results
        result_select.appendChild(div_result);
      } catch (error){
        console.error("Error fetching data:", error);
      }
    },
    setAsSelected(selected_div) {
      // Remove the 'selected' class from all divs in the results
      const result_divs = document.querySelectorAll('.result_divs');
      result_divs.forEach((div) => {
        div.classList.remove('selected');
      });
      // Add the 'selected' class to the clicked div
      selected_div.classList.add('selected');
    },
    findResult(marker_id) {
      // Find the result associated with the marker_id in the data
      const result_divs = document.querySelectorAll('.result_divs');
      // Find the result element with a data-id attribute matching the marker_id
      const result = Array.from(result_divs).find(div => div.dataset.id === marker_id.toString());
      if (result) {
        this.setAsSelected(result);
        this.scrollAndSetAsSelected(result);
      }
    },
    scrollAndSetAsSelected(selected_div) {
      // Scroll to the selected div
      selected_div.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
      this.setAsSelected(selected_div);
    }
  }
};
</script>
<style >
#filter_results {
  width: 95%;
  height: 95%;
  border-radius: 0;
  margin-right: 5%;
}
.result_divs {
  background-color: #e1c6a8;
  box-shadow: 0 8px 10px rgba(0, 0, 0, 0.6);
  color: #7D1310;
  width: 95%;
  height: 10%;
  padding-top: 1%;
  padding-left: 1%;
  margin-top: 2%;
  margin-right: 2%;
  font-size: 1em;
  text-align: center;
  border-radius: 5px;
}
.result_divs.selected {
  background-color: #7D1310;
  color: white;
}
</style>