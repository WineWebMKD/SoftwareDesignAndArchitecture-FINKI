<template>
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
</template>
<script>
import {useStore} from "vuex";
import {computed} from "vue";
import axios from "axios";
import cyrillicToTranslit from "cyrillic-to-translit-js";

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
      address: null,
      working_hours: null,
      facebook: null,
      instagram: null,
      webpage: null,
      contact: null,
    };
  },
  async mounted() {

  },
  methods: {
    async resetDetails(){
      this.address = null
      this.working_hours = null
      this.facebook = null
      this.instagram = null
      this.webpage = null
      this.contact = null
    },
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
    async map_data(parsedData){
      return parsedData.map(obj => {
        return {
          Address: obj.Address,
          Working_Hours: obj['Working Hours'],
          Facebook: obj.Facebook,
          Instagram: obj.Instagram,
          WebPage: obj.WebPage,
          Numbers: obj.Numbers
        };
      })
    },

  }
}
</script>
<style scoped>
.right-block-details{
  width: 90%;
  height: 100%;
  margin-left: 5%;
  background: #B18B6A;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
}
.address-result{
  color: #7D1310;
  margin-left: 10%;
  width: 60%;
  height: 10%;
  background: #B18B6A;
  border-radius: 10px;
}
.contact-result{
  color: #7D1310;
  margin-left: 10%;
  width: 60%;
  height: 10%;
  background: #B18B6A;
  border-radius: 10px;
}
.working-hrs-result{
  color: #7D1310;
  margin-left: 10%;
  width: 60%;
  height: 10%;
  background: #B18B6A;
  border-radius: 10px;
}
div.outer-block-map > div.right-block > div > label
{
  padding-top: 10%;
  font-size: 1.2em;
  padding-left: 10%;
  color: white;
}
.social-result {
  margin-top: 10%;
  width: 100%;
  height: 10%;
  border-radius: 1%;
  margin-left: 25%;
}
div.outer-block-map > div.right-block > div > div.social-result > a > img {
  width: 35px;
  height: 35px;
  padding-right: 10%;
}
.social-result .inactive-link {
  pointer-events: none;  /* Make the link non-clickable */
  opacity: 0.5;          /* Adjust the opacity as needed (0.5 for 50% transparency) */
}
</style>