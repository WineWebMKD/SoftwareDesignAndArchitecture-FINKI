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
            name: 'Home',
            component: Home
        },
        {
            path: '/about',
            name: 'About',
            component: About
        },
        {
            path: '/map',
            component: Map
        },
        {
            path: '/contact',
            name: 'Contact',
            component: Contact
        }
    ]
})
router.beforeEach((to, from, next) => {
    document.body.classList.add('background-image')
    if (to.name === 'Home') {
        document.body.style.backgroundImage = 'url(src/components/WineWeb/Backgrounds/homepage_background.png)';
    } else if (to.name === 'About') {
        document.body.style.backgroundImage = 'url(src/components/WineWeb/Backgrounds/about_page_background.png)';
    } else if (to.name === 'Contact') {
        // Reset background for other routes
        document.body.style.backgroundImage = 'url(src/components/WineWeb/Backgrounds/contact_page_background.png)';
    } else{
        document.body.style.backgroundImage = 'url(src/components/WineWeb/Backgrounds/map_page_background.png)';
    }
    next();
});
createApp(App)
    .use(router)
    .use(store) // Use your Vuex store
    .mount('#app')
