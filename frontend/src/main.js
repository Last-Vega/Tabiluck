import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import axios from 'axios'
import * as GoogleMaps from 'vue2-google-maps'
import Geocoder from '@pderas/vue2-geocoder'
axios.defaults.baseURL = process.env.VUE_APP_BASE_URL
axios.defaults.headers.post['Content-Type'] = 'application/json;charset=utf-8'
axios.defaults.headers.post['Access-Control-Allow-Origin'] = '*'

Vue.config.productionTip = false

Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)
Vue.prototype.$api = axios // this.$apiでaxiosを呼び出せるようにする。

Vue.use(GoogleMaps, {
  load: {
    key: process.env.VUE_APP_API_KEY,
    libraries: 'places'
  }
})

Vue.use(Geocoder, {
  defaultCountryCode: null, // e.g. 'CA'
  defaultLanguage: null, // e.g. 'en'
  // defaultMode:        'address', // or 'lat-lng'
  googleMapsApiKey: process.env.VUE_APP_API_KEY
})

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
