import "bootstrap/dist/css/bootstrap.css"
import "bootstrap/dist/js/bootstrap.js"
import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios';
import components from '@/components';
import router from '@/router';
import store from '@/store';


const app = createApp(App).use(router);

components.forEach(component => {
    app.component(component.name, component)
})

app.use(store);
app.mount('#app');

axios.defaults.withCredentials = true;
axios.defaults.baseURL = process.env.VUE_APP_BACKEND;

axios.interceptors.response.use( resp => resp, async error => {
  if (error.response.status === 422 && error.response.data.detail === "Signature has expired" && !store.state.allUsers.refreshExpired){
    store.commit('allUsers/setRefreshExpired', true)
    const res = await axios.post('/auth/refresh', {
      withCredentials: true,
    })
    if (res && res.status === 200){
      store.commit('allUsers/setRefreshExpired', false)
      return axios(error.config)
    }

  } else if (error.response.status === 422 && error.response.data.detail === "Signature has expired" && store.state.allUsers.refreshExpired){
    store.commit('allUsers/setRefreshExpired', false)
    store.commit('allUsers/setUser', null)
    return router.push('/login')
  } else {
    store.commit('allUsers/setErrors', error.response.data.detail)
  }
})
