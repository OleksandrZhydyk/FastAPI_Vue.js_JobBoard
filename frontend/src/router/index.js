import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import VacanciesView from '@/views/VacanciesView.vue'
import VacancyDetailView from '@/views/VacancyDetailView.vue'
import CompanyVacancies from '@/views/CompanyVacancies.vue'
import VacancyAppliers from '@/views/VacancyAppliers.vue'
import VacancyUpdate from '@/views/VacancyUpdate.vue'
import store from '@/store'

const routes = [
  {
    path: '/',
    name: 'main',
    component: VacanciesView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/me/vacancies',
    name: 'companyVacancies',
    component: CompanyVacancies,
    meta: { requiresAuth: true },
  },
  {
    path: '/vacancies/:id',
    name: 'vacancies',
    component: VacancyDetailView
  },
  {
    path: '/vacancies/:id/update',
    name: 'vacanciesUpdate',
    component: VacancyUpdate,
    meta: { requiresAuth: true },
  },
  {
    path: '/vacancies/:id/appliers',
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
