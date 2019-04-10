import Vue from 'vue'
import App from './App'
import router from './router'

import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import './assets/sass/index.scss'

import axios from 'axios'
import VueAxios from 'vue-axios'
// import JwtDecode from 'jwt-decode'

import Vuex from 'vuex'
import store from './store'

Vue.use(Vuex)
Vue.use(BootstrapVue)
Vue.use(VueAxios, axios)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
