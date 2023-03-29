import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import JobsView from '@/views/JobsView.vue'
import JobDetailView from '@/views/JobDetailView.vue'
import CompanyVacancies from '@/views/CompanyVacancies.vue'
import VacancyAppliers from '@/views/VacancyAppliers.vue'
import JobUpdate from '@/views/JobUpdate.vue'
import store from '@/store'

const routes = [
  {
    path: '/',
    name: 'main',
    component: JobsView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/me/jobs',
    name: 'companyVacancies',
    component: CompanyVacancies,
    meta: { requiresAuth: true },
  },
  {
    path: '/jobs/:id',
    name: 'jobs',
    component: JobDetailView
  },
  {
    path: '/jobs/:id/update',
    name: 'jobsUpdate',
    component: JobUpdate,
    meta: { requiresAuth: true },
  },
  {
    path: '/jobs/:id/appliers',
    name: 'appliers',
    component: VacancyAppliers,
    meta: { requiresAuth: true },
  },
  {
    path: '/about',
    name: 'about',
    component: () => import(/* webpackChunkName: "about" */ '@/views/AboutView.vue')
  },
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
