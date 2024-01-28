// main.js
import App from './App.vue';
import './assets/main.css'
import {createApp} from "vue";
import store from "@/store";
import router from "@/router" // Import the router configuration
import { translate } from '@/translation';

const app = createApp(App);

app.config.globalProperties.$translate = translate;

app
    .use(router)
    .use(store) // Use your Vuex store
    .mount('#app')
