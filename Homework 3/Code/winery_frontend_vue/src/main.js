import './assets/main.css'
import Home from '@/components/Home.vue';
import About from '@/components/About.vue';
import Map from '@/components/Map.vue';
import Contact from "@/components/Contact.vue";

import {createRouter, createWebHistory} from "vue-router";


// main.js

//import * as Vue from 'vue';
// import Vue from 'vue';
import App from './App.vue';// Import the router configuration

import {createApp} from "vue";
import store from "@/store";


const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            redirect: '/home' // Set the default route to Contact page
        },
        {
            path: '/home',
            component: Home
        },
        {
            path: '/about',
            component: About
        },
        {
            path: '/map',
            component: Map
        },
        {
            path: '/contact',
            component: Contact
        }
    ]
})

createApp(App)
    .use(router)
    .use(store) // Use your Vuex store
    .mount('#app')
// new Vue({
//     router, // Use the router
//     render: h => h(App)
// }).$mount('#app');
