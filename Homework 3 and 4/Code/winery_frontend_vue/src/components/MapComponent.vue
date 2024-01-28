<template>
    <!-- Map integration goes here -->
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
    const select_marker = null;
    const initial_view = {
      center: [41.6086, 21.7453],
      zoom: 8
    };
    return {
      language,
      select_marker,
      initial_view
    };
  },
  data() {
    return {
      map: null,
      icon_properties: {
        iconSize: [50, 50],
        iconAnchor: [25, 50],
        popupAnchor: [0, -25],
      },
      selected_icon_url: 'src/components/Icons/custom_red_marker.png',
      default_icon_url: 'src/components/Icons/default_marker_icon.png'
    };
  },
  async mounted() {
    // Map initialization
    this.map = L.map(this.$refs.map).setView(this.initial_view.center, this.initial_view.zoom);
    // Adding OpenStreetMap tile layer
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 22,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(this.map);
    await this.getAllCoordinates();
  },
  methods: {
    async mapData(parsed_data) {
      return parsed_data.map(obj => {
        return {
          ID: obj.ID,
          Name: obj.Name,
          Latitude: obj.Latitude,
          Longitude: obj.Longitude
        };
      })
    },
    async getAllCoordinates() {
      try {
        // Request for getting coordinates
        const response = await axios.get('http://127.0.0.1:8002/coordinates_info');
        const data = response.data['data'];
        const parsed_data = JSON.parse(data);
        // Creating markers
        await this.createMarkers(parsed_data);
      } catch (error) {
        console.error('Error fetching coordinates:', error);
      }
    },
    async createMarkers(data){
      this.map.setView(this.initial_view.center, this.initial_view.zoom);
      // Reset selected marker
      this.select_marker = null;
      // Map needed data for markers
      let markers = await this.mapData(data);
      // Reset all markers
      await this.removeAllMarkers()
      for (const obj of markers) {
        // Create marker and user interaction with it
        await this.addNewMarker(obj.Latitude, obj.Longitude, obj.ID, obj.Name);
      }
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
      if (this.language === 'EN') {
        latin = true;
      }
      if (latin) {
        name = transliterate(name);
      }
      // Create a marker with the specified icon URL
      const marker = L.marker([latitude, longitude], {
        icon: L.icon({
          iconUrl: this.default_icon_url,
          ...this.icon_properties
        }),
      }).addTo(this.map);
      // Store the obj.ID as a custom property on the marker
      marker.objID = id;
      marker.on('click', () => {
        // Emit event when clicked
        this.$emit('markerClicked', id, 1);
        this.selectMarker(marker);
      });
    },
    selectMarker(marker) {
      // Change the icon for the previously selected marker (if any) to the default icon
      if (this.select_marker) {
        this.select_marker.setIcon(L.icon({
          iconUrl: this.default_icon_url,
          ...this.icon_properties
        }));
      }
      // Set the icon for the clicked marker to the selected icon
      marker.setIcon(L.icon({
        iconUrl: this.selected_icon_url,
        ...this.icon_properties
      }));
      // Update the selected marker
      this.select_marker = marker;
    },
    findMarker(id) {
      let found_marker = null;

      // Iterate through each marker on the map
      this.map.eachLayer(layer => {
        if (layer instanceof L.Marker) {
          const marker_id = layer.objID;

          // Check if the marker objID matches the provided ID
          if (marker_id === id) {
            found_marker = layer;
          }
        }
      });
      if (found_marker) {
        // Zoom to the selected marker
        this.selectMarker(found_marker);
        this.map.setView(found_marker.getLatLng(), 13);
      }
    },
    async checkLocation(winery_ids) {
      try {
        const response = await axios.post(
            'http://127.0.0.1:8002/check_location',
            { "winery_ids": winery_ids }
          );
        const data = response.data['data'];
        const parsed_data = JSON.parse(data);
        // Create filtered markers
        await this.createMarkers(parsed_data);
      } catch (error) {
        console.error("Error checking winery locations:", error);
      }
    },
  }
};
</script>

<style scoped>
@import "leaflet/dist/leaflet.css";
#map {
  width: 98%;
  height: 98%;
  overflow: hidden;
}
</style>