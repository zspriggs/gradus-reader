import { createApp } from 'vue';
import App from './App.vue';
import './assets/main.css';

import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(),
  routes: [],
});

const app = createApp(App).mount('#app');
app.use(router);
