import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios';
import router from './router'

const app = createApp(App).use(router)

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:8000/';


app.use(router);
app.mount('#app');
