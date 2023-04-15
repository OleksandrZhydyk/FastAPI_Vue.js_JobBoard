import { createRouter, createWebHistory } from 'vue-router'
import VacanciesView from '@/views/VacanciesView.vue'
import store from '@/store'

const routes = [
  {
    path: '/',
    name: 'main',
    component: VacanciesView
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/RegisterView.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue')
  },
  {
    path: '/users/profile/:id(\\d+)',
    name: 'applicantProfile',
    component: () => import('@/views/ApplicantProfile.vue'),
    meta: { isCompany: true },
  },
  {
    path: '/me/vacancies',
    name: 'companyVacancies',
    component: () => import('@/views/CompanyVacancies.vue'),
    meta: { isCompany: true },
  },
  {
    path: '/me',
    name: 'userProfile',
    component: () => import('@/views/UserProfile.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/me/applied_vacancies',
    name: 'appliedVacancies',
    component: () => import('@/views/AppliedVacancies.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/me/vacancies/archive',
    name: 'archivedVacancies',
    component: () => import('@/views/ArchivedVacancies.vue'),
    meta: { isCompany: true },
  },
  {
    path: '/vacancies/create',
    name: 'createVacancy',
    component: () => import('@/views/CreateVacancy.vue'),
    meta: { isCompany: true },
  },
  {
    path: '/vacancies/:id(\\d+)',
    name: 'vacancies',
    component: () => import('@/views/VacancyDetailView.vue')
  },
  {
    path: '/vacancies/:id(\\d+)/update',
    name: 'vacanciesUpdate',
    component: () => import('@/views/VacancyUpdate.vue'),
    meta: { isCompany: true },
  },
  {
    path: '/vacancies/:id(\\d+)/appliers',
    name: 'appliers',
    component: () => import('@/views/VacancyAppliers.vue'),
    meta: { isCompany: true },
  },
  {
    path: '/forbidden',
    name: 'forbidden',
    component: () => import('@/views/Forbidden.vue'),
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not_found',
    component: () => import('@/views/PageNotFound.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, _, next) => {
  store.commit('allUsers/setErrors', null);
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (store.getters['allUsers/isAuthenticated']) {
      next();
      return;
    }
    next('/login');
    return;
  }
  if (to.matched.some(record => record.meta.isCompany)) {
    if (store.getters['allUsers/isCompany']) {
      next();
      return;
    }
    next('/forbidden');
    return;
  }
 else {
    next();
  }
});

export default router
