<template>
    <!-- Map component code goes here -->
    <div id="map" ref="map"></div>
</template>

<script>
import L from 'leaflet';
import axios from "axios";
import {transliterate} from "transliteration";
import {useStore} from "vuex";
import {computed} from "vue";

export default {
  setup() {
    const store = useStore();
    const language = computed(() => store.state.language);
    const selectedMarker = null;
    const initialView = {
      center: [41.6086, 21.7453],
      zoom: 8
    };
    return {
      language,
      selectedMarker,
      initialView,
    };
  },
  data() {
    return {
      map: null,
      iconProperties: {
        iconSize: [50, 50],
        iconAnchor: [25, 50],
        popupAnchor: [0, -25],
      },
      selectedIconUrl: 'src/components/WineWeb/Icons/custom_red_marker.png',
      defaultIconUrl: 'src/components/WineWeb/Icons/default_marker_icon.png',
    };
  },
  async mounted() {
    // Map initialization code goes here
    this.map = L.map(this.$refs.map).setView(this.initialView.center, this.initialView.zoom);
    // Add OpenStreetMap tile layer
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 22,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(this.map);
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
    async get_all_data() {
      try {
        this.map.setView(this.initialView.center, this.initialView.zoom);
        console.log("Send request to backend")
        const response = await axios.get('http://127.0.0.1:8000/coordinates_info');
        const data = response.data['data'];
        console.log("Parse data..")
        const parsedData = JSON.parse(data);
        this.selectedMarker = null;

        await this.createMarkers(parsedData)
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    async createMarkers(Data){
      let Wineries = await this.map_data(Data)
      await this.removeAllMarkers()
      for (const obj of Wineries) {
        //create marker and user interaction with it
        await this.addNewMarker(obj.Latitude, obj.Longitude, obj.ID, obj.Name)
        console.log(`Coordinate ${obj.ID}: (${obj.Latitude}, ${obj.Longitude})`);
      }
    },
    async map_data(parsedData) {
      return parsedData.map(obj => {
        return {
          ID: obj.ID,
          Name: obj.Name,
          Latitude: obj.Latitude,
          Longitude: obj.Longitude
        };
      })
    },
    async removeAllMarkers() {
      this.map.eachLayer(layer => {
        if (layer instanceof L.Marker) {
          this.map.removeLayer(layer);
        }
      });
    },
    async addNewMarker(latitude, longitude, id, name) {
      let latin = false;
      console.log(latin)
      if (this.language === 'EN') {
        latin = true;
        console.log("YES")
      }
      if (latin) {
        name = transliterate(name);
      }

      // Create a marker with the specified icon URL
      const marker = L.marker([latitude, longitude], {
        icon: L.icon({
          iconUrl: this.defaultIconUrl,
          ...this.iconProperties
        }),
      }).addTo(this.map);

      // Store the obj.ID as a custom property on the marker
      marker.objID = id;

      marker.on('click', () => {
        // Change the icon for the previously selected marker (if any) to the default icon
        this.selectMarker(marker);
        // marker.bindPopup(`<b>${name}</b>`);
        this.$emit('markerClicked', id, 1);
      });
    },
    selectMarker(marker) {
      // Change the icon for the previously selected marker (if any) to the default icon
      if (this.selectedMarker) {
        this.selectedMarker.setIcon(L.icon({
          iconUrl: this.defaultIconUrl,
          ...this.iconProperties
        }));
      }

      // Set the icon for the clicked marker to the selected icon
      marker.setIcon(L.icon({
        iconUrl: this.selectedIconUrl,
        ...this.iconProperties
      }));

      // Update the selected marker
      this.selectedMarker = marker;
    },
    findMarker(ID) {
      let foundMarker = null;

      // Iterate through each marker on the map
      this.map.eachLayer(layer => {
        if (layer instanceof L.Marker) {
          const markerId = layer.objID;

          // Check if the marker objID matches the provided ID
          if (markerId === ID) {
            foundMarker = layer;
          }
        }
      });
      if (foundMarker) {
        // Zoom to the selected marker
        this.selectMarker(foundMarker);
        this.map.setView(foundMarker.getLatLng(), 13); // You can adjust the zoom level (14 is just an example)
      }
    },
  },
};
</script>

<style scoped>
@import "leaflet/dist/leaflet.css";
/* Map component styles go here */
#map {
  width: 98%;
  height: 98%;
  overflow: hidden;
}
</style>