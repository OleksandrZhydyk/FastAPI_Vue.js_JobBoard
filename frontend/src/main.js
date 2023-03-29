import "bootstrap/dist/css/bootstrap.css"
import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios';
import components from '@/components';
import router from '@/router';
import store from '@/store';


const app = createApp(App).use(router)

import "bootstrap/dist/js/bootstrap.js"

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:8000/';
axios.interceptors.response.use( resp => resp, async error => {
    console.log(error.config)
    if (error.response.status === 422 && error.response.data.detail === "Signature has expired"){
        const {status} = await axios.post('/auth/refresh', {
            withCredentials: true,
        })
    };
    if (status === 200){
        return axios(error.config)
    };
})

components.forEach(component => {
    app.component(component.name, component)
})

app.use(router);
app.use(store);
app.mount('#app');
