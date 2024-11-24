import { createRouter, createWebHistory } from 'vue-router';
import Welcome from '../pages/Welcome.vue';
import UserPage from '../pages/[user].vue';

const routes = [
  { path: '/', component: Welcome },
  { 
    path: '/:user',
    component: UserPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;