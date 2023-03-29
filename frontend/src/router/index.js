import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import JobsView from '@/views/JobsView.vue'
import JobDetailView from '@/views/JobDetailView.vue'
import CompanyVacancies from '@/views/CompanyVacancies.vue'
import VacancyAppliers from '@/views/VacancyAppliers.vue'
import store from '@/store'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/',
    name: 'main',
    component: JobsView
  },
  {
    path: '/jobs/:id',
    name: 'jobs',
    component: JobDetailView
  },
  {
    path: '/jobs/:id/appliers',
    name: 'appliers',
    component: VacancyAppliers,
    meta: { requiresAuth: true },
  },
  {
    path: '/me/jobs',
    name: 'companyVacancies',
    component: CompanyVacancies,
    meta: { requiresAuth: true },
  },
  {
    path: '/about',
    name: 'about',
    component: () => import(/* webpackChunkName: "about" */ '@/views/AboutView.vue')
  },
//  { path: '*', redirect: '/' },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, _, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (store.getters['allUsers/isAuthenticated']) {
      next();
      return;
    }
    next('/login');
  } else {
    next();
  }
});

export default router
