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
      <a :href="facebook"><img class="fejs" :class="{ 'inactive-link': !facebook}" src="./Icons/Facebook_icon.png" alt="Facebook"></a>
      <a :href="instagram"><img class="insta" :class="{ 'inactive-link': !instagram}" src="./Icons/Insta_icon.png" alt="Instagram"></a>
      <a :href="webpage"><img class="web" :class="{ 'inactive-link': !webpage}" src="./Icons/WebPage_icon.png" alt="Site"></a>
    </div>
  </div>
</template>
<script>
import {useStore} from "vuex";
import {computed} from "vue";
import axios from "axios";
import cyrillicToTranslit from "cyrillic-to-translit-js";
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
      address: null,
      working_hours: null,
      facebook: null,
      instagram: null,
      webpage: null,
      contact: null
    };
  },
  methods: {
    async mapData(parsed_data){
      return parsed_data.map(obj => {
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
    async resetDetails(){
      this.address = null;
      this.working_hours = null;
      this.facebook = null;
      this.instagram = null;
      this.webpage = null;
      this.contact = null;
    },
    async getDataFromBackend(winery_id) {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/get_data/${winery_id}`);// Replace with your backend endpoint
        const data = response.data['data'];
        const parsed_data = JSON.parse(data);
        // Handle the received data
        let target = await this.mapData(parsed_data);

        let latin = false;
        if(this.language === 'EN'){
          latin = true;
        }

        if(latin){
          this.address = cyrillicToTranslit().transform(`${target[0].Address}`, " ");
          let temp = cyrillicToTranslit().transform(`${target[0].Working_Hours}`, " ");
          this.working_hours = translate(temp);

        }else{
          this.address = cyrillicToTranslit().reverse(`${target[0].Address}`);
          let temp = cyrillicToTranslit().reverse(`${target[0].Working_Hours}`);
          this.working_hours = translate(temp);
        }
        this.facebook = `${target[0].Facebook}`;
        this.instagram = `${target[0].Instagram}`;
        this.webpage = `${target[0].WebPage}`;
        this.contact = `${target[0].Numbers}`;

        //Checking links
        this.facebook = target[0].Facebook !== 'https://' ? target[0].Facebook : null;
        this.instagram = target[0].Instagram !== 'https://' ? target[0].Instagram : null;
        this.webpage = target[0].WebPage !== 'https://' ? target[0].WebPage : null;
      } catch (error) {
        console.error("Error fetching more information:", error);
      }
    }
  }
}
</script>
<style scoped>
.right-block-details {
  background: #B18B6A;
  box-shadow: 0 8px 10px rgba(0, 0, 0, 0.6);
  width: 90%;
  height: 100%;
  margin-left: 5%;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
}
.address-result {
  background: #B18B6A;
  color: #7D1310;
  width: 60%;
  height: 10%;
  margin-left: 10%;
  border-radius: 10px;
}
.contact-result {
  background: #B18B6A;
  color: #7D1310;
  width: 60%;
  height: 10%;
  margin-left: 10%;
  border-radius: 10px;
}
.working-hrs-result {
  background: #B18B6A;
  color: #7D1310;
  width: 60%;
  height: 10%;
  margin-left: 10%;
  border-radius: 10px;
}
div.outer-block-map > div.right-block > div > label {
  color: white;
  padding-top: 10%;
  font-size: 1.2em;
  padding-left: 10%;
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
  pointer-events: none;
  opacity: 0.5;
}
</style>